"""
Astrological calculation service module using Swiss Ephemeris

Note on Indexing:
- Signs are 0-based in calculations (0-11) but displayed as 1-12 in the API
- Houses are 1-based (1-12) in both calculations and the API
- Nakshatras are 0-based (0-26) in calculations but displayed as 1-27 in the API
"""
from api.models.response import (
    AscendantInfo, 
    PlanetInfo, 
    HouseInfo, 
    AspectInfo, 
    DashaPeriod,
    YogaInfo,
    TransitInfo,
    TransitAspectInfo,
    SpecialTransitInfo
)
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import math
import os
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger("jai-api.calculation")

# TEMPORARY FIX: Always use the mock implementation to avoid ephemeris file dependency
logger.warning("Using mock Swiss Ephemeris implementation")
from api.services.mock_swisseph import *
import api.services.mock_swisseph as swe
logger.warning("Mock Swiss Ephemeris is only for development and testing!")

# Initialize Swiss Ephemeris
def initialize_ephemeris():
    """Initialize Swiss Ephemeris with proper error handling"""
    # Get ephemeris path from environment or use default
    ephemeris_path = os.environ.get("EPHEMERIS_PATH", "./ephemeris")
    
    # Create Path object
    path = Path(ephemeris_path)
    
    # Ensure the directory exists
    if not path.exists():
        logger.warning(f"Ephemeris directory {ephemeris_path} not found. Creating directory.")
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create ephemeris directory: {str(e)}")
            # Fall back to relative path as last resort
            ephemeris_path = "./ephemeris"
            logger.warning(f"Falling back to {ephemeris_path}")
            Path(ephemeris_path).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Setting ephemeris path to {ephemeris_path}")
    
    # Set the ephemeris path
    swe.set_ephe_path(ephemeris_path)
    
    # Verify the ephemeris by attempting to calculate the sun's position
    try:
        test_jd = swe.julday(2000, 1, 1, 0)
        _ = swe.calc_ut(test_jd, swe.SUN)
        logger.info("Swiss Ephemeris initialized successfully")
    except Exception as e:
        logger.error(f"Failed to verify Swiss Ephemeris: {str(e)}")
        logger.warning("Ephemeris data files may be missing. Calculations may be inaccurate.")

# Run initialization
initialize_ephemeris()

# Ayanamsa constants
AYANAMSA_LAHIRI = swe.SIDM_LAHIRI
AYANAMSA_RAMAN = swe.SIDM_RAMAN
AYANAMSA_KP = swe.SIDM_KRISHNAMURTI

# Zodiac signs - 1-based indexing in the API but 0-based in the code
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio", 
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Nakshatras (27 lunar mansions) - 0-based indexing
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", 
    "Mrigashira", "Ardra", "Punarvasu", "Pushya", 
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", 
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", 
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Planet constants
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # North Node (Rahu)
    "Ketu": -1  # South Node (Ketu), calculated from Rahu
}

# Dasha years for each planet (Vimshottari system)
DASHA_YEARS = {
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
    "Ketu": 7,
    "Venus": 20
}

# House systems - using Whole Sign (W) as required by specifications
HOUSE_SYSTEM = b'W'  # Whole Sign house system

# Add Sanskrit names mapping
SANSKRIT_NAMES = {
    "Sun": "Surya",
    "Moon": "Chandra",
    "Mars": "Mangala",
    "Mercury": "Budha",
    "Jupiter": "Guru",
    "Venus": "Shukra",
    "Saturn": "Shani",
    "Rahu": "Rahu",
    "Ketu": "Ketu"
}

def get_julian_day(birth_date: str, birth_time: str, timezone_offset: float) -> float:
    """Calculate Julian day from birth date and time"""
    try:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        
        # Convert local time to UTC based on timezone offset
        utc_datetime = dt - timedelta(hours=timezone_offset)
        
        # Extract date components for Julian day calculation
        year, month, day = utc_datetime.year, utc_datetime.month, utc_datetime.day
        hour = utc_datetime.hour + utc_datetime.minute/60.0 + utc_datetime.second/3600.0
        
        # Calculate Julian day
        julian_day = swe.julday(year, month, day, hour)
        return julian_day
    
    except Exception as e:
        logger.error(f"Error calculating Julian day: {str(e)}")
        raise ValueError(f"Failed to calculate Julian day: {str(e)}")

def set_ayanamsa(ayanamsa: str) -> int:
    """Set the ayanamsa (precession model) for calculations"""
    ayanamsa_map = {
        "lahiri": AYANAMSA_LAHIRI,
        "raman": AYANAMSA_RAMAN,
        "krishnamurti": AYANAMSA_KP
    }
    
    ayanamsa_id = ayanamsa_map.get(ayanamsa.lower(), AYANAMSA_LAHIRI)
    swe.set_sid_mode(ayanamsa_id)
    return ayanamsa_id

