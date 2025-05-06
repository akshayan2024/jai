"""
Constants related to planetary aspects in Vedic astrology.
"""

from typing import Dict, List, Tuple

# Vedic aspects are different from Western aspects
# Each planet aspects certain houses from its position

# Dictionary of planets and the houses they aspect (relative to their position)
# All planets aspect the 7th house (180°) by default, so it's included for all
PLANET_ASPECTS = {
    "sun": [7],        # 7th house only
    "moon": [7],       # 7th house only
    "mars": [4, 7, 8], # 4th, 7th, and 8th houses
    "mercury": [7],    # 7th house only
    "jupiter": [5, 7, 9], # 5th, 7th, and 9th houses
    "venus": [7],      # 7th house only
    "saturn": [3, 7, 10], # 3rd, 7th, and 10th houses
    "rahu": [5, 7, 9], # 5th, 7th, and 9th houses (same as Jupiter)
    "ketu": [5, 7, 9]  # 5th, 7th, and 9th houses (same as Jupiter)
}

# Graha Drishti (Planetary Aspect) Strength
# Full strength (100%) for 7th house aspect, varied strengths for special aspects
ASPECT_STRENGTH = {
    "mars": {4: 75, 7: 100, 8: 75},
    "jupiter": {5: 75, 7: 100, 9: 75},
    "saturn": {3: 75, 7: 100, 10: 75},
    "rahu": {5: 75, 7: 100, 9: 75},
    "ketu": {5: 75, 7: 100, 9: 75}
}

# Default aspect strength for planets that only aspect the 7th house
DEFAULT_ASPECT_STRENGTH = {7: 100}

# Aspect orb (allowable deviation in degrees)
ASPECT_ORB = 6.0

def get_planet_aspects(planet: str) -> List[int]:
    """
    Get the houses aspected by a planet.
    
    Args:
        planet (str): Planet name
        
    Returns:
        List[int]: List of houses aspected by the planet
    """
    return PLANET_ASPECTS.get(planet.lower(), [7])

def get_aspect_strength(planet: str, house_position: int) -> int:
    """
    Get the strength of a planet's aspect on a house.
    
    Args:
        planet (str): Planet name
        house_position (int): House position relative to the planet (1-12)
        
    Returns:
        int: Aspect strength percentage (0-100)
    """
    planet_lower = planet.lower()
    
    # Check if the planet has special aspect strengths
    if planet_lower in ASPECT_STRENGTH:
        # Return the strength if the house is aspected, otherwise 0
        return ASPECT_STRENGTH[planet_lower].get(house_position, 0)
    else:
        # For planets that only aspect the 7th house
        return DEFAULT_ASPECT_STRENGTH.get(house_position, 0) 