"""
Main FastAPI application for JAI API
"""
import os
import logging
import re
import time
import json
from fastapi import FastAPI, Request, HTTPException, Depends, Path, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import requests

# Import error handling
from api.utils.error_handling import get_error_handlers, validation_exception_handler
# Import input parsing utilities
from api.utils.input_parser import parse_date, parse_time, clean_json_string

# Create logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("jai-api")

# Rate limiting configuration
RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", "100"))  # requests per window
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "3600"))  # window in seconds
MAX_REQUEST_SIZE = int(os.environ.get("MAX_REQUEST_SIZE", "1024"))  # max request size in KB

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Clean old entries
        current_time = time.time()
        self.requests = {
            ip: timestamps 
            for ip, timestamps in self.requests.items()
            if current_time - timestamps[-1] < RATE_LIMIT_WINDOW
        }
        
        # Check rate limit
        if client_ip in self.requests:
            timestamps = self.requests[client_ip]
            if len(timestamps) >= RATE_LIMIT_REQUESTS:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )
            timestamps.append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_REQUEST_SIZE * 1024:
            logger.warning(f"Request too large from IP: {client_ip}")
            return JSONResponse(
                status_code=413,
                content={"detail": f"Request too large. Maximum size is {MAX_REQUEST_SIZE}KB."}
            )
        
        return await call_next(request)

# Create FastAPI app
app = FastAPI(
    title="JAI - Jyotish Astrological Interpretation API",
    description="API for Vedic astrology calculations",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

# Add security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(RateLimitMiddleware)

# Register exception handlers
exception_handlers = get_error_handlers()
for exc, handler in exception_handlers.items():
    app.add_exception_handler(exc, handler)

# Add validation error handler
app.add_exception_handler(ValidationError, validation_exception_handler)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler for HTTP exceptions"""
    logger.warning(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation",
        "version": "1.0.0",
        "endpoints": [
            "/v1/api/health",
            "/v1/api/horoscope/planets",
            "/v1/api/horoscope/ascendant",
            "/v1/api/horoscope"
        ]
    }

# Health check endpoint
@app.get("/v1/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Main application initialization
def create_app():
    """Initialize and configure the application"""
    # Import routers from routes module
    from api.routes import ascendant_router, planets_router
    
    # Include routers
    app.include_router(ascendant_router)
    app.include_router(planets_router)
    
    # Add any additional routers here in the future
    
    return app 