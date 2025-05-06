"""
Natal chart API endpoint.
"""

from fastapi import APIRouter, HTTPException

from ...models import BirthDataRequest, NatalChartResponse
from ...services import ascendant_service, natal_chart_service
from ...utils.validators import validate_birth_data
from ...utils.converters import convert_to_julian_day, get_ayanamsa_code
from ...utils.logger import get_logger
from ...utils.custom_exceptions import ValidationError, CalculationError

logger = get_logger(__name__)

router = APIRouter(tags=["Natal Chart"])

@router.post("/natal-chart", response_model=NatalChartResponse)
async def get_natal_chart(request: BirthDataRequest):
    """
    Calculate natal chart (D1) based on birth data.
    
    - **birth_date**: Date of birth in YYYY-MM-DD format
    - **birth_time**: Time of birth in HH:MM:SS format (24h)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Time zone offset from UTC in hours
    - **ayanamsa**: Ayanamsa method (lahiri, raman, krishnamurti)
    
    Returns ascendant and planet positions in D1 chart.
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
        
        # Calculate natal chart
        planets = natal_chart_service.calculate_natal_chart(
            julian_day,
            ascendant["ascendant_sign"],
            ayanamsa_code
        )
        
        # Construct response
        response = {
            "ascendant": ascendant,
            "planets": planets
        }
        
        return NatalChartResponse(**response)
        
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
        logger.error(f"Unexpected error calculating natal chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during calculation"
        ) 