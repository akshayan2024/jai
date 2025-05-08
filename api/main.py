"""
Main FastAPI application for JAI API
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any, List, Optional

# Create FastAPI app
app = FastAPI(
    title="JAI API",
    description="Jyotish Astrological Interpretation API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Rate limiting
rate_limit_store = {}

async def rate_limiter(request: Request):
    """Basic IP-based rate limiting middleware"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Check if client is in store
    if client_ip in rate_limit_store:
        # Get last request time
        last_request_time = rate_limit_store[client_ip]
        
        # If less than 1 second since last request
        if current_time - last_request_time < 1:
            raise HTTPException(
                status_code=429, 
                detail="Too many requests. Please try again later."
            )
    
    # Update store with current time
    rate_limit_store[client_ip] = current_time
    return client_ip

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation",
        "version": "1.0.0",
        "endpoints": [
            "/v1/api/health",
            "/v1/api/horoscope",
            "/api/v1/horoscope"  # Alternative endpoint
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
    
    return app 