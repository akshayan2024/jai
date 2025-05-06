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