"""
Ascendant service module for ascendant and house calculations.
"""

import math
from typing import Dict, Any, List

from ..utils.logger import get_logger
from ..utils.custom_exceptions import CalculationError
from ..constants import get_constant
from .ephemeris_service import swe
from ..constants.ayanamsa import AYANAMSA_LAHIRI

logger = get_logger(__name__)

def calculate_ascendant(julian_day: float, latitude: float, longitude: float, ayanamsa=AYANAMSA_LAHIRI) -> Dict[str, Any]:
    """
    Calculate ascendant degree and sign.
    
    Args:
        julian_day (float): Julian day
        latitude (float): Birth latitude
        longitude (float): Birth longitude
        ayanamsa (int): Ayanamsa to use
        
    Returns:
        dict: Containing ascendant degree and sign index
    """
    try:
        logger.debug(f"Calculating ascendant: JD={julian_day}, lat={latitude}, lon={longitude}")
        
        # Set ayanamsa
        swe.set_sid_mode(ayanamsa)
        
        # Calculate houses using whole sign system
        houses_cusps, ascmc = swe.houses_ex(julian_day, latitude, longitude, b'W')
        
        # Extract ascendant degree
        ascendant_degree = ascmc[0]
        
        # Map to sign (1-12)
        ascendant_sign = math.floor(ascendant_degree / 30) + 1
        
        # Get sign name
        zodiac_signs = get_constant('zodiac_signs')
        ascendant_sign_name = zodiac_signs[ascendant_sign]["name"]
        
        logger.debug(f"Ascendant calculated: degree={ascendant_degree}, sign={ascendant_sign_name}")
        
        return {
            "ascendant_degree": ascendant_degree,
            "ascendant_sign": ascendant_sign,
            "ascendant_sign_name": ascendant_sign_name
        }
    except Exception as e:
        logger.error(f"Error calculating ascendant: {str(e)}")
        raise CalculationError(f"Failed to calculate ascendant: {str(e)}")

def get_houses(ascendant_sign: int) -> List[int]:
    """
    Get houses starting from ascendant sign, using Whole Sign house system.
    
    Args:
        ascendant_sign (int): Ascendant sign index (1-12)
        
    Returns:
        list: House to sign mapping, where index is house number (1-based)
    """
    try:
        # In Whole Sign system, the ascendant sign becomes the 1st house,
        # and subsequent signs follow in zodiacal order
        houses = [0]  # 0-index placeholder (houses are 1-based)
        
        for house in range(1, 13):
            sign = ((ascendant_sign - 1 + house - 1) % 12) + 1
            houses.append(sign)
        
        return houses
    except Exception as e:
        logger.error(f"Error calculating houses: {str(e)}")
        raise CalculationError(f"Failed to calculate houses: {str(e)}") 