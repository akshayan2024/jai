"""
Service module for yoga (planetary combination) detection and analysis.
"""

from typing import Dict, List, Any, Optional, Set

from ..utils.logger import get_logger
from ..constants.yogas import get_yoga_description, YOGA_DESCRIPTIONS
from ..constants.planets import PLANETS
from ..constants.zodiac import SIGNS
from ..utils.custom_exceptions import CalculationError

logger = get_logger(__name__)

def is_kendra(house: int) -> bool:
    """
    Check if a house is a kendra (quadrant house).
    Kendras are 1st, 4th, 7th, and 10th houses.
    
    Args:
        house (int): House position (1-12)
        
    Returns:
        bool: True if house is a kendra
    """
    return house in [1, 4, 7, 10]

def is_trikona(house: int) -> bool:
    """
    Check if a house is a trikona (trine house).
    Trikonas are 1st, 5th, and 9th houses.
    
    Args:
        house (int): House position (1-12)
        
    Returns:
        bool: True if house is a trikona
    """
    return house in [1, 5, 9]

def is_dusthana(house: int) -> bool:
    """
    Check if a house is a dusthana (difficult house).
    Dusthanas are 6th, 8th, and 12th houses.
    
    Args:
        house (int): House position (1-12)
        
    Returns:
        bool: True if house is a dusthana
    """
    return house in [6, 8, 12]

def is_own_sign(planet: Dict[str, Any]) -> bool:
    """
    Check if a planet is in its own sign.
    
    Args:
        planet (Dict[str, Any]): Planet data with sign and planet name
        
    Returns:
        bool: True if planet is in its own sign
    """
    planet_name = planet.get("planet", "").lower()
    sign = planet.get("sign", 0)
    
    # Define lordships (which planet rules which sign)
    sign_lords = {
        1: "mars",        # Aries
        2: "venus",       # Taurus
        3: "mercury",     # Gemini
        4: "moon",        # Cancer
        5: "sun",         # Leo
        6: "mercury",     # Virgo
        7: "venus",       # Libra
        8: "mars",        # Scorpio
        9: "jupiter",     # Sagittarius
        10: "saturn",     # Capricorn
        11: "saturn",     # Aquarius
        12: "jupiter"     # Pisces
    }
    
    return sign_lords.get(sign, "") == planet_name

def is_exalted(planet: Dict[str, Any]) -> bool:
    """
    Check if a planet is in its exaltation sign.
    
    Args:
        planet (Dict[str, Any]): Planet data with sign and planet name
        
    Returns:
        bool: True if planet is exalted
    """
    planet_name = planet.get("planet", "").lower()
    sign = planet.get("sign", 0)
    
    # Define exaltation signs
    exaltation_signs = {
        "sun": 1,        # Aries
        "moon": 2,       # Taurus
        "mars": 10,      # Capricorn
        "mercury": 6,    # Virgo
        "jupiter": 4,    # Cancer
        "venus": 12,     # Pisces
        "saturn": 7,     # Libra
        "rahu": 3,       # Gemini (some systems)
        "ketu": 9        # Sagittarius (some systems)
    }
    
    return exaltation_signs.get(planet_name, 0) == sign

def is_debilitated(planet: Dict[str, Any]) -> bool:
    """
    Check if a planet is in its debilitation sign.
    
    Args:
        planet (Dict[str, Any]): Planet data with sign and planet name
        
    Returns:
        bool: True if planet is debilitated
    """
    planet_name = planet.get("planet", "").lower()
    sign = planet.get("sign", 0)
    
    # Define debilitation signs (opposite of exaltation)
    debilitation_signs = {
        "sun": 7,        # Libra
        "moon": 8,       # Scorpio
        "mars": 4,       # Cancer
        "mercury": 12,   # Pisces
        "jupiter": 10,   # Capricorn
        "venus": 6,      # Virgo
        "saturn": 1,     # Aries
        "rahu": 9,       # Sagittarius (some systems)
        "ketu": 3        # Gemini (some systems)
    }
    
    return debilitation_signs.get(planet_name, 0) == sign

