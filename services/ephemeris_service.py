"""
Ephemeris service module for Swiss Ephemeris calculations.
This module provides integration with the Swiss Ephemeris for precise astronomical calculations.
"""

import os
import math
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

from ..utils.custom_exceptions import EphemerisError
from ..utils.logger import get_logger
from ..constants.ayanamsa import AYANAMSA_LAHIRI, AYANAMSA_KRISHNAMURTI, AYANAMSA_RAMAN
from ..constants.planets import PLANETS
from ..config import settings

logger = get_logger(__name__)

# Import the Swiss Ephemeris library
import swisseph as swe

# Ayanamsa mapping to Swiss Ephemeris constants
AYANAMSA_MAPPING = {
    AYANAMSA_LAHIRI: swe.SIDM_LAHIRI,
    AYANAMSA_KRISHNAMURTI: swe.SIDM_KRISHNAMURTI,
    AYANAMSA_RAMAN: swe.SIDM_RAMAN
}

# Planet codes for Swiss Ephemeris
PLANET_CODES = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mars": swe.MARS,
    "mercury": swe.MERCURY,
    "jupiter": swe.JUPITER,
    "venus": swe.VENUS,
    "saturn": swe.SATURN,
    "rahu": swe.MEAN_NODE,  # Mean Lunar Node (North)
    "ketu": swe.MEAN_NODE   # For Ketu, we'll use the same and add 180°
}

def init_ephemeris() -> bool:
    """
    Initialize the Swiss Ephemeris library.
    
    Returns:
        bool: True if initialization was successful
    """
    try:
        ephemeris_path = Path(settings.EPHEMERIS_PATH).resolve()
        logger.info(f"Initializing ephemeris with path: {ephemeris_path}")
        
        # Create directory if it doesn't exist
        ephemeris_path.mkdir(parents=True, exist_ok=True)
        
        # Set the ephemeris files path
        swe.set_ephe_path(str(ephemeris_path))
        
        logger.info("Swiss Ephemeris initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize ephemeris: {str(e)}")
        raise EphemerisError(f"Initialization failed: {str(e)}")

def convert_to_julian_day(year: int, month: int, day: int, hour: float) -> float:
    """
    Convert Gregorian date to Julian day.
    
    Args:
        year (int): Year
        month (int): Month (1-12)
        day (int): Day (1-31)
        hour (float): Hour including minutes and seconds (0-23.999)
        
    Returns:
        float: Julian day
    """
    try:
        return swe.julday(year, month, day, hour)
    except Exception as e:
        logger.error(f"Error converting to Julian day: {str(e)}")
        raise EphemerisError(f"Julian day conversion failed: {str(e)}")

def get_planet_position(julian_day: float, planet_code: int, ayanamsa=AYANAMSA_LAHIRI) -> Dict[str, Any]:
    """
    Calculate planet's longitude and latitude at a given julian day.
    
    Args:
        julian_day (float): Julian day for calculation
        planet_code (int): Swiss Ephemeris planet code
        ayanamsa (int): Ayanamsa to use (default: Lahiri)
        
    Returns:
        dict: Containing longitude, latitude, distance, speed
    """
    try:
        # Set ayanamsa
        swe.set_sid_mode(AYANAMSA_MAPPING.get(ayanamsa, AYANAMSA_MAPPING[AYANAMSA_LAHIRI]))
        
        # For Ketu, we need special handling
        is_ketu = planet_code == PLANET_CODES["ketu"]
        
        # If Ketu, we calculate Rahu and then add 180°
        calc_planet_code = PLANET_CODES["rahu"] if is_ketu else planet_code
        
        # Calculate planet position
        flags = 0  # We can add flags for different calculations if needed
        result = swe.calc_ut(julian_day, calc_planet_code, flags)
        
        # For Ketu, add 180° to Rahu's longitude
        longitude = (result[0] + 180) % 360 if is_ketu else result[0]
        
        # Structure response
        return {
            "longitude": longitude,
            "latitude": result[1],
            "distance": result[2],
            "speed": result[3] * -1 if is_ketu else result[3]  # Reverse speed for Ketu
        }
    except Exception as e:
        logger.error(f"Error calculating planet position: {str(e)}")
        raise EphemerisError(f"Planet calculation failed: {str(e)}")

