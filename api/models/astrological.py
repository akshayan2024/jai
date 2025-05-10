from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

class Sign(Enum):
    ARIES = 1
    TAURUS = 2
    GEMINI = 3
    CANCER = 4
    LEO = 5
    VIRGO = 6
    LIBRA = 7
    SCORPIO = 8
    SAGITTARIUS = 9
    CAPRICORN = 10
    AQUARIUS = 11
    PISCES = 12

class Planet(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"

class PlanetPosition(BaseModel):
    planet: Planet
    sign: Sign
    degree: float = Field(..., ge=0, lt=30)
    is_retrograde: bool = False
    nakshatra: Optional[str] = None
    pada: Optional[int] = Field(None, ge=1, le=4)

class HousePosition(BaseModel):
    house_number: int = Field(..., ge=1, le=12)
    sign: Sign
    degree: float = Field(..., ge=0, lt=30)
    planets: List[PlanetPosition] = []

class BirthData(BaseModel):
    date: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str

class Yoga(BaseModel):
    name: str
    planets: List[Planet]
    description: str
    strength: float = Field(..., ge=0, le=1)

class DashaPeriod(BaseModel):
    planet: Planet
    start_date: datetime
    end_date: datetime
    sub_periods: Optional[List['DashaPeriod']] = None

class TransitPosition(BaseModel):
    planet: Planet
    current_sign: Sign
    current_degree: float
    is_retrograde: bool
    next_sign_change: Optional[datetime] = None

class TransitResponse(BaseModel):
    date: datetime
    positions: List[TransitPosition]

class Aspect(BaseModel):
    planet1: Planet
    planet2: Planet
    aspect_type: str
    distance: float = Field(..., ge=0, lt=360)
    strength: float = Field(..., ge=0, le=1)

class HoroscopeResponse(BaseModel):
    birth_data: BirthData
    ascendant: HousePosition
    planets: List[PlanetPosition]
    houses: List[HousePosition]
    yogas: List[Yoga] = []
    dashas: Optional[List[DashaPeriod]] = None
    aspects: List[Aspect] = [] 