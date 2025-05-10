"""
Planetary positions calculation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from api.models.request import HoroscopeRequest
from api.models.response import PlanetInfo, PlanetsResponse
from api.services import calculation
from typing import Dict, List, Any
from datetime import datetime

router = APIRouter(prefix="/v1/api/horoscope", tags=["planets"])

@router.post("/planets", response_model=PlanetsResponse)
async def get_planets(request: HoroscopeRequest):
    """
    Calculate planetary positions based on birth details
    
    **PREFERRED METHOD**: Provide only the `place` field
    ```json
    {
      "birth_date": "1990-01-01",
      "birth_time": "12:30:00",
      "place": "Chennai, India", 
      "ayanamsa": "lahiri"
    }
    ```
    
    **ALTERNATIVE METHOD**: Provide all location fields manually
    ```json
    {
      "birth_date": "1990-01-01",
      "birth_time": "12:30:00",
      "latitude": 13.0827,
      "longitude": 80.2707,
      "timezone_offset": 5.5,
      "ayanamsa": "lahiri"
    }
    ```
    
    The place-based input method is strongly recommended as it simplifies the API usage
    and ensures consistent coordinate and timezone determination.
    """
    try:
        # Calculate the ascendant
        ascendant = calculation.calculate_ascendant(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        
        # Calculate the planetary positions
        planets = calculation.calculate_planets(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        
        # Calculate houses
        houses = calculation.calculate_houses(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        
        # Validate D1 chart calculations for consistency
        calculation.validate_d1_chart(ascendant, planets, houses)
        
        # Prepare the response with standardized format
        response = PlanetsResponse(
            status="success",
            version="1.0",
            generated_at=datetime.utcnow().isoformat(),
            request_params={
                "birth_date": request.birth_date,
                "birth_time": request.birth_time,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "timezone_offset": request.timezone_offset,
                "ayanamsa": request.ayanamsa,
                "place": request.place
            },
            planets=planets
        )
        
        return response
    except Exception as e:
        # Log the error
        import logging
        logger = logging.getLogger("jai-api")
        logger.error(f"Error calculating planetary positions: {str(e)}")
        
        # Raise a proper HTTP exception
        raise HTTPException(
            status_code=500, 
            detail={
                "error_code": "CALCULATION_ERROR",
                "error_message": f"Error calculating planetary positions: {str(e)}",
                "details": {
                    "request": {
                        "birth_date": request.birth_date,
                        "birth_time": request.birth_time,
                        "latitude": request.latitude,
                        "longitude": request.longitude
                    }
                }
            }
        )
 