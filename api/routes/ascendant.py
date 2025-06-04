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
    
    **Request Format**:
    ```json
    {
      "birth_date": "1990-01-01",
      "birth_time": "12:30:00",
      "place": "Chennai, India",
      "ayanamsa": "lahiri"
    }
    ```
    
    The API will automatically determine the coordinates and timezone from the provided place name.
    """
    try:
        # Calculate the ascendant
        logger.info(f"Calculating ascendant for {request.birth_date} {request.birth_time} in {request.place}")
        logger.debug(f"Using coordinates: {request.latitude}, {request.longitude}, timezone: {request.timezone_offset}")
        
        try:
            ascendant = calculation.calculate_ascendant(
                birth_date=request.birth_date,
                birth_time=request.birth_time,
                latitude=request.latitude,
                longitude=request.longitude,
                timezone_offset=request.timezone_offset,
                ayanamsa=request.ayanamsa
            )
        except Exception as e:
            logger.error(f"Error in ascendant calculation: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail={
                    "error_code": "CALCULATION_ERROR",
                    "error_message": "Failed to calculate ascendant. Please check your input parameters.",
                    "details": str(e)
                }
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
        # For validation errors, return 422 with details
        if isinstance(e, ValueError):
            status_code = 422
            error_code = "VALIDATION_ERROR"
        else:
            status_code = 500
            error_code = "INTERNAL_SERVER_ERROR"
            
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "error_message": str(e),
                "details": {
                    "request": {
                        "birth_date": request.birth_date,
                        "birth_time": request.birth_time,
                        "place": request.place,
                        "ayanamsa": request.ayanamsa
                    }
                }
            }
        ) 