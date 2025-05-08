"""
Ascendant calculation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from api.models.request import HoroscopeRequest
from api.models.response import AscendantInfo
from api.services import calculation
from typing import Dict, Any

router = APIRouter(prefix="/v1/api/horoscope", tags=["ascendant"])

@router.post("/ascendant", response_model=Dict[str, AscendantInfo])
async def get_ascendant(request: HoroscopeRequest):
    """
    Calculate the ascendant (lagna) based on birth details
    
    - **birth_date**: Date of birth (YYYY-MM-DD)
    - **birth_time**: Time of birth (HH:MM:SS)
    - **latitude**: Latitude of birth place
    - **longitude**: Longitude of birth place
    - **timezone_offset**: Timezone offset in hours
    - **ayanamsa**: Ayanamsa system (lahiri, raman, etc.)
    """
    try:
        # This would be implemented in the calculation service
        ascendant = calculation.calculate_ascendant(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        return {"ascendant": ascendant}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating ascendant: {str(e)}") 