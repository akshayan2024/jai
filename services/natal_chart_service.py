"""
Natal chart service module for D1 chart calculations.
"""

import math
from typing import Dict, Any, List

from ..utils.logger import get_logger
from ..utils.custom_exceptions import CalculationError
from ..constants import get_constant
from .ephemeris_service import get_planet_position
from .ascendant_service import get_houses
from ..constants.ayanamsa import AYANAMSA_LAHIRI

logger = get_logger(__name__)

def calculate_natal_chart(julian_day: float, ascendant_sign: int, ayanamsa=AYANAMSA_LAHIRI) -> List[Dict[str, Any]]:
    """
    Calculate the natal chart (D1) for all planets.
    
    Args:
        julian_day (float): Julian day for the calculation
        ascendant_sign (int): Ascendant sign index (1-12)
        ayanamsa (int): Ayanamsa to use
        
    Returns:
        list: List of planet positions with sign and house placements
    """
    try:
        logger.debug(f"Calculating natal chart: JD={julian_day}, ascendant={ascendant_sign}")
        
        # Get planet and zodiac data
        planets = get_constant('planets')
        zodiac_signs = get_constant('zodiac_signs')
        
        # Get house placements (Whole Sign system)
        houses = get_houses(ascendant_sign)
        
        # Calculate planet positions
        planet_positions = []
        
        for planet_idx in range(1, 10):  # 1-9 for the 9 planets
            planet = planets[planet_idx]
            planet_name = planet["name"]
            swe_code = planet["swe_code"]
            
            # Special case for Ketu (South Node)
            if planet_idx == 9:  # Ketu
                # Ketu is 180° from Rahu
                # Get Rahu position first
                rahu_position = next(
                    (p for p in planet_positions if p["planet"] == "Rahu"),
                    None
                )
                
                if rahu_position:
                    # Adjust Rahu's longitude by 180°
                    longitude = (rahu_position["longitude"] + 180) % 360
                    is_retrograde = rahu_position["is_retrograde"]
                else:
                    # Fallback if Rahu position not found
                    rahu = get_planet_position(julian_day, 10, ayanamsa)
                    longitude = (rahu["longitude"] + 180) % 360
                    is_retrograde = rahu["speed"] < 0
            else:
                # Get planet position
                position = get_planet_position(julian_day, swe_code, ayanamsa)
                longitude = position["longitude"]
                is_retrograde = position["speed"] < 0
            
            # Calculate sign
            sign_idx = math.floor(longitude / 30) + 1
            sign_name = zodiac_signs[sign_idx]["name"]
            
            # Find house
            house = houses.index(sign_idx) if sign_idx in houses else 0
            
            # Add to result
            planet_positions.append({
                "planet": planet_name,
                "longitude": longitude,
                "sign_index": sign_idx,
                "sign_name": sign_name,
                "house": house,
                "is_retrograde": is_retrograde
            })
        
        logger.debug(f"Natal chart calculation completed with {len(planet_positions)} planets")
        return planet_positions
    
    except Exception as e:
        logger.error(f"Error calculating natal chart: {str(e)}")
        raise CalculationError(f"Failed to calculate natal chart: {str(e)}")

def calculate_planet_house(planet_sign: int, ascendant_sign: int) -> int:
    """
    Determine house placement based on planet sign and ascendant sign.
    Uses Whole Sign house system.
    
    Args:
        planet_sign (int): Planet's sign index (1-12)
        ascendant_sign (int): Ascendant sign index (1-12)
        
    Returns:
        int: House number (1-12)
    """
    # In Whole Sign system, calculate house by zodiacal order from ascendant
    house = ((planet_sign - ascendant_sign) % 12) + 1
    return house 