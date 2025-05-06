"""
Service module for nakshatra (lunar mansion) calculations.
"""

from typing import Dict, Any, List

from ..utils.logger import get_logger
from ..constants.nakshatras import (
    get_nakshatra_index, 
    get_nakshatra_name, 
    get_nakshatra_lord, 
    get_nakshatra_pada,
    get_degrees_in_nakshatra,
    NAKSHATRA_SPAN,
    PADA_SPAN,
    NAKSHATRA_STARTING_LORDS,
    VIMSHOTTARI_SEQUENCE,
    DASHA_YEARS,
    TOTAL_DASHA_YEARS
)
from ..utils.custom_exceptions import CalculationError

logger = get_logger(__name__)

def calculate_nakshatra(longitude: float) -> Dict[str, Any]:
    """
    Calculate nakshatra details for a given longitude.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        Dict[str, Any]: Nakshatra details including index, name, lord, pada,
                       and degrees traversed
    """
    try:
        # Calculate nakshatra index (1-27)
        nakshatra_index = get_nakshatra_index(longitude)
        
        # Get nakshatra name
        nakshatra_name = get_nakshatra_name(nakshatra_index)
        
        # Get ruling planet of the nakshatra
        nakshatra_lord = get_nakshatra_lord(nakshatra_index)
        
        # Calculate pada (quarter) within nakshatra (1-4)
        pada = get_nakshatra_pada(longitude)
        
        # Calculate degrees traversed within nakshatra (0-13.3333)
        degrees_in_nakshatra = get_degrees_in_nakshatra(longitude)
        
        # Calculate percentage traversed within nakshatra (0-100)
        percentage_traversed = (degrees_in_nakshatra / NAKSHATRA_SPAN) * 100
        
        # Calculate percentage traversed within pada (0-100)
        position_in_pada = degrees_in_nakshatra % PADA_SPAN
        percentage_in_pada = (position_in_pada / PADA_SPAN) * 100
        
        return {
            "nakshatra_index": nakshatra_index,
            "nakshatra_name": nakshatra_name,
            "nakshatra_lord": nakshatra_lord,
            "pada": pada,
            "degrees_in_nakshatra": degrees_in_nakshatra,
            "percentage_traversed": percentage_traversed,
            "percentage_in_pada": percentage_in_pada
        }
    except Exception as e:
        logger.error(f"Error calculating nakshatra: {str(e)}")
        raise CalculationError(f"Nakshatra calculation failed: {str(e)}")

def calculate_nakshatra_balance(longitude: float) -> float:
    """
    Calculate the remaining balance of the nakshatra at birth.
    Used for Vimshottari dasha calculations.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        float: Remaining balance as a decimal (0-1)
    """
    try:
        # Calculate degrees traversed within nakshatra (0-13.3333)
        degrees_in_nakshatra = get_degrees_in_nakshatra(longitude)
        
        # Calculate remaining balance as decimal (0-1)
        # 1.0 = just entered nakshatra, 0.0 = about to leave nakshatra
        remaining_balance = 1.0 - (degrees_in_nakshatra / NAKSHATRA_SPAN)
        
        return remaining_balance
    except Exception as e:
        logger.error(f"Error calculating nakshatra balance: {str(e)}")
        raise CalculationError(f"Nakshatra balance calculation failed: {str(e)}")

def get_dasha_sequence(nakshatra_index: int) -> List[str]:
    """
    Get the Vimshottari dasha sequence starting from the lord of the birth nakshatra.
    
    Args:
        nakshatra_index (int): Nakshatra index (1-27)
        
    Returns:
        List[str]: Ordered list of mahadasha lords
    """
    try:
        # Get the starting lord based on birth nakshatra
        starting_lord = NAKSHATRA_STARTING_LORDS[nakshatra_index]
        
        # Find the index of the starting lord in the vimshottari sequence
        start_idx = VIMSHOTTARI_SEQUENCE.index(starting_lord)
        
        # Create the ordered sequence starting from the birth nakshatra lord
        return VIMSHOTTARI_SEQUENCE[start_idx:] + VIMSHOTTARI_SEQUENCE[:start_idx]
    except Exception as e:
        logger.error(f"Error getting dasha sequence: {str(e)}")
        raise CalculationError(f"Dasha sequence calculation failed: {str(e)}")

def calculate_all_planet_nakshatras(planet_positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate nakshatra details for all planets in a chart.
    
    Args:
        planet_positions (List[Dict[str, Any]]): List of planet positions with longitudes
        
    Returns:
        List[Dict[str, Any]]: Planet positions with added nakshatra information
    """
    try:
        result = []
        
        for planet in planet_positions:
            # Get the planet's longitude
            longitude = planet.get("longitude", 0.0)
            
            # Calculate nakshatra details
            nakshatra_info = calculate_nakshatra(longitude)
            
            # Create a new planet dict with nakshatra information
            planet_with_nakshatra = {
                **planet,
                "nakshatra": nakshatra_info
            }
            
            result.append(planet_with_nakshatra)
            
        return result
    except Exception as e:
        logger.error(f"Error calculating all planet nakshatras: {str(e)}")
        raise CalculationError(f"Planet nakshatra calculation failed: {str(e)}") 