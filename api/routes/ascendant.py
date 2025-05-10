"""
Ascendant calculation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from api.models.request import HoroscopeRequest
from api.models.response import AscendantInfo, AscendantResponse
from api.services import calculation
from typing import Dict, Any
from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger("jai-api.routes.ascendant")

router = APIRouter(prefix="/v1/api/horoscope", tags=["ascendant"])

@router.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: HoroscopeRequest):
    """
    Calculate the ascendant (lagna) based on birth details
    
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
        logger.info(f"Calculating ascendant for {request.birth_date} {request.birth_time} at {request.latitude}, {request.longitude}")
        
        ascendant = calculation.calculate_ascendant(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone_offset=request.timezone_offset,
            ayanamsa=request.ayanamsa
        )
        
        # Prepare the standardized response
        response = AscendantResponse(
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
            ascendant=ascendant
        )
        
        return response
    except Exception as e:
        # Log the error
        logger.error(f"Error calculating ascendant: {str(e)}", exc_info=True)
        
        # Raise a proper HTTP exception
        raise HTTPException(
            status_code=500, 
            detail={
                "error_code": "ASCENDANT_CALCULATION_ERROR",
                "error_message": f"Error calculating ascendant: {str(e)}",
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