"""
Response data models for JAI API
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class PlanetInfo(BaseModel):
    """Planet position information"""
    name: str
    longitude: float
    latitude: float = 0.0
    house: int
    sign: str
    sign_id: int
    nakshatra: str
    nakshatra_id: int
    nakshatra_pada: int
    is_retrograde: bool
    degrees: float
    minutes: float
    seconds: float
    dignity: Optional[str] = None

class AscendantInfo(BaseModel):
    """Ascendant information"""
    sign: str
    sign_id: int
    degrees: float
    minutes: float
    seconds: float
    longitude: float
    nakshatra: str
    nakshatra_id: int
    nakshatra_pada: int

class HouseInfo(BaseModel):
    """House information"""
    house_number: int
    sign: str
    sign_id: int
    degrees: float
    minutes: float
    seconds: float
    longitude: float

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

class DashaPeriod(BaseModel):
    """Dasha period information"""
    planet: str
    start_date: str
    end_date: str
    duration: str

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