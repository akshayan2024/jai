"""
API routes for planetary aspect calculations.
"""

from fastapi import APIRouter, Query, Path, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional

from ...services.natal_chart_service import calculate_natal_chart, NatalChartParams
from ...services.aspect_service import calculate_aspects, calculate_aspects_for_chart
from ...constants.ayanamsa import AYANAMSA_LAHIRI
from ...utils.custom_exceptions import CalculationError
from ...utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/aspect",
    tags=["aspect"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Calculation error"}
    }
)

class PlanetInput(BaseModel):
    """Request model for a planet position."""
    planet: str = Field(..., description="Planet name")
    longitude: float = Field(..., description="Longitude in degrees (0-360)")
    house: int = Field(..., description="House position (1-12)")


class PlanetListInput(BaseModel):
    """Request model for a list of planet positions."""
    planets: List[PlanetInput] = Field(..., description="List of planets with their positions")


class AspectResponse(BaseModel):
    """Response model for a planetary aspect."""
    source_planet: str = Field(..., description="Source planet casting the aspect")
    target_planet: str = Field(..., description="Target planet receiving the aspect")
    aspect_type: int = Field(..., description="Aspect type in houses (e.g., 7 for 7th aspect)")
    strength: int = Field(..., description="Aspect strength percentage (0-100)")
    is_exact: bool = Field(..., description="Whether the aspect is exact (within 1 degree)")


@router.post("/calculate", response_model=List[AspectResponse], summary="Calculate aspects between planets")
async def calculate_planet_aspects(input_data: PlanetListInput):
    """
    Calculate aspects between a list of planets.
    
    - **planets**: List of planets with their positions
    
    Returns a list of active aspects with details about source, target, type, and strength.
    """
    try:
        logger.info(f"Calculating aspects for {len(input_data.planets)} planets")
        
        # Convert the input model to a list of dicts
        planets = [planet.dict() for planet in input_data.planets]
        
        # Calculate the aspects
        result = calculate_aspects(planets)
        
        logger.info(f"Aspect calculation completed with {len(result)} aspects found")
        return result
    except CalculationError as e:
        logger.error(f"Aspect calculation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in aspect calculation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        )


@router.post("/chart", response_model=Dict[str, Any], summary="Calculate aspects for birth chart")
async def calculate_chart_aspects(params: NatalChartParams):
    """
    Calculate aspects for all planets in a birth chart.
    
    - **birth_date**: Date of birth (YYYY-MM-DD)
    - **birth_time**: Time of birth (HH:MM:SS)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Timezone offset in hours (-12 to +14)
    - **ayanamsa**: Ayanamsa system (lahiri, krishnamurti, raman)
    
    Returns the birth chart data with added aspects.
    """
    try:
        logger.info(f"Calculating aspects for birth chart: {params}")
        
        # Calculate the natal chart first
        natal_chart = calculate_natal_chart(
            birth_date=params.birth_date,
            birth_time=params.birth_time,
            latitude=params.latitude,
            longitude=params.longitude,
            timezone_offset=params.timezone_offset,
            ayanamsa=params.ayanamsa or AYANAMSA_LAHIRI
        )
        
        # Calculate aspects and add to chart data
        result = calculate_aspects_for_chart(natal_chart)
        
        logger.info(f"Chart aspect calculation completed")
        return result
    except CalculationError as e:
        logger.error(f"Chart aspect calculation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in chart aspect calculation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        ) 