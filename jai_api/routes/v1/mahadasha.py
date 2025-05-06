"""
Mahadasha API endpoint.
"""

from fastapi import APIRouter, HTTPException, Query

from ...models import BirthDataRequest, MahadashaResponse
from ...services import mahadasha_service
from ...utils.validators import validate_birth_data
from ...utils.converters import convert_to_julian_day, get_ayanamsa_code
from ...utils.logger import get_logger
from ...utils.custom_exceptions import ValidationError, CalculationError

logger = get_logger(__name__)

router = APIRouter(tags=["Mahadasha"])

@router.post("/mahadasha", response_model=MahadashaResponse)
async def get_mahadasha(
    request: BirthDataRequest,
    levels: str = Query("mahadasha", description="Comma-separated list of dasha levels to calculate")
):
    """
    Calculate Vimshottari Mahadasha periods based on birth data.
    
    - **birth_date**: Date of birth in YYYY-MM-DD format
    - **birth_time**: Time of birth in HH:MM:SS format (24h)
    - **latitude**: Birth latitude (-90 to +90)
    - **longitude**: Birth longitude (-180 to +180)
    - **timezone_offset**: Time zone offset from UTC in hours
    - **ayanamsa**: Ayanamsa method (lahiri, raman, krishnamurti)
    - **levels**: Comma-separated list of dasha levels (mahadasha, antardasha, pratyantardasha)
    
    Returns mahadasha periods with start and end dates.
    """
    try:
        # Validate input
        validate_birth_data(request)
        
        # Parse requested levels
        level_list = [level.strip().lower() for level in levels.split(",")]
        
        # Validate levels
        valid_levels = ["mahadasha", "antardasha", "pratyantardasha"]
        for level in level_list:
            if level not in valid_levels:
                raise ValidationError(f"Invalid dasha level: {level}. Must be one of {valid_levels}")
        
        # Convert to Julian Day
        julian_day = convert_to_julian_day(
            request.birth_date,
            request.birth_time,
            request.timezone_offset
        )
        
        # Get ayanamsa code
        ayanamsa_code = get_ayanamsa_code(request.ayanamsa)
        
        # Calculate mahadasha
        mahadasha_result = mahadasha_service.calculate_mahadasha(
            julian_day,
            request.birth_date,
            ayanamsa_code
        )
        
        # Calculate antardashas if requested
        if "antardasha" in level_list or "pratyantardasha" in level_list:
            mahadashas_with_antardashas = []
            
            for mahadasha in mahadasha_result["mahadashas"]:
                mahadasha_with_antardashas = mahadasha_service.calculate_antardasha(mahadasha)
                mahadashas_with_antardashas.append(mahadasha_with_antardashas)
            
            mahadasha_result["mahadashas"] = mahadashas_with_antardashas
        
        # Calculate pratyantardashas if requested
        if "pratyantardasha" in level_list:
            mahadashas_with_pratyantardashas = []
            
            for mahadasha in mahadasha_result["mahadashas"]:
                antardashas_with_pratyantardashas = []
                
                for antardasha in mahadasha["antardashas"]:
                    antardasha_with_pratyantardashas = mahadasha_service.calculate_pratyantardasha(antardasha)
                    antardashas_with_pratyantardashas.append(antardasha_with_pratyantardashas)
                
                # Update the mahadasha with the new antardashas containing pratyantardashas
                mahadasha_updated = mahadasha.copy()
                mahadasha_updated["antardashas"] = antardashas_with_pratyantardashas
                mahadashas_with_pratyantardashas.append(mahadasha_updated)
            
            mahadasha_result["mahadashas"] = mahadashas_with_pratyantardashas
            
            logger.info("Pratyantardasha calculations completed")
        
        # Construct response
        response = {
            "moon": mahadasha_result["moon"],
            "vimshottari_mahadasha": mahadasha_result["mahadashas"]
        }
        
        return MahadashaResponse(**response)
        
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
        logger.error(f"Unexpected error calculating mahadasha: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during calculation"
        )

@router.get("/mahadasha/supported-levels")
async def get_supported_levels():
    """
    Get list of supported dasha levels.
    
    Returns a list of supported dasha level names.
    """
    return {
        "supported_levels": ["mahadasha", "antardasha", "pratyantardasha"]
    } 