def get_planet_speed(julian_day: float, planet_code: int) -> float:
    """
    Calculate planet's speed at a given julian day.
    Used to determine if planet is retrograde.
    
    Args:
        julian_day (float): Julian day for calculation
        planet_code (int): Swiss Ephemeris planet code
        
    Returns:
        float: Planet speed
    """
    try:
        # For Ketu, we need special handling
        is_ketu = planet_code == PLANET_CODES["ketu"]
        
        # If Ketu, we calculate Rahu and then reverse the speed
        calc_planet_code = PLANET_CODES["rahu"] if is_ketu else planet_code
        
        result = swe.calc_ut(julian_day, calc_planet_code)
        return result[3] * -1 if is_ketu else result[3]
    except Exception as e:
        logger.error(f"Error calculating planet speed: {str(e)}")
        raise EphemerisError(f"Speed calculation failed: {str(e)}")

def get_ayanamsa(julian_day: float, ayanamsa_code: int) -> float:
    """
    Get ayanamsa value at a given julian day.
    
    Args:
        julian_day (float): Julian day for calculation
        ayanamsa_code (int): Ayanamsa code
        
    Returns:
        float: Ayanamsa value in degrees
    """
    try:
        # Set the sidereal mode
        ayanamsa_se_code = AYANAMSA_MAPPING.get(ayanamsa_code, AYANAMSA_MAPPING[AYANAMSA_LAHIRI])
        swe.set_sid_mode(ayanamsa_se_code)
        
        # Get the ayanamsa value
        return swe.get_ayanamsa_ut(julian_day)
    except Exception as e:
        logger.error(f"Error calculating ayanamsa: {str(e)}")
        raise EphemerisError(f"Ayanamsa calculation failed: {str(e)}")

def calculate_ascendant(julian_day: float, latitude: float, longitude: float, ayanamsa=AYANAMSA_LAHIRI) -> float:
    """
    Calculate the ascendant degree for a given time and location.
    
    Args:
        julian_day (float): Julian day for calculation
        latitude (float): Latitude in degrees (-90 to +90)
        longitude (float): Longitude in degrees (-180 to +180)
        ayanamsa (int): Ayanamsa to use (default: Lahiri)
        
    Returns:
        float: Ascendant longitude in degrees (0-360)
    """
    try:
        # Set ayanamsa
        swe.set_sid_mode(AYANAMSA_MAPPING.get(ayanamsa, AYANAMSA_MAPPING[AYANAMSA_LAHIRI]))
        
        # Calculate houses - 'P' is for Placidus house system
        houses_system = 'P'
        cusps, ascmc = swe.houses(julian_day, latitude, longitude, houses_system.encode('utf-8'))
        
        # Ascendant is the first angle in ascmc array
        ascendant = ascmc[0]
        
        return ascendant
    except Exception as e:
        logger.error(f"Error calculating ascendant: {str(e)}")
        raise EphemerisError(f"Ascendant calculation failed: {str(e)}")

def calculate_house_cusps(julian_day: float, latitude: float, longitude: float, ayanamsa=AYANAMSA_LAHIRI) -> List[float]:
    """
    Calculate house cusps for a given time and location.
    
    Args:
        julian_day (float): Julian day for calculation
        latitude (float): Latitude in degrees (-90 to +90)
        longitude (float): Longitude in degrees (-180 to +180)
        ayanamsa (int): Ayanamsa to use (default: Lahiri)
        
    Returns:
        List[float]: List of house cusps (13 elements: 0 plus 12 house cusps)
    """
    try:
        # Set ayanamsa
        swe.set_sid_mode(AYANAMSA_MAPPING.get(ayanamsa, AYANAMSA_MAPPING[AYANAMSA_LAHIRI]))
        
        # Calculate houses - 'P' is for Placidus house system
        houses_system = 'P'
        cusps, ascmc = swe.houses(julian_day, latitude, longitude, houses_system.encode('utf-8'))
        
        return cusps
    except Exception as e:
        logger.error(f"Error calculating house cusps: {str(e)}")
        raise EphemerisError(f"House cusps calculation failed: {str(e)}")

def check_ephemeris_health() -> bool:
    """
    Check if the ephemeris is functioning properly.
    
    Returns:
        bool: True if ephemeris is healthy
    """
    try:
        # Try a simple calculation to verify ephemeris is working
        get_planet_position(2451545.0, PLANET_CODES["sun"])  # Sun position at J2000
        return True
    except Exception as e:
        logger.error(f"Ephemeris health check failed: {str(e)}")
        return False

def close_ephemeris():
    """Close the ephemeris."""
    try:
        swe.close()
        logger.info("Swiss Ephemeris closed successfully")
    except Exception as e:
        logger.error(f"Error closing ephemeris: {str(e)}") 