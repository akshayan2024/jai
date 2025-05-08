"""
Request data models for JAI API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date

class HoroscopeRequest(BaseModel):
    """Base request model for horoscope data"""
    birth_date: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Time of birth (HH:MM:SS)")
    latitude: float = Field(..., description="Latitude of birth place")
    longitude: float = Field(..., description="Longitude of birth place")
    timezone_offset: float = Field(..., description="Timezone offset in hours")
    ayanamsa: str = Field("lahiri", description="Ayanamsa system (lahiri, raman, etc.)")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("birth_date must be in YYYY-MM-DD format")
            
    @validator('birth_time')
    def validate_birth_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            try:
                # Try without seconds
                datetime.strptime(v, "%H:%M")
                return v
            except ValueError:
                raise ValueError("birth_time must be in HH:MM:SS or HH:MM format")

class TransitRequest(HoroscopeRequest):
    """Request model for transit calculations"""
    transit_date: str = Field(..., description="Transit date (YYYY-MM-DD)")
    
    @validator('transit_date')
    def validate_transit_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("transit_date must be in YYYY-MM-DD format") 