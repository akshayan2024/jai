"""
Horoscope calculation endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from api.utils.input_validation import (
    CalculationInput,
    ValidationError,
    validate_date_range,
    validate_extreme_latitude
)
from api.services import calculation

router = APIRouter(prefix="/v1/api/horoscope", tags=["horoscope"])

class HoroscopeRequest(BaseModel):
    """Request model for horoscope calculations."""
    date: datetime
    latitude: float
    longitude: float
    house_system: str = 'W'  # Default to Whole Sign
    ayanamsa: int = 1  # Default to Lahiri

class HoroscopeResponse(BaseModel):
    """Response model for horoscope calculations."""
    ascendant: float
    mc: float
    armc: float
    vertex: float
    equatorial_ascendant: float
    house_cusps: List[float]
    planets: List[dict]

@router.post("/calculate", response_model=HoroscopeResponse)
async def calculate_horoscope(request: HoroscopeRequest):
    """
    Calculate a complete horoscope for the given date, time, and location.
    
    Args:
        request: HoroscopeRequest containing date, location, and calculation parameters
        
    Returns:
        HoroscopeResponse containing calculated positions
        
    Raises:
        HTTPException: If calculation fails or input is invalid
    """
    try:
        # Validate input using our validation system
        calc_input = CalculationInput(
            date=request.date,
            latitude=request.latitude,
            longitude=request.longitude,
            house_system=request.house_system,
            ayanamsa=request.ayanamsa
        )
        
        # Validate extreme latitude
        validate_extreme_latitude(request.latitude)
        
        # Use calculation.py functions
        ascendant = calculation.calculate_ascendant(
            birth_date=calc_input.date.strftime("%Y-%m-%d"),
            birth_time=calc_input.date.strftime("%H:%M:%S"),
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            timezone_offset=0,  # Adjust as needed
            ayanamsa="lahiri"  # Adjust as needed
        )
        planets = calculation.calculate_planets(
            birth_date=calc_input.date.strftime("%Y-%m-%d"),
            birth_time=calc_input.date.strftime("%H:%M:%S"),
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            timezone_offset=0,  # Adjust as needed
            ayanamsa="lahiri"  # Adjust as needed
        )
        houses = calculation.calculate_houses(
            birth_date=calc_input.date.strftime("%Y-%m-%d"),
            birth_time=calc_input.date.strftime("%H:%M:%S"),
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            timezone_offset=0,  # Adjust as needed
            ayanamsa="lahiri"  # Adjust as needed
        )
        # Compose the response
        return HoroscopeResponse(
            ascendant=ascendant.longitude,
            mc=0.0,  # Placeholder, add calculation if needed
            armc=0.0,  # Placeholder
            vertex=0.0,  # Placeholder
            equatorial_ascendant=0.0,  # Placeholder
            house_cusps=[h.longitude for h in houses],
            planets=[p.dict() for p in planets]
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/transits")
async def calculate_transits(
    request: HoroscopeRequest,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Calculate planetary transits for a given period.
    """
    try:
        # Validate input using our validation system
        calc_input = CalculationInput(
            date=request.date,
            latitude=request.latitude,
            longitude=request.longitude,
            house_system=request.house_system,
            ayanamsa=request.ayanamsa
        )
        # Validate date range
        if start_date and end_date:
            validate_date_range(start_date, end_date)
        # TODO: Implement canonical transit calculation using calculation.py
        raise HTTPException(status_code=501, detail="Transit calculation not yet implemented with canonical logic.")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@router.post("/progressions")
async def calculate_progressions(
    request: HoroscopeRequest,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Calculate secondary progressions for a given period.
    """
    try:
        # Validate input using our validation system
        calc_input = CalculationInput(
            date=request.date,
            latitude=request.latitude,
            longitude=request.longitude,
            house_system=request.house_system,
            ayanamsa=request.ayanamsa
        )
        # Validate date range
        if start_date and end_date:
            validate_date_range(start_date, end_date)
        # TODO: Implement canonical progression calculation using calculation.py
        raise HTTPException(status_code=501, detail="Progression calculation not yet implemented with canonical logic.")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}") 