def get_house_lord(house: int, ascendant_sign: int) -> str:
    """
    Get the lord (ruling planet) of a house.
    
    Args:
        house (int): House number (1-12)
        ascendant_sign (int): Ascendant sign (1-12)
        
    Returns:
        str: Planet name that rules the house
    """
    # Calculate the sign of the house
    house_sign = ((ascendant_sign - 1 + house - 1) % 12) + 1
    
    # Define sign rulers
    sign_lords = {
        1: "mars",        # Aries
        2: "venus",       # Taurus
        3: "mercury",     # Gemini
        4: "moon",        # Cancer
        5: "sun",         # Leo
        6: "mercury",     # Virgo
        7: "venus",       # Libra
        8: "mars",        # Scorpio
        9: "jupiter",     # Sagittarius
        10: "saturn",     # Capricorn
        11: "saturn",     # Aquarius
        12: "jupiter"     # Pisces
    }
    
    return sign_lords.get(house_sign, "")

def find_planet_by_name(planets: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    """
    Find a planet in a list by its name.
    
    Args:
        planets (List[Dict[str, Any]]): List of planets
        name (str): Planet name to find
        
    Returns:
        Optional[Dict[str, Any]]: Planet data or None if not found
    """
    name_lower = name.lower()
    for planet in planets:
        if planet.get("planet", "").lower() == name_lower:
            return planet
    return None

def detect_pancha_mahapurusha_yogas(planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect Pancha Mahapurusha yogas in a chart.
    These yogas occur when Mars, Mercury, Jupiter, Venus, or Saturn is in its own sign or exaltation
    and in a kendra house (1, 4, 7, 10).
    
    Args:
        planets (List[Dict[str, Any]]): List of planets with positions
        
    Returns:
        List[Dict[str, Any]]: Detected yogas with details
    """
    yogas = []
    
    # Planet name to yoga name mapping
    mahapurusha_yogas = {
        "mars": "ruchaka_yoga",
        "mercury": "bhadra_yoga",
        "jupiter": "hamsa_yoga",
        "venus": "malavya_yoga",
        "saturn": "sasa_yoga"
    }
    
    for planet in planets:
        planet_name = planet.get("planet", "").lower()
        house = planet.get("house", 0)
        
        # Check if this planet forms a Mahapurusha yoga
        if planet_name in mahapurusha_yogas and is_kendra(house) and (is_own_sign(planet) or is_exalted(planet)):
            yoga_name = mahapurusha_yogas[planet_name]
            yoga_info = get_yoga_description(yoga_name)
            
            yogas.append({
                "yoga": yoga_name,
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": [planet_name],
                "strength": "Strong" if is_exalted(planet) else "Medium"
            })
    
    return yogas

def detect_raj_yogas(planets: List[Dict[str, Any]], ascendant_sign: int) -> List[Dict[str, Any]]:
    """
    Detect Raj (royal) yogas in a chart.
    
    Args:
        planets (List[Dict[str, Any]]): List of planets with positions
        ascendant_sign (int): The ascendant sign (1-12)
        
    Returns:
        List[Dict[str, Any]]: Detected yogas with details
    """
    yogas = []
    
    # Get planet positions by name for easier reference
    planet_dict = {planet.get("planet", "").lower(): planet for planet in planets}
    
    # Check for Gaja-Kesari Yoga (Jupiter in kendra from Moon)
    if "moon" in planet_dict and "jupiter" in planet_dict:
        moon = planet_dict["moon"]
        jupiter = planet_dict["jupiter"]
        
        moon_house = moon.get("house", 0)
        jupiter_house = jupiter.get("house", 0)
        
        # Calculate house distance
        house_diff = (jupiter_house - moon_house) % 12
        if house_diff == 0:
            house_diff = 12
        
        if house_diff in [1, 4, 7, 10]:
            yoga_info = get_yoga_description("gaja_kesari_yoga")
            yogas.append({
                "yoga": "gaja_kesari_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon", "jupiter"],
                "strength": "Strong" if is_exalted(jupiter) or is_own_sign(jupiter) else "Medium"
            })
    
    # Check for Budha-Aditya Yoga (Mercury and Sun in the same house)
    if "sun" in planet_dict and "mercury" in planet_dict:
        sun = planet_dict["sun"]
        mercury = planet_dict["mercury"]
        
        sun_house = sun.get("house", 0)
        mercury_house = mercury.get("house", 0)
        sun_longitude = sun.get("longitude", 0.0)
        mercury_longitude = mercury.get("longitude", 0.0)
        
        # Check if Mercury is not combust (too close to Sun)
        is_combust = abs(sun_longitude - mercury_longitude) < 8.0
        
        if sun_house == mercury_house and not is_combust:
            yoga_info = get_yoga_description("budha_aditya_yoga")
            yogas.append({
                "yoga": "budha_aditya_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["sun", "mercury"],
                "strength": "Strong" if is_kendra(sun_house) or is_trikona(sun_house) else "Medium"
            })
    
    # Check for Chandra-Mangala Yoga (Moon and Mars in the same house or aspecting)
    if "moon" in planet_dict and "mars" in planet_dict:
        moon = planet_dict["moon"]
        mars = planet_dict["mars"]
        
        moon_house = moon.get("house", 0)
        mars_house = mars.get("house", 0)
        
        # Check if in same house or Mars aspects Moon
        # Mars aspects 4th, 7th, and 8th houses from its position
        house_diff = (moon_house - mars_house) % 12
        if house_diff == 0:
            house_diff = 12
        
        if moon_house == mars_house or house_diff in [4, 7, 8]:
            yoga_info = get_yoga_description("chandra_mangala_yoga")
            yogas.append({
                "yoga": "chandra_mangala_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon", "mars"],
                "strength": "Strong" if is_exalted(moon) or is_exalted(mars) else "Medium"
            })
    
    return yogas

def detect_dhana_yogas(planets: List[Dict[str, Any]], ascendant_sign: int) -> List[Dict[str, Any]]:
    """
    Detect Dhana (wealth) yogas in a chart.
    
    Args:
        planets (List[Dict[str, Any]]): List of planets with positions
        ascendant_sign (int): The ascendant sign (1-12)
        
    Returns:
        List[Dict[str, Any]]: Detected yogas with details
    """
    yogas = []
    
    # Get planet positions by name for easier reference
    planet_dict = {planet.get("planet", "").lower(): planet for planet in planets}
    
    # Get the lord of the 2nd house (wealth)
    second_lord_name = get_house_lord(2, ascendant_sign)
    second_lord = planet_dict.get(second_lord_name)
    
    # Get the lord of the 9th house (luck, fortune)
    ninth_lord_name = get_house_lord(9, ascendant_sign)
    ninth_lord = planet_dict.get(ninth_lord_name)
    
    # Check for Dhana Yoga (2nd lord in kendra or trikona)
    if second_lord:
        second_lord_house = second_lord.get("house", 0)
        
        if is_kendra(second_lord_house) or is_trikona(second_lord_house):
            yoga_info = get_yoga_description("dhana_yoga")
            yogas.append({
                "yoga": "dhana_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": [second_lord_name],
                "strength": "Strong" if is_own_sign(second_lord) or is_exalted(second_lord) else "Medium"
            })
    
    # Check for Lakshmi Yoga (Venus in own sign or exalted, and 9th lord in kendra)
    if "venus" in planet_dict and ninth_lord:
        venus = planet_dict["venus"]
        ninth_lord_house = ninth_lord.get("house", 0)
        
        if (is_own_sign(venus) or is_exalted(venus)) and is_kendra(ninth_lord_house):
            yoga_info = get_yoga_description("lakshmi_yoga")
            yogas.append({
                "yoga": "lakshmi_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["venus", ninth_lord_name],
                "strength": "Strong"
            })
    
    return yogas

def detect_chandra_yogas(planets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect Moon-based (Chandra) yogas in a chart.
    
    Args:
        planets (List[Dict[str, Any]]): List of planets with positions
        
    Returns:
        List[Dict[str, Any]]: Detected yogas with details
    """
    yogas = []
    
    # Get planet positions by name for easier reference
    planet_dict = {planet.get("planet", "").lower(): planet for planet in planets}
    
    # Check for Moon-based yogas
    if "moon" in planet_dict:
        moon = planet_dict["moon"]
        moon_house = moon.get("house", 0)
        
        # Check for Adhi Yoga (Mercury, Venus, and Jupiter in 6th, 7th, and 8th from Moon)
        has_planet_in_6th = False
        has_planet_in_7th = False
        has_planet_in_8th = False
        
        for planet in planets:
            planet_name = planet.get("planet", "").lower()
            if planet_name not in ["mercury", "venus", "jupiter"]:
                continue
                
            planet_house = planet.get("house", 0)
            house_from_moon = ((planet_house - moon_house) % 12) + 1
            
            if house_from_moon == 6:
                has_planet_in_6th = True
            elif house_from_moon == 7:
                has_planet_in_7th = True
            elif house_from_moon == 8:
                has_planet_in_8th = True
        
        if has_planet_in_6th and has_planet_in_7th and has_planet_in_8th:
            yoga_info = get_yoga_description("adhi_yoga")
            yogas.append({
                "yoga": "adhi_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon", "mercury", "venus", "jupiter"],
                "strength": "Strong"
            })
        
        # Check for Sunapha Yoga (a planet other than Sun in 2nd from Moon)
        has_sunapha = False
        sunapha_planet = None
        
        for planet in planets:
            planet_name = planet.get("planet", "").lower()
            if planet_name == "sun":
                continue
                
            planet_house = planet.get("house", 0)
            house_from_moon = ((planet_house - moon_house) % 12) + 1
            
            if house_from_moon == 2:
                has_sunapha = True
                sunapha_planet = planet_name
                break
        
        if has_sunapha:
            yoga_info = get_yoga_description("sunapha_yoga")
            yogas.append({
                "yoga": "sunapha_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon", sunapha_planet],
                "strength": "Medium"
            })
        
        # Check for Anapha Yoga (a planet other than Sun in 12th from Moon)
        has_anapha = False
        anapha_planet = None
        
        for planet in planets:
            planet_name = planet.get("planet", "").lower()
            if planet_name == "sun":
                continue
                
            planet_house = planet.get("house", 0)
            house_from_moon = ((planet_house - moon_house) % 12) + 1
            
            if house_from_moon == 12:
                has_anapha = True
                anapha_planet = planet_name
                break
        
        if has_anapha:
            yoga_info = get_yoga_description("anapha_yoga")
            yogas.append({
                "yoga": "anapha_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon", anapha_planet],
                "strength": "Medium"
            })
        
        # Check for Kemadruma Yoga (no planets in 2nd and 12th from Moon)
        has_planet_in_2nd = False
        has_planet_in_12th = False
        
        for planet in planets:
            planet_name = planet.get("planet", "").lower()
            planet_house = planet.get("house", 0)
            house_from_moon = ((planet_house - moon_house) % 12) + 1
            
            if house_from_moon == 2:
                has_planet_in_2nd = True
            elif house_from_moon == 12:
                has_planet_in_12th = True
        
        if not has_planet_in_2nd and not has_planet_in_12th:
            yoga_info = get_yoga_description("kemadruma_yoga")
            yogas.append({
                "yoga": "kemadruma_yoga",
                "name": yoga_info["name"],
                "description": yoga_info["description"],
                "category": yoga_info["category"],
                "effect": yoga_info["effect"],
                "planets_involved": ["moon"],
                "strength": "Strong"
            })
    
    return yogas

