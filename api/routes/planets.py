"""
Planetary positions calculation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from api.models.request import HoroscopeRequest
from api.models.response import PlanetInfo
from api.services import calculation
from typing import Dict, List, Any

router = APIRouter(prefix="/v1/api/horoscope", tags=["planets"])

@router.post("/planets", response_model=Dict[str, List[PlanetInfo]])
async def get_planets(request: HoroscopeRequest):
    """
    Calculate planetary positions based on birth details
    
    - **birth_date**: Date of birth (YYYY-MM-DD)
    - **birth_time**: Time of birth (HH:MM:SS)
    - **latitude**: Latitude of birth place
    - **longitude**: Longitude of birth place
    - **timezone_offset**: Timezone offset in hours
    - **ayanamsa**: Ayanamsa system (lahiri, raman, etc.)
    """
    try:
        # This would be implemented in the calculation service
        planets = calculation.calculate_planets(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        return {"planets": planets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating planetary positions: {str(e)}")
 