def get_nakshatra_info(longitude: float) -> Tuple[str, int, int]:
    """
    Get nakshatra information based on longitude
    Returns: (nakshatra_name, nakshatra_id, pada)
    """
    # Each nakshatra is 13°20' (or 13.33333... degrees)
    nakshatra_size = 13 + 1/3
    
    # Calculate nakshatra ID (0-26)
    nakshatra_id = int(longitude / nakshatra_size) % 27
    
    # Calculate pada (1-4)
    pada = int((longitude % nakshatra_size) / (nakshatra_size / 4)) + 1
    
    return NAKSHATRAS[nakshatra_id], nakshatra_id, pada

def get_sign_info(longitude: float) -> Tuple[str, int]:
    """
    Get zodiac sign information based on longitude
    
    Args:
        longitude (float): Longitude in degrees (0-360)
        
    Returns:
        Tuple[str, int]: Tuple containing (sign_name, sign_id)
        
    Note: sign_id is 0-based (0-11) internally to make modular arithmetic simpler,
    but will be converted to 1-based indexing (1-12) for API responses.
    
    Sign mapping (0-based):
    0: Aries, 1: Taurus, 2: Gemini, 3: Cancer, 
    4: Leo, 5: Virgo, 6: Libra, 7: Scorpio, 
    8: Sagittarius, 9: Capricorn, 10: Aquarius, 11: Pisces
    """
    sign_id = int(longitude / 30) % 12  # Get 0-based index (0-11)
    return ZODIAC_SIGNS[sign_id], sign_id

def get_planet_dignity(planet: str, sign_id: int) -> str:
    """
    Determine planet's dignity in the current sign
    
    Note: sign_id is expected to be 0-based (0-11)
    """
    # Simplified dignities - this can be expanded for more detailed information
    exaltation = {
        "Sun": 0,       # Aries
        "Moon": 1,      # Taurus
        "Mars": 9,      # Capricorn
        "Mercury": 5,   # Virgo
        "Jupiter": 3,   # Cancer
        "Venus": 11,    # Pisces
        "Saturn": 6,    # Libra
        "Rahu": 1,      # Taurus
        "Ketu": 7       # Scorpio
    }
    
    debilitation = {
        "Sun": 6,       # Libra
        "Moon": 7,      # Scorpio
        "Mars": 3,      # Cancer
        "Mercury": 11,  # Pisces
        "Jupiter": 9,   # Capricorn
        "Venus": 5,     # Virgo
        "Saturn": 0,    # Aries
        "Rahu": 7,      # Scorpio
        "Ketu": 1       # Taurus
    }
    
    own_sign = {
        "Sun": [4],            # Leo
        "Moon": [3],           # Cancer
        "Mars": [0, 7],        # Aries, Scorpio
        "Mercury": [2, 5],     # Gemini, Virgo
        "Jupiter": [8, 11],    # Sagittarius, Pisces
        "Venus": [1, 6],       # Taurus, Libra
        "Saturn": [9, 10],     # Capricorn, Aquarius
        "Rahu": [],            # None
        "Ketu": []             # None
    }
    
    if planet in exaltation and sign_id == exaltation[planet]:
        return "Exalted"
    elif planet in debilitation and sign_id == debilitation[planet]:
        return "Debilitated"
    elif planet in own_sign and sign_id in own_sign[planet]:
        return "Own Sign"
    else:
        return "Neutral"

