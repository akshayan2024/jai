from typing import Optional
from pydantic import BaseModel

class BirthDataRequest(BaseModel):
    """Birth data input model for astrological calculations"""
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone_offset: float
    ayanamsa: Optional[str] = "lahiri"
    
    class Config:
        schema_extra = {
            "example": {
                "birth_date": "1990-01-01",
                "birth_time": "12:00:00",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "timezone_offset": 5.5,
                "ayanamsa": "lahiri"
            }
        } 