"""
API routes for nakshatra (lunar mansion) calculations.
"""

from fastapi import APIRouter, Query, Path, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from ...services.natal_chart_service import calculate_natal_chart, NatalChartParams
from ...services.nakshatra_service import calculate_nakshatra, calculate_all_planet_nakshatras
from ...constants.ayanamsa import AYANAMSA_LAHIRI
from ...utils.custom_exceptions import CalculationError
from ...utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/nakshatra",
    tags=["nakshatra"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Calculation error"}
    }
)

class LongitudeInput(BaseModel):
    """Request model for a simple longitude calculation."""
    longitude: float = Field(..., description="Longitude in degrees (0-360)")


class NakshatraResponse(BaseModel):
    """Response model for nakshatra details."""
    nakshatra_index: int = Field(..., description="Nakshatra index (1-27)")
    nakshatra_name: str = Field(..., description="Nakshatra name")
    nakshatra_lord: str = Field(..., description="Ruling planet of the nakshatra")
    pada: int = Field(..., description="Pada (quarter) within nakshatra (1-4)")
    degrees_in_nakshatra: float = Field(..., description="Degrees traversed within nakshatra (0-13.3333)")
    percentage_traversed: float = Field(..., description="Percentage traversed within nakshatra (0-100)")
    percentage_in_pada: float = Field(..., description="Percentage traversed within pada (0-100)")


class PlanetNakshatraResponse(BaseModel):
    """Response model for planet with nakshatra details."""
    planet: str = Field(..., description="Planet name")
    longitude: float = Field(..., description="Longitude in degrees (0-360)")
    nakshatra: NakshatraResponse = Field(..., description="Nakshatra details")


@router.post("/from-longitude", response_model=NakshatraResponse, summary="Calculate nakshatra from longitude")
async def get_nakshatra_from_longitude(input_data: LongitudeInput):
    """
    Calculate nakshatra details for a given longitude.
    
    - **longitude**: Zodiacal longitude in degrees (0-360)
    
    Returns nakshatra details including index, name, lord, pada, and more.
    """
    try:
        logger.info(f"Calculating nakshatra for longitude: {input_data.longitude}")
        
        result = calculate_nakshatra(input_data.longitude)
        
        logger.info(f"Nakshatra calculation completed: {result['nakshatra_name']}")
        return result
    except CalculationError as e:
        logger.error(f"Nakshatra calculation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in nakshatra calculation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        )


@router.post("/all-planets", response_model=List[PlanetNakshatraResponse], summary="Calculate nakshatras for all planets")
async def get_all_planet_nakshatras(params: NatalChartParams):
    """
    Calculate nakshatra details for all planets in a birth chart.
    
    - **birth_date**: Date of birth (YYYY-MM-DD)
    - **birth_time**: Time of birth (HH:MM:SS)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Timezone offset in hours (-12 to +14)
    - **ayanamsa**: Ayanamsa system (lahiri, krishnamurti, raman)
    
    Returns a list of planets with their nakshatra details.
    """
    try:
        logger.info(f"Calculating nakshatras for all planets: {params}")
        
        # Calculate the natal chart first
        natal_chart = calculate_natal_chart(
            birth_date=params.birth_date,
            birth_time=params.birth_time,
            latitude=params.latitude,
            longitude=params.longitude,
            timezone_offset=params.timezone_offset,
            ayanamsa=params.ayanamsa or AYANAMSA_LAHIRI
        )
        
        # Extract just the planets from the natal chart
        planets = natal_chart.get("planets", [])
        
        # Calculate nakshatra details for all planets
        result = calculate_all_planet_nakshatras(planets)
        
        logger.info(f"All planet nakshatra calculation completed")
        return result
    except CalculationError as e:
        logger.error(f"All planet nakshatra calculation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in all planet nakshatra calculation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        ) 