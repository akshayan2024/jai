"""
JAI - Jyotish Astrological Interpretation API
Simple entry point with absolute imports for deployment
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime, timedelta

# Create logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("jai-api")

# Create FastAPI app
app = FastAPI(
    title="JAI Astrological API",
    description="API for Vedic astrological calculations based on the Swiss Ephemeris.",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic models
class AyanamsaEnum(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KRISHNAMURTI = "krishnamurti"

class BirthDataRequest(BaseModel):
    birth_date: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    birth_time: str = Field(..., description="Time of birth in HH:MM:SS format (24h)")
    latitude: float = Field(..., description="Birth latitude (-90 to +90)")
    longitude: float = Field(..., description="Birth longitude (-180 to +180)")
    timezone_offset: float = Field(..., description="Time zone offset from UTC in hours")
    ayanamsa: AyanamsaEnum = Field(AyanamsaEnum.LAHIRI, description="Ayanamsa method")

# Health check
@app.get("/v1/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development")
    }

# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation",
        "documentation": "/v1/docs",
        "status": "online"
    }

# Example endpoint
@app.post("/v1/api/ascendant", tags=["Example"])
async def get_ascendant_example(request: BirthDataRequest):
    """
    This is a simplified example endpoint for testing deployment.
    In the full version, this would calculate the ascendant based on birth data.
    """
    return {
        "ascendant_degree": 123.456,
        "ascendant_sign": 5,
        "ascendant_sign_name": "Leo",
        "birth_data": {
            "date": request.birth_date,
            "time": request.birth_time,
            "latitude": request.latitude,
            "longitude": request.longitude,
        }
    }

# Horoscope endpoint
@app.post("/v1/api/horoscope", tags=["Horoscope"])
async def get_horoscope(request: BirthDataRequest):
    """
    Generate a Vedic horoscope based on birth data.
    This is a simplified implementation for testing deployment.
    """
    # Log request
    logger.info(f"Horoscope request received for birth date: {request.birth_date}")
    
    # Generate horoscope data
    return generate_horoscope_response(request)

# Alternate pattern for the horoscope endpoint (/api/v1/... instead of /v1/api/...)
@app.post("/api/v1/horoscope", tags=["Horoscope"], include_in_schema=False)
async def get_horoscope_alt(request: BirthDataRequest):
    """
    Alternative URL pattern for the horoscope endpoint.
    Some clients may expect /api/v1/... instead of /v1/api/...
    """
    # Log request with note about alternate endpoint
    logger.info(f"Horoscope request received at alternate endpoint for birth date: {request.birth_date}")
    
    # Use the same response generation as the primary endpoint
    return generate_horoscope_response(request)

# Helper function to generate horoscope response (used by both endpoints)
def generate_horoscope_response(request: BirthDataRequest):
    """Generate a horoscope response based on the request data."""
    # Mock planetary positions
    planets = [
        {"planet": "Sun", "longitude": 105.23, "sign_index": 4, "sign_name": "Leo", "house": 5, "is_retrograde": False},
        {"planet": "Moon", "longitude": 78.45, "sign_index": 3, "sign_name": "Cancer", "house": 4, "is_retrograde": False},
        {"planet": "Mars", "longitude": 32.18, "sign_index": 2, "sign_name": "Taurus", "house": 2, "is_retrograde": False},
        {"planet": "Mercury", "longitude": 95.67, "sign_index": 4, "sign_name": "Leo", "house": 5, "is_retrograde": True},
        {"planet": "Jupiter", "longitude": 210.34, "sign_index": 8, "sign_name": "Scorpio", "house": 8, "is_retrograde": False},
        {"planet": "Venus", "longitude": 150.78, "sign_index": 6, "sign_name": "Virgo", "house": 6, "is_retrograde": False},
        {"planet": "Saturn", "longitude": 280.12, "sign_index": 10, "sign_name": "Capricorn", "house": 10, "is_retrograde": True},
        {"planet": "Rahu", "longitude": 55.89, "sign_index": 2, "sign_name": "Taurus", "house": 2, "is_retrograde": False},
        {"planet": "Ketu", "longitude": 235.89, "sign_index": 8, "sign_name": "Scorpio", "house": 8, "is_retrograde": False}
    ]
    
    # Mock ascendant info
    ascendant = {
        "ascendant_degree": 45.67,
        "ascendant_sign": 2,
        "ascendant_sign_name": "Taurus"
    }
    
    # Mock dasha periods
    birth_date_obj = datetime.strptime(request.birth_date, "%Y-%m-%d")
    current_date = datetime.now().date()
    
    mahadasha = [
        {
            "planet": "Saturn",
            "start_date": (birth_date_obj).strftime("%Y-%m-%d"),
            "end_date": (birth_date_obj + timedelta(days=365*19)).strftime("%Y-%m-%d"),
            "years": 19
        },
        {
            "planet": "Mercury",
            "start_date": (birth_date_obj + timedelta(days=365*19)).strftime("%Y-%m-%d"),
            "end_date": (birth_date_obj + timedelta(days=365*(19+17))).strftime("%Y-%m-%d"),
            "years": 17
        }
    ]
    
    # Return a simulated horoscope
    return {
        "birth_data": {
            "date": request.birth_date,
            "time": request.birth_time,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "timezone_offset": request.timezone_offset,
            "ayanamsa": request.ayanamsa
        },
        "ascendant": ascendant,
        "planets": planets,
        "mahadasha": mahadasha,
        "generated_at": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up JAI API")
    
# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("JAI API shutting down")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)