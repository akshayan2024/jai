"""
Divisional chart API endpoint.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List

from ...models import BirthDataRequest, DivisionalChartResponse
from ...services import ascendant_service, natal_chart_service, divisional_chart_service
from ...utils.validators import validate_birth_data
from ...utils.converters import convert_to_julian_day, get_ayanamsa_code
from ...utils.logger import get_logger
from ...utils.custom_exceptions import ValidationError, CalculationError, MappingNotFoundError
from ...constants.divisional_mappings import DIVISIONAL_MAPPINGS

logger = get_logger(__name__)

router = APIRouter(tags=["Divisional Chart"])

@router.post("/divisional-chart", response_model=DivisionalChartResponse)
async def get_divisional_chart(
    request: BirthDataRequest, 
    charts: str = Query("D1,D9", description="Comma-separated list of divisional charts to calculate")
):
    """
    Calculate divisional charts based on birth data.
    
    - **birth_date**: Date of birth in YYYY-MM-DD format
    - **birth_time**: Time of birth in HH:MM:SS format (24h)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Time zone offset from UTC in hours
    - **ayanamsa**: Ayanamsa method (lahiri, raman, krishnamurti)
    - **charts**: Comma-separated list of divisional charts (e.g., "D1,D9,D10")
    
    Returns the requested divisional charts.
    """
    try:
        # Validate input
        validate_birth_data(request)
        
        # Parse requested charts
        chart_list = [c.strip().upper() for c in charts.split(",")]
        
        # Validate chart names
        for chart in chart_list:
            if not chart.startswith("D") or not chart[1:].isdigit():
                raise ValidationError(f"Invalid chart name: {chart}. Must be in format 'D1', 'D9', etc.")
                
            chart_num = int(chart[1:])
            if chart_num < 1 or chart_num > 60:
                raise ValidationError(f"Invalid chart number: {chart}. Must be between D1 and D60.")
        
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
        
        # Calculate natal chart (D1)
        natal_positions = natal_chart_service.calculate_natal_chart(
            julian_day,
            ascendant["ascendant_sign"],
            ayanamsa_code
        )
        
        # Calculate requested divisional charts
        divisional_charts = {}
        
        for chart in chart_list:
            chart_num = int(chart[1:])
            
            # For D1, just use the natal chart
            if chart_num == 1:
                divisional_charts[chart] = natal_positions
                continue
                
            try:
                # Calculate divisional chart
                divisional_positions = divisional_chart_service.calculate_divisional_chart(
                    natal_positions,
                    chart_num,
                    ascendant["ascendant_sign"]
                )
                
                divisional_charts[chart] = divisional_positions
                
            except MappingNotFoundError as e:
                raise HTTPException(
                    status_code=500,
                    detail=str(e)
                )
        
        # Construct response
        response = {
            "ascendant": ascendant,
            "divisional_charts": divisional_charts
        }
        
        return DivisionalChartResponse(**response)
        
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
        logger.error(f"Unexpected error calculating divisional charts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during calculation"
        )

@router.get("/divisional-chart/supported")
async def get_supported_charts():
    """
    Get list of supported divisional charts.
    
    Returns a list of supported divisional chart names.
    """
    supported_charts = list(DIVISIONAL_MAPPINGS.keys())
    return {"supported_charts": supported_charts} 