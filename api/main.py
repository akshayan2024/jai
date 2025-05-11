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
from api.services.ephemeris_service import ephemeris_service
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import error handling
from api.utils.error_handling import get_error_handlers, validation_exception_handler

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

# Initialize rate limiter (60 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=429,
    content={"detail": "Rate limit exceeded. Please try again later."}
))

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    response = await limiter(request, call_next)
    return response

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

# Register exception handlers
exception_handlers = get_error_handlers()
for exc, handler in exception_handlers.items():
    app.add_exception_handler(exc, handler)

# Add validation error handler
app.add_exception_handler(ValidationError, validation_exception_handler)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    # Use environment variable for allowed origins in production
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
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
            "/v1/api/horoscope",
            "/v1/api/horoscope/planets",
            "/v1/api/horoscope/ascendant"
        ]
    }

# Health check endpoint
@app.get("/v1/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Swiss Ephemeris initialization
        test_jd = ephemeris_service.julday(2000, 1, 1, 0)
        xx, ret = ephemeris_service.get_planet_position(test_jd, 0)  # Test with Sun
        if ret < 0:
            raise RuntimeError(f"Swiss Ephemeris test failed with error code {ret}")
        return {"status": "healthy", "ephemeris": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

# Main application initialization
def create_app():
    """Initialize and configure the application"""
    # Import routers from routes module
    from api.routes import ascendant_router, planets_router, horoscope_router
    
    # Include routers
    app.include_router(ascendant_router)
    app.include_router(planets_router)
    app.include_router(horoscope_router)
    
    return app 