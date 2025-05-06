"""
Service module for planetary aspect calculations.
"""

from typing import Dict, List, Any, Optional, Tuple

from ..utils.logger import get_logger
from ..constants.aspects import get_planet_aspects, get_aspect_strength, ASPECT_ORB
from ..constants.zodiac import SIGN_SPAN
from ..utils.custom_exceptions import CalculationError

logger = get_logger(__name__)

def calculate_angular_distance(longitude1: float, longitude2: float) -> float:
    """
    Calculate the angular distance between two zodiacal longitudes.
    
    Args:
        longitude1 (float): First longitude (0-360)
        longitude2 (float): Second longitude (0-360)
        
    Returns:
        float: Shortest angular distance in degrees (0-180)
    """
    # Normalize longitudes to ensure they're between 0-360
    lon1 = longitude1 % 360
    lon2 = longitude2 % 360
    
    # Calculate raw difference
    raw_diff = abs(lon1 - lon2)
    
    # Return the smaller arc between the two points
    return min(raw_diff, 360 - raw_diff)

def house_distance(house1: int, house2: int) -> int:
    """
    Calculate the distance between two houses in the zodiac wheel.
    
    Args:
        house1 (int): First house (1-12)
        house2 (int): Second house (1-12)
        
    Returns:
        int: Shortest house distance (0-6)
    """
    # Normalize to ensure houses are between 1-12
    h1 = ((house1 - 1) % 12) + 1
    h2 = ((house2 - 1) % 12) + 1
    
    # Calculate raw difference
    raw_diff = abs(h1 - h2)
    
    # Return the smaller arc between the two houses
    return min(raw_diff, 12 - raw_diff)

def is_in_aspect(planet_longitude: float, target_longitude: float, aspect_type: int, orb: float = ASPECT_ORB) -> bool:
    """
    Determine if a planet aspects a specific target longitude based on aspect type.
    
    Args:
        planet_longitude (float): Planet's longitude (0-360)
        target_longitude (float): Target longitude (0-360)
        aspect_type (int): Aspect type in houses (e.g., 7 for 7th aspect/opposition)
        orb (float): Allowable orb in degrees (default: ASPECT_ORB)
        
    Returns:
        bool: True if the aspect is active, False otherwise
    """
    # Convert aspect_type from houses to degrees
    aspect_degrees = (aspect_type - 1) * 30
    
    # Calculate expected aspect longitude
    expected_aspect_longitude = (planet_longitude + aspect_degrees) % 360
    
    # Calculate the distance between the expected aspect longitude and target longitude
    distance = calculate_angular_distance(expected_aspect_longitude, target_longitude)
    
    # Check if the distance is within the allowed orb
    return distance <= orb

def calculate_aspects(planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate aspects between all planets in a chart.
    
    Args:
        planets (List[Dict[str, Any]]): List of planet data including name and longitude
        
    Returns:
        List[Dict[str, Any]]: List of aspects with source planet, target planet, aspect type, and strength
    """
    try:
        aspects = []
        
        # Calculate aspects for each planet pair
        for i, source_planet in enumerate(planets):
            source_name = source_planet.get("planet", "")
            source_longitude = source_planet.get("longitude", 0.0)
            source_house = source_planet.get("house", 0)
            
            # Get the houses this planet aspects
            aspected_houses = get_planet_aspects(source_name)
            
            for j, target_planet in enumerate(planets):
                # Skip self-aspects
                if i == j:
                    continue
                    
                target_name = target_planet.get("planet", "")
                target_longitude = target_planet.get("longitude", 0.0)
                target_house = target_planet.get("house", 0)
                
                # Calculate the house distance from source to target
                house_diff = (target_house - source_house) % 12
                if house_diff == 0:
                    house_diff = 12
                
                # Check if this house difference is in the planet's aspect list
                if house_diff in aspected_houses:
                    # Calculate if the aspect is within orb
                    if is_in_aspect(source_longitude, target_longitude, house_diff):
                        # Get the strength of the aspect
                        strength = get_aspect_strength(source_name, house_diff)
                        
                        # Add to the aspects list
                        aspects.append({
                            "source_planet": source_name,
                            "target_planet": target_name,
                            "aspect_type": house_diff,
                            "strength": strength,
                            "is_exact": calculate_angular_distance(source_longitude + (house_diff - 1) * 30, target_longitude) < 1.0
                        })
        
        return aspects
    except Exception as e:
        logger.error(f"Error calculating aspects: {str(e)}")
        raise CalculationError(f"Aspect calculation failed: {str(e)}")

def calculate_aspects_for_chart(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate all planetary aspects for a chart and add them to the chart data.
    
    Args:
        chart_data (Dict[str, Any]): Chart data containing planets list
        
    Returns:
        Dict[str, Any]: Chart data with added aspects
    """
    try:
        # Extract planets from the chart
        planets = chart_data.get("planets", [])
        
        # Calculate aspects
        aspects = calculate_aspects(planets)
        
        # Add aspects to the chart data
        chart_data_with_aspects = {
            **chart_data,
            "aspects": aspects
        }
        
        return chart_data_with_aspects
    except Exception as e:
        logger.error(f"Error calculating chart aspects: {str(e)}")
        raise CalculationError(f"Chart aspect calculation failed: {str(e)}") 