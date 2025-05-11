"""
Main FastAPI application for JAI API - Simplified for direct integration with ChatGPT
"""
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import requests
from api.services.ephemeris_service import ephemeris_service
from api.utils.error_handling import validation_exception_handler

# Create logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("jai-api")

# Create FastAPI app
app = FastAPI(
    title="JAI - Jyotish Astrological Interpretation API",
    description="API for Vedic astrology calculations. Designed for direct integration with ChatGPT Actions. Provides ascendant calculation, planetary positions, dashas, and more.",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

# Add validation error handler
app.add_exception_handler(ValidationError, validation_exception_handler)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation",
        "version": "1.0.0",
        "endpoints": [
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