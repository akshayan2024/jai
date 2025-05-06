"""
Constants related to nakshatras (lunar mansions) in Vedic astrology.
"""

from typing import Dict, List, Tuple

# Nakshatra spans 13°20' (13.3333°) each
NAKSHATRA_SPAN = 13.3333

# Total number of nakshatras
NAKSHATRA_COUNT = 27

# Number of padas per nakshatra
PADA_COUNT = 4

# Each pada spans 3°20' (3.3333°)
PADA_SPAN = NAKSHATRA_SPAN / PADA_COUNT

# Nakshatra names
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

# Dasha years for each nakshatra lord (for Vimshottari dasha)
DASHA_YEARS = {
    "sun": 6,
    "moon": 10,
    "mars": 7,
    "rahu": 18,
    "jupiter": 16,
    "saturn": 19,
    "mercury": 17,
    "ketu": 7,
    "venus": 20
}

# Total Vimshottari dasha cycle
TOTAL_DASHA_YEARS = 120

# Mapping of nakshatras to their starting lord for Vimshottari dasha
# This determines which mahadasha sequence starts based on birth nakshatra
NAKSHATRA_STARTING_LORDS = [
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

# The sequence of planets for the Vimshottari dasha
VIMSHOTTARI_SEQUENCE = [
    "ketu",
    "venus", 
    "sun", 
    "moon", 
    "mars", 
    "rahu", 
    "jupiter", 
    "saturn", 
    "mercury"
]

def get_nakshatra_index(longitude: float) -> int:
    """
    Calculate nakshatra index (1-27) from longitude.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        int: Nakshatra index (1-27)
    """
    # Adjust longitude to ensure it's within 0-360
    longitude = longitude % 360
    
    # Calculate nakshatra index (1-based)
    nakshatra = int(longitude / NAKSHATRA_SPAN) + 1
    
    return nakshatra

def get_nakshatra_name(nakshatra_index: int) -> str:
    """
    Get nakshatra name from index.
    
    Args:
        nakshatra_index (int): Nakshatra index (1-27)
        
    Returns:
        str: Nakshatra name
    """
    if nakshatra_index < 1 or nakshatra_index > 27:
        raise ValueError(f"Invalid nakshatra index: {nakshatra_index}. Must be between 1 and 27.")
        
    return NAKSHATRA_NAMES[nakshatra_index - 1]

def get_nakshatra_lord(nakshatra_index: int) -> str:
    """
    Get ruling planet (lord) of a nakshatra.
    
    Args:
        nakshatra_index (int): Nakshatra index (1-27)
        
    Returns:
        str: Planet name
    """
    if nakshatra_index < 1 or nakshatra_index > 27:
        raise ValueError(f"Invalid nakshatra index: {nakshatra_index}. Must be between 1 and 27.")
        
    return NAKSHATRA_LORDS[nakshatra_index]

def get_nakshatra_pada(longitude: float) -> int:
    """
    Calculate pada (quarter) within nakshatra.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        int: Pada index (1-4)
    """
    # Adjust longitude to ensure it's within 0-360
    longitude = longitude % 360
    
    # Calculate position within nakshatra
    position_in_nakshatra = longitude % NAKSHATRA_SPAN
    
    # Calculate pada (1-4)
    pada = int(position_in_nakshatra / PADA_SPAN) + 1
    
    return pada

def get_degrees_in_nakshatra(longitude: float) -> float:
    """
    Calculate degrees traversed within nakshatra.
    
    Args:
        longitude (float): Zodiacal longitude (0-360)
        
    Returns:
        float: Degrees traversed in nakshatra (0-13.3333)
    """
    # Adjust longitude to ensure it's within 0-360
    longitude = longitude % 360
    
    # Calculate position within nakshatra
    position_in_nakshatra = longitude % NAKSHATRA_SPAN
    
    return position_in_nakshatra 