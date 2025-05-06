"""
Response models for the API.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AscendantResponse(BaseModel):
    """Ascendant calculation response"""
    ascendant_degree: float
    ascendant_sign: int
    ascendant_sign_name: str

class PlanetPositionResponse(BaseModel):
    """Planet position in a chart"""
    planet: str
    longitude: float
    sign_index: int
    sign_name: str
    house: int
    is_retrograde: bool

class NatalChartResponse(BaseModel):
    """Full natal chart response"""
    ascendant: AscendantResponse
    planets: List[PlanetPositionResponse]

class DivisionalPlanetResponse(BaseModel):
    """Planet position in a divisional chart"""
    planet: str
    divisional_sign_index: int
    divisional_sign_name: str
    divisional_house: int
    is_retrograde: bool

class DivisionalChartResponse(BaseModel):
    """Divisional charts response"""
    ascendant: AscendantResponse
    divisional_charts: Dict[str, List[DivisionalPlanetResponse]]

class DashaPeriod(BaseModel):
    """Dasha period information"""
    planet: str
    start_date: str
    end_date: str
    years: float

class PratyantarDashaPeriod(BaseModel):
    """Pratyantardasha (sub-sub-period) information"""
    planet: str
    start_date: str
    end_date: str
    days: int

class AntarDashaPeriod(BaseModel):
    """Antardasha period information"""
    planet: str
    start_date: str
    end_date: str
    months: float
    pratyantardashas: List[PratyantarDashaPeriod] = []

class MahadashaPeriod(BaseModel):
    """Mahadasha period with sub-periods"""
    planet: str
    start_date: str
    end_date: str
    years: float
    antardashas: List[AntarDashaPeriod] = []

class MoonPositionResponse(BaseModel):
    """Moon position information"""
    longitude: float
    nakshatra_index: int
    nakshatra_name: str
    nakshatra_lord: str

class MahadashaResponse(BaseModel):
    """Vimshottari mahadasha periods response"""
    moon: MoonPositionResponse
    vimshottari_mahadasha: List[MahadashaPeriod] 