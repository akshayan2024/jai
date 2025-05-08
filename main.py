"""
JAI - Jyotish Astrological Interpretation API
Simple entry point with absolute imports for deployment
"""

import os
import logging
import re
import time
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, validator, constr
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

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
    title="JAI Astrological API",
    description="API for Vedic astrological calculations based on the Swiss Ephemeris.",
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

# Add security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(RateLimitMiddleware)

# Add CORS middleware with proper configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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

# Validation patterns
DATE_PATTERN = r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"
TIME_PATTERN = r"^(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)$"
TIME_PATTERN_SHORT = r"^(?:[01]\d|2[0-3]):(?:[0-5]\d)$"

# Basic models
class AyanamsaEnum(str, Enum):
    LAHIRI = "lahiri"
    RAMAN = "raman"
    KRISHNAMURTI = "krishnamurti"

class BirthDataRequest(BaseModel):
    birth_date: constr(regex=DATE_PATTERN) = Field(..., description="Date of birth in YYYY-MM-DD format")
    birth_time: constr(regex=TIME_PATTERN) = Field(..., description="Time of birth in HH:MM:SS format (24h)")
    latitude: float = Field(..., ge=-90, le=90, description="Birth latitude (-90 to +90)")
    longitude: float = Field(..., ge=-180, le=180, description="Birth longitude (-180 to +180)")
    timezone_offset: float = Field(..., ge=-12, le=14, description="Time zone offset from UTC in hours")
    ayanamsa: AyanamsaEnum = Field(AyanamsaEnum.LAHIRI, description="Ayanamsa method")

    @validator('birth_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Must be YYYY-MM-DD")

    @validator('birth_time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Must be HH:MM:SS")

# Also accept alternative property names that might be sent by clients
class AlternativeBirthDataRequest(BaseModel):
    dateOfBirth: Optional[constr(regex=DATE_PATTERN)] = Field(None, description="Date of birth in YYYY-MM-DD format")
    timeOfBirth: Optional[constr(regex=TIME_PATTERN_SHORT)] = Field(None, description="Time of birth in HH:MM format")
    birth_date: Optional[constr(regex=DATE_PATTERN)] = Field(None, description="Date of birth in YYYY-MM-DD format")
    birth_time: Optional[constr(regex=TIME_PATTERN)] = Field(None, description="Time of birth in HH:MM:SS format (24h)")
    latitude: float = Field(..., ge=-90, le=90, description="Birth latitude (-90 to +90)")
    longitude: float = Field(..., ge=-180, le=180, description="Birth longitude (-180 to +180)")
    timezone_offset: Optional[float] = Field(None, ge=-12, le=14, description="Time zone offset from UTC in hours")
    timezone: Optional[float] = Field(None, ge=-12, le=14, description="Alternative field for timezone offset")
    ayanamsa: AyanamsaEnum = Field(AyanamsaEnum.LAHIRI, description="Ayanamsa method")
    
    @validator('dateOfBirth', 'birth_date')
    def validate_date(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
                return v
            except ValueError:
                raise ValueError("Invalid date format. Must be YYYY-MM-DD")
        return v

    @validator('timeOfBirth')
    def validate_short_time(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%H:%M")
                return v
            except ValueError:
                raise ValueError("Invalid time format. Must be HH:MM")
        return v

    @validator('birth_time')
    def validate_full_time(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%H:%M:%S")
                return v
            except ValueError:
                raise ValueError("Invalid time format. Must be HH:MM:SS")
        return v

    def get_standardized_request(self) -> BirthDataRequest:
        """Convert to standardized request format with validation"""
        if not (self.birth_date or self.dateOfBirth):
            raise HTTPException(status_code=400, detail="Date of birth is required")
        
        if not (self.birth_time or self.timeOfBirth):
            raise HTTPException(status_code=400, detail="Time of birth is required")

        timezone = self.timezone_offset or self.timezone
        if timezone is None:
            raise HTTPException(status_code=400, detail="Timezone offset is required")

        return BirthDataRequest(
            birth_date=self.birth_date or self.dateOfBirth,
            birth_time=self.birth_time or f"{self.timeOfBirth}:00",
            latitude=self.latitude,
            longitude=self.longitude,
            timezone_offset=timezone,
            ayanamsa=self.ayanamsa
        )

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

# Horoscope endpoint with our standard path pattern
@app.post("/v1/api/horoscope", tags=["Horoscope"])
async def get_horoscope(request: BirthDataRequest):
    """
    Generate a Vedic horoscope based on birth data.
    This is a simplified implementation for testing deployment.
    """
    # Log request
    logger.info(f"Horoscope request received for birth date: {request.birth_date}")
    
    # Return horoscope data
    return generate_horoscope_response(request)

# Alternative horoscope endpoint matching the requested path pattern
@app.post("/api/v1/horoscope", tags=["Horoscope"], include_in_schema=False)
async def get_horoscope_alt_path(request: AlternativeBirthDataRequest):
    """
    Alternative path for generating a Vedic horoscope.
    This handles requests to /api/v1/horoscope which is the reverse of our standard pattern.
    """
    # Log request with special note
    logger.info(f"Alternative path horoscope request received")
    
    # Convert to our standard format
    std_request = request.get_standardized_request()
    
    # Return horoscope data using the same function
    return generate_horoscope_response(std_request)

def safe_parse_datetime(date_str: str, time_str: str) -> datetime:
    """Safely parse datetime from date and time strings"""
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error(f"Failed to parse datetime: {date_str} {time_str}")
        raise HTTPException(status_code=400, detail=f"Invalid date/time format: {str(e)}")

# Update the generate_horoscope_response function
def generate_horoscope_response(request: BirthDataRequest):
    """Generate a consistent horoscope response with error handling"""
    try:
        # Parse birth datetime
        birth_datetime = safe_parse_datetime(request.birth_date, request.birth_time)
        
        # Log the request with sanitized data
        logger.info(
            "Horoscope request received",
            extra={
                "birth_date": request.birth_date,
                "birth_time": request.birth_time,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "timezone": request.timezone_offset,
                "ayanamsa": request.ayanamsa
            }
        )

        # Mock planetary positions (in a real implementation, these would be calculated)
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
        
        # Calculate dasha periods
        mahadasha = calculate_dasha_periods(birth_datetime)
        
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
    except Exception as e:
        logger.error(f"Error generating horoscope: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate horoscope")

def calculate_dasha_periods(birth_datetime: datetime) -> List[Dict[str, Any]]:
    """Calculate dasha periods with error handling"""
    try:
        return [
            {
                "planet": "Saturn",
                "start_date": birth_datetime.strftime("%Y-%m-%d"),
                "end_date": (birth_datetime + timedelta(days=365*19)).strftime("%Y-%m-%d"),
                "years": 19
            },
            {
                "planet": "Mercury",
                "start_date": (birth_datetime + timedelta(days=365*19)).strftime("%Y-%m-%d"),
                "end_date": (birth_datetime + timedelta(days=365*(19+17))).strftime("%Y-%m-%d"),
                "years": 17
            }
        ]
    except Exception as e:
        logger.error(f"Error calculating dasha periods: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to calculate dasha periods")

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