"""
Response data models for JAI API
Designed for consistency and optimal consumption

All response models should inherit from BaseResponse for consistent structure.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class BaseResponse(BaseModel):
    """Base response model with metadata for all API responses"""
    status: str = Field("success", description="Response status (success or error)")
    version: str = Field("1.0", description="API version")
    generated_at: str = Field(..., description="Timestamp when the response was generated")
    request_params: Dict[str, Any] = Field(..., description="Original request parameters")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "version": "1.0",
                "generated_at": "2023-07-01T12:34:56.789Z",
                "request_params": {
                    "birth_date": "1990-01-01",
                    "birth_time": "12:00:00",
                    "place": "Chennai, India",
                    "ayanamsa": "lahiri"
                }
            }
        }

class ErrorResponse(BaseResponse):
    """Standardized error response model"""
    status: str = Field("error", description="Error status")
    error_code: str = Field(..., description="Error code for programmatic handling")
    error_message: str = Field(..., description="Human-readable error description")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Additional error context")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "version": "1.0",
                "generated_at": "2023-07-01T12:34:56.789Z",
                "request_params": {
                    "birth_date": "1990-01-01",
                    "birth_time": "invalid_time",
                    "place": "Chennai, India"
                },
                "error_code": "INVALID_TIME_FORMAT",
                "error_message": "The provided birth time is invalid",
                "error_details": {
                    "parameter": "birth_time",
                    "expected_format": "HH:MM:SS",
                    "received_value": "invalid_time"
                }
            }
        }

class PlanetInfo(BaseModel):
    """Planetary position information"""
    name: str = Field(..., description="Planet name")
    sanskrit_name: str = Field(..., description="Sanskrit name of the planet")
    longitude: float = Field(..., description="Longitude in degrees (0-360)")
    latitude: Optional[float] = Field(None, description="Latitude in degrees")
    sign: str = Field(..., description="Zodiac sign name")
    sign_id: int = Field(..., description="Zodiac sign ID (1-12)")
    sign_longitude: float = Field(..., description="Longitude within the sign (0-30)")
    house: int = Field(..., description="House position (1-12)")
    nakshatra: str = Field(..., description="Nakshatra (lunar mansion) name")
    nakshatra_id: int = Field(..., description="Nakshatra ID (1-27)")
    nakshatra_pada: int = Field(..., description="Nakshatra pada (1-4)")
    degrees: int = Field(..., description="Degrees within sign (0-29)")
    minutes: int = Field(..., description="Minutes (0-59)")
    seconds: int = Field(..., description="Seconds (0-59)")
    is_retrograde: bool = Field(..., description="Whether the planet is retrograde")
    speed: float = Field(..., description="Planet's speed in degrees per day")
    dignity: str = Field(..., description="Planet's dignity in the sign")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jupiter",
                "sanskrit_name": "Guru",
                "longitude": 95.83,
                "latitude": 1.07,
                "sign": "Cancer",
                "sign_id": 4,
                "sign_longitude": 5.83,
                "house": 4,
                "nakshatra": "Pushya",
                "nakshatra_id": 8,
                "nakshatra_pada": 2,
                "degrees": 5,
                "minutes": 49,
                "seconds": 48,
                "is_retrograde": False,
                "speed": 0.12,
                "dignity": "Exalted"
            }
        }

class AscendantInfo(BaseModel):
    """Ascendant (Lagna) information"""
    sign: str = Field(..., description="Ascendant sign name")
    sign_id: int = Field(..., description="Ascendant sign ID (1-12)")
    longitude: float = Field(..., description="Absolute longitude in degrees (0-360)")
    degrees: int = Field(..., description="Degrees within sign (0-29)")
    minutes: int = Field(..., description="Minutes (0-59)")
    seconds: int = Field(..., description="Seconds (0-59)")
    nakshatra: str = Field(..., description="Nakshatra name")
    nakshatra_id: int = Field(..., description="Nakshatra ID (1-27)")
    nakshatra_pada: int = Field(..., description="Nakshatra pada (1-4)")
    
    class Config:
        schema_extra = {
            "example": {
                "sign": "Taurus",
                "sign_id": 2,
                "longitude": 45.23,
                "degrees": 15,
                "minutes": 13,
                "seconds": 48,
                "nakshatra": "Rohini",
                "nakshatra_id": 4,
                "nakshatra_pada": 2
            }
        }

class HouseInfo(BaseModel):
    """House information"""
    house_number: int = Field(..., description="House number (1-12)")
    sign: str = Field(..., description="Sign of house cusp")
    sign_id: int = Field(..., description="Sign ID of house cusp (1-12)")
    longitude: float = Field(..., description="Absolute longitude in degrees (0-360)")
    degrees: int = Field(..., description="Degrees within sign (0-29)")
    minutes: int = Field(..., description="Minutes (0-59)")
    seconds: int = Field(..., description="Seconds (0-59)")
    
    class Config:
        schema_extra = {
            "example": {
                "house_number": 1,
                "sign": "Taurus",
                "sign_id": 2,
                "longitude": 45.23,
                "degrees": 15,
                "minutes": 13,
                "seconds": 48
            }
        }

class DashaPeriod(BaseModel):
    """Dasha period information"""
    planet: str = Field(..., description="Ruling planet name")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    years: float = Field(..., description="Duration in years")
    
    class Config:
        schema_extra = {
            "example": {
                "planet": "Jupiter",
                "start_date": "2023-01-01",
                "end_date": "2039-01-01",
                "years": 16
            }
        }

class BirthDataInfo(BaseModel):
    """Birth data information including derived location details"""
    date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    time: str = Field(..., description="Birth time (HH:MM:SS)")
    place: Optional[str] = Field(None, description="Place name if provided")
    latitude: float = Field(..., description="Birth latitude")
    longitude: float = Field(..., description="Birth longitude")
    timezone_offset: float = Field(..., description="Timezone offset in hours")
    ayanamsa: str = Field(..., description="Ayanamsa method used")
    julian_day: float = Field(..., description="Julian day for the birth time")
    location_derived: bool = Field(..., description="Whether location was derived from place name")
    
    class Config:
        schema_extra = {
            "example": {
                "date": "1990-01-01",
                "time": "12:00:00",
                "place": "Chennai, India",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "timezone_offset": 5.5,
                "ayanamsa": "lahiri",
                "julian_day": 2447893.0,
                "location_derived": True
            }
        }

class HoroscopeResponse(BaseResponse):
    """Complete horoscope response with all calculated elements"""
    birth_data: BirthDataInfo = Field(..., description="Birth data information")
    ascendant: AscendantInfo = Field(..., description="Ascendant information")
    planets: List[PlanetInfo] = Field(..., description="Planetary positions")
    houses: List[HouseInfo] = Field(..., description="House cusps")
    mahadasha: List[DashaPeriod] = Field(..., description="Mahadasha periods")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "version": "1.0",
                "generated_at": "2023-07-01T12:34:56.789Z",
                "request_params": {
                    "birth_date": "1990-01-01",
                    "birth_time": "12:00:00",
                    "place": "Chennai, India",
                    "ayanamsa": "lahiri"
                },
                "birth_data": {
                    "date": "1990-01-01",
                    "time": "12:00:00",
                    "place": "Chennai, India",
                    "latitude": 13.0827,
                    "longitude": 80.2707,
                    "timezone_offset": 5.5,
                    "ayanamsa": "lahiri",
                    "julian_day": 2447893.0,
                    "location_derived": True
                },
                "ascendant": {
                    "sign": "Taurus",
                    "sign_id": 2,
                    "longitude": 45.23,
                    "degrees": 15,
                    "minutes": 13,
                    "seconds": 48,
                    "nakshatra": "Rohini",
                    "nakshatra_id": 4,
                    "nakshatra_pada": 2
                },
                "planets": [
                    {
                        "name": "Sun",
                        "sanskrit_name": "Surya",
                        "longitude": 256.83,
                        "latitude": 0.0,
                        "sign": "Sagittarius",
                        "sign_id": 9,
                        "sign_longitude": 16.83,
                        "house": 8,
                        "nakshatra": "Purva Ashadha",
                        "nakshatra_id": 19,
                        "nakshatra_pada": 3,
                        "degrees": 16,
                        "minutes": 49,
                        "seconds": 48,
                        "is_retrograde": False,
                        "speed": 1.02,
                        "dignity": "Neutral"
                    }
                ],
                "houses": [
                    {
                        "house_number": 1,
                        "sign": "Taurus",
                        "sign_id": 2,
                        "longitude": 45.23,
                        "degrees": 15,
                        "minutes": 13,
                        "seconds": 48
                    }
                ],
                "mahadasha": [
                    {
                        "planet": "Saturn",
                        "start_date": "1990-01-01",
                        "end_date": "2009-01-01",
                        "years": 19
                    }
                ]
            }
        }

class AspectInfo(BaseModel):
    """Planetary aspect information"""
    graha_1: str
    graha_2: str
    type: str
    angle: float
    orb: float
    is_exact: bool
    is_applying: bool
    strength: float
    description: str

class AntarDashaPeriod(DashaPeriod):
    """Antardasha period information"""
    maha_planet: str

class PratyantarDashaPeriod(AntarDashaPeriod):
    """Pratyantardasha period information"""
    antar_planet: str

class MahaDashaResponse(BaseModel):
    """Mahadasha response"""
    mahadasha: List[DashaPeriod]

class AntarDashaResponse(BaseModel):
    """Antardasha response"""
    antardasha: List[Dict[str, Any]]

class PratyantarDashaResponse(BaseModel):
    """Pratyantardasha response"""
    pratyantardasha: List[Dict[str, Any]]

class DivisionalChartResponse(BaseModel):
    """Divisional chart response"""
    ascendant: AscendantInfo
    planets: List[PlanetInfo]

class YogaInfo(BaseModel):
    """Yoga information"""
    name: str
    description: str
    planets_involved: List[str]
    houses_involved: List[int]
    strength: float
    results: str

class TransitInfo(BaseModel):
    """Transit information"""
    planet: str
    birth_position: Dict[str, Any]
    current_position: Dict[str, Any]
    house_from_birth_moon: int
    house_from_birth_ascendant: int

class TransitAspectInfo(BaseModel):
    """Transit aspect information"""
    transit_planet: str
    natal_planet: str
    aspect_type: str
    angle: float
    orb: float
    is_exact: bool
    is_applying: bool
    description: str

class SpecialTransitInfo(BaseModel):
    """Special transit information"""
    type: str
    planet: str
    description: str
    start_date: str
    end_date: str

# All response models for specific endpoints should inherit from BaseResponse
class PlanetsResponse(BaseResponse):
    """Response model for planets endpoint"""
    planets: List[PlanetInfo] = Field(..., description="List of planetary positions")

class AscendantResponse(BaseResponse):
    """Response model for ascendant endpoint"""
    ascendant: AscendantInfo = Field(..., description="Ascendant information")

class DashaResponse(BaseResponse):
    """Response model for dasha periods endpoint"""
    mahadasha: List[DashaPeriod] = Field(..., description="List of mahadasha periods")

class NakshatraResponse(BaseResponse):
    """Response model for nakshatra information endpoint"""
    moon_nakshatra: Dict[str, Any] = Field(..., description="Moon's nakshatra information")
    nakshatras: List[Dict[str, Any]] = Field(..., description="All planets' nakshatra information") 