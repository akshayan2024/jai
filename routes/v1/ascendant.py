"""
Ascendant API endpoint.
"""

from fastapi import APIRouter, HTTPException, Depends

from ...models import BirthDataRequest, AscendantResponse
from ...services import ascendant_service
from ...utils.validators import validate_birth_data
from ...utils.converters import convert_to_julian_day, get_ayanamsa_code
from ...utils.logger import get_logger
from ...utils.custom_exceptions import ValidationError, CalculationError

logger = get_logger(__name__)

router = APIRouter(tags=["Ascendant"])

@router.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: BirthDataRequest):
    """
    Calculate ascendant sign and degree based on birth data.
    
    - **birth_date**: Date of birth in YYYY-MM-DD format
    - **birth_time**: Time of birth in HH:MM:SS format (24h)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Time zone offset from UTC in hours
    - **ayanamsa**: Ayanamsa method (lahiri, raman, krishnamurti)
    
    Returns ascendant degree and zodiac sign.
    """
    try:
        # Validate input
        validate_birth_data(request)
        
        # Convert to Julian Day
        julian_day = convert_to_julian_day(
            request.birth_date,
            request.birth_time,
            request.timezone_offset
        )
        
        # Get ayanamsa code
        ayanamsa_code = get_ayanamsa_code(request.ayanamsa)
        
        # Calculate ascendant
        ascendant = ascendant_service.calculate_ascendant(
            julian_day,
            request.latitude,
            request.longitude,
            ayanamsa_code
        )
        
        return AscendantResponse(**ascendant)
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except CalculationError as e:
        logger.error(f"Calculation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error calculating ascendant: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during calculation"
        ) 