def detect_all_yogas(chart_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect all yogas in a birth chart.
    
    Args:
        chart_data (Dict[str, Any]): Chart data with planets and ascendant
        
    Returns:
        List[Dict[str, Any]]: List of detected yogas with details
    """
    try:
        planets = chart_data.get("planets", [])
        ascendant_sign = chart_data.get("ascendant_sign", 1)
        
        all_yogas = []
        
        # Detect different types of yogas
        all_yogas.extend(detect_pancha_mahapurusha_yogas(planets))
        all_yogas.extend(detect_raj_yogas(planets, ascendant_sign))
        all_yogas.extend(detect_dhana_yogas(planets, ascendant_sign))
        all_yogas.extend(detect_chandra_yogas(planets))
        
        # Sort yogas by category for better organization
        all_yogas.sort(key=lambda yoga: yoga["category"])
        
        return all_yogas
    except Exception as e:
        logger.error(f"Error detecting yogas: {str(e)}")
        raise CalculationError(f"Yoga detection failed: {str(e)}")

def calculate_yogas_for_chart(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate all yogas for a chart and add them to the chart data.
    
    Args:
        chart_data (Dict[str, Any]): Chart data containing planets and ascendant
        
    Returns:
        Dict[str, Any]: Chart data with added yogas
    """
    try:
        # Detect all yogas
        yogas = detect_all_yogas(chart_data)
        
        # Add yogas to the chart data
        chart_data_with_yogas = {
            **chart_data,
            "yogas": yogas
        }
        
        return chart_data_with_yogas
    except Exception as e:
        logger.error(f"Error calculating chart yogas: {str(e)}")
        raise CalculationError(f"Chart yoga calculation failed: {str(e)}") 