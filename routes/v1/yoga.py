"""
API routes for yoga (planetary combination) calculations.
"""

from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from ...services.natal_chart_service import calculate_natal_chart, NatalChartParams
from ...services.yoga_service import calculate_yogas_for_chart, detect_all_yogas
from ...constants.ayanamsa import AYANAMSA_LAHIRI
from ...constants.yogas import get_yoga_description, get_yogas_by_category, YOGA_CATEGORIES
from ...utils.custom_exceptions import CalculationError
from ...utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/yoga",
    tags=["yoga"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid input"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Calculation error"}
    }
)

class YogaResponse(BaseModel):
    """Response model for a yoga (planetary combination)."""
    yoga: str = Field(..., description="Yoga identifier")
    name: str = Field(..., description="Yoga name")
    description: str = Field(..., description="Yoga description")
    category: str = Field(..., description="Yoga category")
    effect: str = Field(..., description="Effect of the yoga")
    planets_involved: List[str] = Field(..., description="Planets involved in the yoga")
    strength: str = Field(..., description="Strength of the yoga (Strong, Medium, Weak)")

class ChartInput(BaseModel):
    """Request model for a chart input."""
    planets: List[Dict[str, Any]] = Field(..., description="List of planets with positions")
    ascendant_sign: int = Field(..., description="Ascendant sign (1-12)")

@router.get("/categories", response_model=Dict[str, str], summary="Get available yoga categories")
async def get_yoga_categories():
    """
    Get a list of available yoga categories.
    
    Returns a dictionary mapping category IDs to category names.
    """
    return YOGA_CATEGORIES

@router.get("/list/{category}", response_model=Dict[str, Dict[str, Any]], summary="List yogas by category")
async def list_yogas_by_category(category: str = Path(..., description="Yoga category")):
    """
    Get a list of all yogas in a specific category.
    
    - **category**: The yoga category ID (e.g., dhana_yoga, raja_yoga)
    
    Returns a dictionary of yogas in the specified category with their descriptions and effects.
    """
    try:
        if category not in YOGA_CATEGORIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"code": 400, "message": f"Invalid category: {category}. Valid categories are: {', '.join(YOGA_CATEGORIES.keys())}"}}
            )
            
        yogas = get_yogas_by_category(category)
        
        if not yogas:
            logger.warning(f"No yogas found in category: {category}")
            return {}
            
        logger.info(f"Found {len(yogas)} yogas in category: {category}")
        return yogas
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error listing yogas by category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        )

@router.get("/info/{yoga_name}", response_model=Dict[str, Any], summary="Get yoga details")
async def get_yoga_info(yoga_name: str = Path(..., description="Yoga name")):
    """
    Get detailed information about a specific yoga.
    
    - **yoga_name**: The yoga identifier (e.g., gaja_kesari_yoga, budha_aditya_yoga)
    
    Returns detailed information about the yoga including description, category, and effects.
    """
    try:
        yoga_info = get_yoga_description(yoga_name)
        
        if yoga_info.get("category") == "unknown":
            logger.warning(f"Yoga not found: {yoga_name}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": {"code": 404, "message": f"Yoga not found: {yoga_name}"}}
            )
            
        logger.info(f"Retrieved info for yoga: {yoga_name}")
        return yoga_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting yoga info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        )

@router.post("/detect", response_model=List[YogaResponse], summary="Detect yogas in a chart")
async def detect_yogas(chart_data: ChartInput):
    """
    Detect yogas (planetary combinations) in a birth chart.
    
    - **planets**: List of planets with their positions
    - **ascendant_sign**: Ascendant sign (1-12)
    
    Returns a list of detected yogas with their details.
    """
    try:
        logger.info(f"Detecting yogas for chart with ascendant sign {chart_data.ascendant_sign}")
        
        # Convert the input model to a dict
        chart_dict = chart_data.dict()
        
        # Detect yogas
        yogas = detect_all_yogas(chart_dict)
        
        logger.info(f"Detected {len(yogas)} yogas in the chart")
        return yogas
    except CalculationError as e:
        logger.error(f"Yoga detection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in yoga detection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        )

@router.post("/chart", response_model=Dict[str, Any], summary="Calculate yogas for birth chart")
async def calculate_chart_yogas(params: NatalChartParams):
    """
    Calculate yogas for a birth chart.
    
    - **birth_date**: Date of birth (YYYY-MM-DD)
    - **birth_time**: Time of birth (HH:MM:SS)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Timezone offset in hours (-12 to +14)
    - **ayanamsa**: Ayanamsa system (lahiri, krishnamurti, raman)
    
    Returns the birth chart data with added yogas.
    """
    try:
        logger.info(f"Calculating yogas for birth chart: {params}")
        
        # Calculate the natal chart first
        natal_chart = calculate_natal_chart(
            birth_date=params.birth_date,
            birth_time=params.birth_time,
            latitude=params.latitude,
            longitude=params.longitude,
            timezone_offset=params.timezone_offset,
            ayanamsa=params.ayanamsa or AYANAMSA_LAHIRI
        )
        
        # Calculate yogas and add to chart data
        result = calculate_yogas_for_chart(natal_chart)
        
        logger.info(f"Chart yoga calculation completed with {len(result.get('yogas', []))} yogas")
        return result
    except CalculationError as e:
        logger.error(f"Chart yoga calculation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": str(e)}}
        )
    except Exception as e:
        logger.error(f"Unexpected error in chart yoga calculation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": 500, "message": f"Unexpected error: {str(e)}"}}
        ) 