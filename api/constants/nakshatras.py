"""
Constants and utilities related to nakshatras (lunar mansions) in Vedic astrology.
"""

from typing import Dict, List, Tuple, TypedDict

class NakshatraData(TypedDict):
    """Type definition for nakshatra data structure."""
    name: str
    lord: str
    start_deg: float
    end_deg: float
    pada_length: float

# Nakshatra spans 13°20' (13.3333°) each
NAKSHATRA_SPAN = 13.3333

# Total number of nakshatras
NAKSHATRA_COUNT = 27

# Number of padas per nakshatra
PADA_COUNT = 4

# Each pada spans 3°20' (3.3333°)
PADA_SPAN = NAKSHATRA_SPAN / PADA_COUNT

# Nakshatra names (1-based index)
NAKSHATRA_NAMES = [
    "Ashwini",      # 1
    "Bharani",      # 2
    "Krittika",     # 3
    "Rohini",       # 4
    "Mrigashira",   # 5
    "Ardra",        # 6
    "Punarvasu",    # 7
    "Pushya",       # 8
    "Ashlesha",     # 9
    "Magha",        # 10
    "Purva Phalguni", # 11
    "Uttara Phalguni", # 12
    "Hasta",        # 13
    "Chitra",       # 14
    "Swati",        # 15
    "Vishakha",     # 16
    "Anuradha",     # 17
    "Jyeshtha",     # 18
    "Mula",         # 19
    "Purva Ashadha", # 20
    "Uttara Ashadha", # 21
    "Shravana",     # 22
    "Dhanishta",    # 23
    "Shatabhisha",  # 24
    "Purva Bhadrapada", # 25
    "Uttara Bhadrapada", # 26
    "Revati"        # 27
]

# Nakshatra lords (planets that rule each nakshatra)
# 1-based indexing, 0th element is a placeholder
NAKSHATRA_LORDS = [
    "",            # 0 (placeholder)
    "ketu",        # 1 - Ashwini
    "venus",       # 2 - Bharani
    "sun",         # 3 - Krittika
    "moon",        # 4 - Rohini
    "mars",        # 5 - Mrigashira
    "rahu",        # 6 - Ardra
    "jupiter",     # 7 - Punarvasu
    "saturn",      # 8 - Pushya
    "mercury",     # 9 - Ashlesha
    "ketu",        # 10 - Magha
    "venus",       # 11 - Purva Phalguni
    "sun",         # 12 - Uttara Phalguni
    "moon",        # 13 - Hasta
    "mars",        # 14 - Chitra
    "rahu",        # 15 - Swati
    "jupiter",     # 16 - Vishakha
    "saturn",      # 17 - Anuradha
    "mercury",     # 18 - Jyeshtha
    "ketu",        # 19 - Mula
    "venus",       # 20 - Purva Ashadha
    "sun",         # 21 - Uttara Ashadha
    "moon",        # 22 - Shravana
    "mars",        # 23 - Dhanishta
    "rahu",        # 24 - Shatabhisha
    "jupiter",     # 25 - Purva Bhadrapada
    "saturn",      # 26 - Uttara Bhadrapada
    "mercury"      # 27 - Revati
]

# Nakshatra data dictionary
NAKSHATRAS: Dict[int, NakshatraData] = {
    i + 1: {
        'name': name,
        'lord': NAKSHATRA_LORDS[i + 1],
        'start_deg': i * NAKSHATRA_SPAN,
        'end_deg': (i + 1) * NAKSHATRA_SPAN,
        'pada_length': PADA_SPAN
    }
    for i, name in enumerate(NAKSHATRA_NAMES)
}

# Nakshatra names (1-based index), derived from NAKSHATRAS for consistency
NAKSHATRA_NAMES_DERIVED = [nakshatra['name'] for nakshatra in NAKSHATRAS.values()]

def get_nakshatra_index(longitude: float) -> int:
    """
    Calculate nakshatra index (1-27) from longitude.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        int: Nakshatra index (1-27)
        
    Raises:
        ValueError: If longitude is not a valid number
    """
    try:
        # Adjust longitude to ensure it's within 0-360
        longitude = float(longitude) % 360.0
        
        # Calculate nakshatra index (1-based)
        nakshatra = int(longitude / NAKSHATRA_SPAN) + 1
        
        # Handle edge case where longitude is exactly 360.0
        if nakshatra > NAKSHATRA_COUNT:
            return NAKSHATRA_COUNT
            
        return nakshatra
    except (TypeError, ValueError) as e:
        raise ValueError(
            f"Invalid longitude value: {longitude}. Must be a number between 0 and 360."
        ) from e

def get_nakshatra_name(nakshatra_index: int) -> str:
    """
    Get nakshatra name from index.
    
    Args:
        nakshatra_index (int): Nakshatra index (1-27)
        
    Returns:
        str: Nakshatra name
        
    Raises:
        ValueError: If nakshatra_index is out of range (1-27)
    """
    try:
        return NAKSHATRAS[nakshatra_index]['name']
    except KeyError as e:
        raise ValueError(
            f"Invalid nakshatra index: {nakshatra_index}. "
            f"Must be between 1 and {NAKSHATRA_COUNT}."
        ) from e

def get_nakshatra_lord(nakshatra_index: int) -> str:
    """
    Get ruling planet (lord) of a nakshatra.
    
    Args:
        nakshatra_index (int): Nakshatra index (1-27)
        
    Returns:
        str: Planet name
        
    Raises:
        ValueError: If nakshatra_index is out of range (1-27)
    """
    try:
        return NAKSHATRAS[nakshatra_index]['lord']
    except KeyError as e:
        raise ValueError(
            f"Invalid nakshatra index: {nakshatra_index}. "
            f"Must be between 1 and {NAKSHATRA_COUNT}."
        ) from e

def get_nakshatra_pada(longitude: float) -> int:
    """
    Calculate pada (quarter) within nakshatra.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        int: Pada index (1-4)
    """
    # Get degrees within the nakshatra
    degrees_in_nakshatra = get_degrees_in_nakshatra(longitude)
    
    # Calculate pada (1-4)
    pada = int(degrees_in_nakshatra / PADA_SPAN) + 1
    
    # Handle edge case where longitude is exactly 360°
    if pada > 4:
        return 4
        
    return pada

def get_degrees_in_nakshatra(longitude: float) -> float:
    """
    Calculate degrees traversed within nakshatra.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        float: Degrees traversed in nakshatra (0-13.3333)
    """
    # Normalize longitude to 0-360
    longitude = longitude % 360
    
    # Calculate degrees within the current nakshatra
    degrees_in_nakshatra = longitude % NAKSHATRA_SPAN
    
    return degrees_in_nakshatra

# Alias for backward compatibility
get_nakshatra_from_longitude = get_nakshatra_index 