def calculate_ascendant(
    birth_date: str, 
    birth_time: str, 
    latitude: float, 
    longitude: float, 
    timezone_offset: float, 
    ayanamsa: str
) -> AscendantInfo:
    """
    Calculate the ascendant (lagna) based on birth details
    
    Note: This function requires coordinates and timezone. It's recommended to use the 
    HoroscopeRequest model with place name instead of directly calling this function,
    as it will handle geocoding automatically.
    """
    try:
        # Calculate Julian day
        julian_day = get_julian_day(birth_date, birth_time, timezone_offset)
        
        # Set ayanamsa
        set_ayanamsa(ayanamsa)
        
        # Calculate houses
        houses_cusps, ascmc = swe.houses_ex(julian_day, latitude, longitude, HOUSE_SYSTEM)
        
        # Get ascendant longitude (sidereal, with ayanamsa adjustment)
        asc_longitude = ascmc[0] - swe.get_ayanamsa(julian_day)
        if asc_longitude < 0:
            asc_longitude += 360
        
        # Get sign information - this returns 0-based sign_id
        sign_name, sign_id = get_sign_info(asc_longitude)
        
        # Get nakshatra information
        nakshatra_name, nakshatra_id, nakshatra_pada = get_nakshatra_info(asc_longitude)
        
        # Calculate degrees, minutes, seconds
        total_degrees = asc_longitude % 30
        degrees = int(total_degrees)
        minutes_float = (total_degrees - degrees) * 60
        minutes = int(minutes_float)
        seconds = round((minutes_float - minutes) * 60, 4)
        
        logger.info(f"Ascendant calculation - Longitude: {asc_longitude}, Sign: {sign_name} (ID: {sign_id}, 0-based), "
                   f"Nakshatra: {nakshatra_name}, Position: {degrees}° {minutes}' {int(seconds)}\"")
        
        return AscendantInfo(
            sign=sign_name,
            sign_id=sign_id + 1,  # Convert to 1-based for API response
            degrees=degrees,
            minutes=minutes,
            seconds=int(seconds),
            longitude=round(asc_longitude, 4),
            nakshatra=nakshatra_name,
            nakshatra_id=nakshatra_id + 1,  # Convert to 1-based for API response
            nakshatra_pada=nakshatra_pada
        )
    
    except Exception as e:
        logger.error(f"Error calculating ascendant: {str(e)}")
        raise ValueError(f"Failed to calculate ascendant: {str(e)}")

def calculate_planet_position(planet_id: int, julian_day: float) -> Dict[str, Any]:
    """Calculate planet position using Swiss Ephemeris"""
    try:
        # For Ketu (South Node), calculate based on Rahu (North Node) + 180°
        if planet_id == -1:  # Ketu
            rahu_result = swe.calc_ut(julian_day, swe.MEAN_NODE)
            # Safe access to tuple elements with defaults
            longitude = (rahu_result[0] + 180) % 360 if len(rahu_result) > 0 else 0
            latitude = -rahu_result[1] if len(rahu_result) > 1 else 0
            distance = rahu_result[2] if len(rahu_result) > 2 else 1.0
            speed = -rahu_result[3] if len(rahu_result) > 3 else 0
        else:
            result = swe.calc_ut(julian_day, planet_id)
            # Safe access to tuple elements with defaults
            longitude = result[0] if len(result) > 0 else 0
            latitude = result[1] if len(result) > 1 else 0
            distance = result[2] if len(result) > 2 else 1.0
            speed = result[3] if len(result) > 3 else 0

        # Apply ayanamsa to get sidereal longitude
        sidereal_longitude = longitude - swe.get_ayanamsa(julian_day)
        if sidereal_longitude < 0:
            sidereal_longitude += 360
        
        return {
            "longitude": round(sidereal_longitude, 4),
            "latitude": round(latitude, 4),
            "distance": distance,
            "speed": round(speed, 4),
            "is_retrograde": speed < 0
        }
    except Exception as e:
        # Log the error and return default values
        logger.error(f"Error in calculate_planet_position: {str(e)}")
        return {
            "longitude": 0,
            "latitude": 0,
            "distance": 1.0,
            "speed": 0,
            "is_retrograde": False
        }

