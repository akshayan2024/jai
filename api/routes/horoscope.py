"""
Horoscope calculation endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from api.services.astrological_calculations import AstrologicalCalculator
from api.utils.input_validation import (
    CalculationInput,
    ValidationError,
    validate_date_range,
    validate_extreme_latitude
)

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
        
        # Create calculator instance
        calculator = AstrologicalCalculator()
        
        # Calculate horoscope
        result = calculator.calculate_horoscope(
            date=calc_input.date,
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            house_system=calc_input.house_system,
            ayanamsa=calc_input.ayanamsa
        )
        
        return HoroscopeResponse(**result)
        
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
    
    Args:
        request: HoroscopeRequest containing birth data
        start_date: Start date for transit calculations
        end_date: End date for transit calculations
        
    Returns:
        List of transit events
        
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
        
        # Validate date range
        if start_date and end_date:
            validate_date_range(start_date, end_date)
        
        # Create calculator instance
        calculator = AstrologicalCalculator()
        
        # Calculate transits
        result = calculator.calculate_transits(
            birth_date=calc_input.date,
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            start_date=start_date or calc_input.date,
            end_date=end_date or calc_input.date,
            house_system=calc_input.house_system,
            ayanamsa=calc_input.ayanamsa
        )
        
        return result
        
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
    
    Args:
        request: HoroscopeRequest containing birth data
        start_date: Start date for progression calculations
        end_date: End date for progression calculations
        
    Returns:
        List of progression events
        
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
        
        # Validate date range
        if start_date and end_date:
            validate_date_range(start_date, end_date)
        
        # Create calculator instance
        calculator = AstrologicalCalculator()
        
        # Calculate progressions
        result = calculator.calculate_progressions(
            birth_date=calc_input.date,
            latitude=calc_input.latitude,
            longitude=calc_input.longitude,
            start_date=start_date or calc_input.date,
            end_date=end_date or calc_input.date,
            house_system=calc_input.house_system,
            ayanamsa=calc_input.ayanamsa
        )
        
        return result
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}") 