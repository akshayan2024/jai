"""
Divisional chart service module for calculating all divisional charts.
"""

import math
from typing import Dict, Any, List

from ..utils.logger import get_logger
from ..utils.custom_exceptions import CalculationError, MappingNotFoundError
from ..constants import get_constant
from ..constants.divisional_mappings import DIVISIONAL_MAPPINGS

logger = get_logger(__name__)

def calculate_divisional_chart(natal_positions: List[Dict[str, Any]], n: int, ascendant_sign: int) -> List[Dict[str, Any]]:
    """
    Calculate divisional chart positions for all planets.
    
    Args:
        natal_positions (list): List of planet positions in D1 chart
        n (int): Divisional chart number (e.g. 9 for D9)
        ascendant_sign (int): Ascendant sign index (1-12)
        
    Returns:
        list: List of planet positions in the divisional chart
    """
    try:
        logger.debug(f"Calculating D{n} chart")
        
        # Get required constants
        zodiac_signs = get_constant('zodiac_signs')
        
        # Get divisional mapping
        chart_name = f"D{n}"
        mapping = DIVISIONAL_MAPPINGS.get(chart_name)
        
        if not mapping:
            error_msg = f"Divisional mapping for {chart_name} is not implemented"
            logger.error(error_msg)
            raise MappingNotFoundError(chart_name)
        
        # Calculate divisional positions
        divisional_positions = []
        
        for planet_data in natal_positions:
            planet_name = planet_data["planet"]
            longitude = planet_data["longitude"]
            is_retrograde = planet_data["is_retrograde"]
            natal_sign = planet_data["sign_index"]
            
            # Calculate division within the sign
            longitude_in_sign = longitude % 30
            division_size = 30 / n
            division = math.floor(longitude_in_sign / division_size) + 1
            
            # Map to divisional sign
            try:
                divisional_sign = mapping[natal_sign][division]
            except (KeyError, TypeError):
                error_msg = f"Invalid mapping for {chart_name}, sign {natal_sign}, division {division}"
                logger.error(error_msg)
                raise CalculationError(error_msg)
            
            # Get divisional sign name
            divisional_sign_name = zodiac_signs[divisional_sign]["name"]
            
            # Calculate house in divisional chart (Whole Sign system)
            divisional_house = ((divisional_sign - ascendant_sign) % 12) + 1
            
            # Add to result
            divisional_positions.append({
                "planet": planet_name,
                "divisional_sign_index": divisional_sign,
                "divisional_sign_name": divisional_sign_name,
                "divisional_house": divisional_house,
                "is_retrograde": is_retrograde  # Retrograde status stays the same as in D1
            })
        
        logger.debug(f"D{n} chart calculation completed")
        return divisional_positions
    
    except MappingNotFoundError:
        # Re-raise mapping errors
        raise
    except Exception as e:
        logger.error(f"Error calculating D{n} chart: {str(e)}")
        raise CalculationError(f"Failed to calculate D{n} chart: {str(e)}")

def get_divisional_span(n: int) -> float:
    """
    Calculate the span of each division in a divisional chart.
    
    Args:
        n (int): Divisional chart number
        
    Returns:
        float: Span of each division in degrees
    """
    return 30.0 / n

def map_to_divisional_sign(sign: int, division: int, mapping: Dict) -> int:
    """
    Map a sign and division to the corresponding divisional sign.
    
    Args:
        sign (int): Original sign index (1-12)
        division (int): Division number within sign (1-based)
        mapping (dict): Divisional mapping dictionary
        
    Returns:
        int: Divisional sign index (1-12)
    """
    try:
        return mapping[sign][division]
    except KeyError:
        raise CalculationError(f"Invalid mapping for sign {sign}, division {division}")

def is_divisional_chart_supported(chart_name: str) -> bool:
    """
    Check if a divisional chart is supported by the system.
    
    Args:
        chart_name (str): Chart name (e.g. 'D9')
        
    Returns:
        bool: True if supported, False otherwise
    """
    return chart_name in DIVISIONAL_MAPPINGS 