def calculate_planets(
    birth_date: str, 
    birth_time: str, 
    latitude: float, 
    longitude: float, 
    timezone_offset: float, 
    ayanamsa: str
) -> List[PlanetInfo]:
    """
    Calculate planetary positions based on birth details
    
    Note: This function requires coordinates and timezone. It's recommended to use the
    HoroscopeRequest model with place name instead of directly calling this function,
    as it will handle geocoding automatically.
    """
    try:
        # Calculate Julian day
        julian_day = get_julian_day(birth_date, birth_time, timezone_offset)
        
        # Set ayanamsa
        set_ayanamsa(ayanamsa)
        
        # Calculate ascendant first
        houses_cusps, ascmc = swe.houses_ex(julian_day, latitude, longitude, HOUSE_SYSTEM)
        
        # Get ascendant longitude with ayanamsa correction
        asc_longitude = ascmc[0] - swe.get_ayanamsa(julian_day)
        if asc_longitude < 0:
            asc_longitude += 360
            
        # Get ascendant sign (0-11)
        asc_sign = int(asc_longitude / 30)
        
        logger.info(f"Ascendant longitude: {asc_longitude}, sign: {ZODIAC_SIGNS[asc_sign]} (ID: {asc_sign})")
        
        # Calculate positions for all planets
        planets_info = []
        
        for planet_name, planet_id in PLANETS.items():
            # Calculate planet position
            position = calculate_planet_position(planet_id, julian_day)
            
            # Get sign information
            sign_name, sign_id = get_sign_info(position["longitude"])
            
            # Get nakshatra information
            nakshatra_name, nakshatra_id, nakshatra_pada = get_nakshatra_info(position["longitude"])
            
            # Calculate house position using Vedic Whole Sign house system
            # In Whole Sign houses, the house is determined by counting from the ascendant sign
            # Sign_id and asc_sign are 0-based, but house is 1-based for the response
            house = ((sign_id - asc_sign) % 12) + 1
            
            logger.info(f"Planet: {planet_name}, Longitude: {position['longitude']}, Sign: {sign_name} (ID: {sign_id}), Asc Sign: {asc_sign}, House: {house}")
            
            # Calculate degrees, minutes, seconds within sign
            total_degrees = position["longitude"] % 30
            degrees = int(total_degrees)
            minutes_float = (total_degrees - degrees) * 60
            minutes = int(minutes_float)
            seconds = round((minutes_float - minutes) * 60, 4)
            
            # Determine planet dignity
            dignity = get_planet_dignity(planet_name, sign_id)
            
            planets_info.append(PlanetInfo(
                name=planet_name,
                sanskrit_name=SANSKRIT_NAMES.get(planet_name, planet_name),
                longitude=round(position["longitude"], 4),
                latitude=round(position.get("latitude", 0.0), 4),
                sign=sign_name,
                sign_id=sign_id + 1,  # Convert to 1-based for API response
                sign_longitude=round(total_degrees, 4),
                house=house,
                nakshatra=nakshatra_name,
                nakshatra_id=nakshatra_id + 1,  # Convert to 1-based for API response
                nakshatra_pada=nakshatra_pada,
                is_retrograde=position["is_retrograde"],
                speed=round(position["speed"], 4),
                degrees=degrees,
                minutes=minutes,
                seconds=int(seconds),
                dignity=dignity
            ))
        
        return planets_info
    
    except Exception as e:
        logger.error(f"Error calculating planetary positions: {str(e)}")
        raise ValueError(f"Failed to calculate planetary positions: {str(e)}")

def calculate_houses(
    birth_date: str, 
    birth_time: str, 
    latitude: float, 
    longitude: float, 
    timezone_offset: float, 
    ayanamsa: str
) -> List[HouseInfo]:
    """Calculate house positions based on birth details using Whole Sign house system"""
    try:
        # Calculate Julian day
        julian_day = get_julian_day(birth_date, birth_time, timezone_offset)
        
        # Set ayanamsa
        set_ayanamsa(ayanamsa)
        
        # Calculate houses
        houses_cusps, ascmc = swe.houses_ex(julian_day, latitude, longitude, HOUSE_SYSTEM)
        
        # Get ascendant longitude with ayanamsa correction
        asc_longitude = ascmc[0] - swe.get_ayanamsa(julian_day)
        if asc_longitude < 0:
            asc_longitude += 360
        
        # Get ascendant sign (0-11)
        asc_sign = int(asc_longitude / 30)
        
        logger.info(f"House calculation - Ascendant longitude: {asc_longitude}, sign: {ZODIAC_SIGNS[asc_sign]} (ID: {asc_sign})")
        
        houses = []
        
        # In Whole Sign houses, each house corresponds to a complete sign
        # House numbering is 1-based, but sign indices are 0-based
        for i in range(12):  # Process all 12 houses (0-11 index)
            # Calculate the sign for this house (0-11)
            house_sign = (asc_sign + i) % 12
            
            # Get the longitude at the beginning of the sign
            house_longitude = house_sign * 30
            
            # Get sign information (0-based)
            sign_name, sign_id = get_sign_info(house_longitude)
            
            # House number is 1-based (i+1)
            house_number = i + 1
            
            logger.info(f"House: {house_number}, Sign: {sign_name} (ID: {sign_id}), Longitude: {house_longitude}")
            
            houses.append(HouseInfo(
                house_number=house_number,
                sign=sign_name,
                sign_id=sign_id + 1,  # Convert to 1-based for API response
                degrees=0,  # In Whole Sign, house starts at 0 degrees of the sign
                minutes=0,
                seconds=0,
                longitude=round(house_longitude, 4)
            ))
        
        return houses
    
    except Exception as e:
        logger.error(f"Error calculating house positions: {str(e)}")
        raise ValueError(f"Failed to calculate house positions: {str(e)}")

def calculate_dasha_periods(
    birth_date: str, 
    birth_time: str, 
    latitude: float, 
    longitude: float, 
    timezone_offset: float, 
    ayanamsa: str
) -> List[DashaPeriod]:
    """Calculate Vimshottari dasha periods"""
    try:
        # Calculate Julian day
        julian_day = get_julian_day(birth_date, birth_time, timezone_offset)
        
        # Set ayanamsa
        set_ayanamsa(ayanamsa)
        
        # Calculate Moon's position
        moon_position = calculate_planet_position(swe.MOON, julian_day)
        
        # Calculate Moon's nakshatra
        nakshatra_size = 13 + 1/3  # 13°20'
        nakshatra_id = int(moon_position["longitude"] / nakshatra_size) % 27
        
        # Calculate remaining degrees in the nakshatra
        degrees_in_nakshatra = moon_position["longitude"] % nakshatra_size
        
        # Calculate balance of dasha at birth
        nakshatra_lord_order = [
            "Ketu", "Venus", "Sun", "Moon", "Mars", 
            "Rahu", "Jupiter", "Saturn", "Mercury"
        ]
        
        # Determine the lord of the nakshatra
        nakshatra_ruler_index = nakshatra_id % 9
        first_dasha_lord = nakshatra_lord_order[nakshatra_ruler_index]
        
        # Calculate balance of first dasha
        total_years = DASHA_YEARS[first_dasha_lord]
        nakshatra_progress = degrees_in_nakshatra / nakshatra_size
        balance_years = total_years * (1 - nakshatra_progress)
        
        # Convert birth date to datetime
        birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        
        # Generate dasha periods
        dasha_periods = []
        current_date = birth_dt
        
        # Start with remaining portion of first dasha
        end_date = current_date + timedelta(days=balance_years*365.25)
        
        dasha_periods.append(DashaPeriod(
            planet=first_dasha_lord,
            start_date=birth_dt.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            years=round(balance_years, 4)
        ))
        
        current_date = end_date
        
        # Calculate subsequent dashas
        start_index = (nakshatra_ruler_index + 1) % 9
        
        for i in range(8):  # 8 more dashas to complete the cycle
            lord_index = (start_index + i) % 9
            dasha_lord = nakshatra_lord_order[lord_index]
            years = DASHA_YEARS[dasha_lord]
            
            end_date = current_date + timedelta(days=years*365.25)
            
            dasha_periods.append(DashaPeriod(
                planet=dasha_lord,
                start_date=current_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                years=years
            ))
            
            current_date = end_date
        
        return dasha_periods
    
    except Exception as e:
        logger.error(f"Error calculating dasha periods: {str(e)}")
        raise ValueError(f"Failed to calculate dasha periods: {str(e)}")

# Additional utility functions for testing and validation

def validate_d1_chart(
    ascendant_info: AscendantInfo,
    planets_info: List[PlanetInfo],
    houses_info: List[HouseInfo]
) -> None:
    """
    Validate that the D1 chart calculations are consistent for debugging purposes.
    
    This checks:
    1. House signs match what's expected from the ascendant
    2. Planet house assignments match their sign positions
    3. The 1-based and 0-based indexing is consistent
    
    Args:
        ascendant_info: The ascendant information
        planets_info: List of planetary positions
        houses_info: List of house positions
    """
    logger.info("=============== D1 CHART VALIDATION ===============")
    
    # Ascendant info
    asc_sign_id_0based = ascendant_info.sign_id - 1  # Convert 1-based to 0-based
    logger.info(f"Ascendant: {ascendant_info.sign} (ID: {ascendant_info.sign_id} / 0-based: {asc_sign_id_0based})")
    
    # Validate houses
    logger.info("House validation:")
    for house in houses_info:
        sign_id_0based = house.sign_id - 1  # Convert 1-based to 0-based
        expected_sign_id_0based = (asc_sign_id_0based + house.house_number - 1) % 12
        is_correct = sign_id_0based == expected_sign_id_0based
        
        logger.info(f"House {house.house_number}: Sign: {house.sign} (ID: {house.sign_id} / 0-based: {sign_id_0based}), "
                   f"Expected sign ID (0-based): {expected_sign_id_0based}, "
                   f"Correct: {is_correct}")
    
    # Validate planets
    logger.info("Planet validation:")
    for planet in planets_info:
        sign_id_0based = planet.sign_id - 1  # Convert 1-based to 0-based
        expected_house = ((sign_id_0based - asc_sign_id_0based) % 12) + 1
        is_correct = planet.house == expected_house
        
        logger.info(f"Planet: {planet.name}, Sign: {planet.sign} (ID: {planet.sign_id} / 0-based: {sign_id_0based}), "
                   f"House: {planet.house}, Expected house: {expected_house}, Correct: {is_correct}")
    
    logger.info("====================================================") 