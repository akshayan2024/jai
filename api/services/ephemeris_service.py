"""
Ephemeris service module for Swiss Ephemeris calculations.
This module provides a high-level interface to the Swiss Ephemeris library.
"""

import os
import logging
from typing import Dict, List, Tuple, Optional
import pyswisseph as swe

# Configure logging
logger = logging.getLogger("jai-api.ephemeris")

class EphemerisService:
    """Service class for Swiss Ephemeris calculations"""
    
    def __init__(self, ayanamsa: int = swe.SIDM_LAHIRI):
        """
        Initialize the ephemeris service
        
        Args:
            ayanamsa: The ayanamsa to use (default: Lahiri)
        """
        # Set ephemeris path from environment or use default
        ephemeris_path = os.environ.get("EPHEMERIS_PATH", "./ephemeris")
        if not os.path.exists(ephemeris_path):
            raise RuntimeError(f"Ephemeris path does not exist: {ephemeris_path}")
        
        # Set ephemeris path
        swe.set_ephe_path(ephemeris_path)
        logger.info(f"Set ephemeris path to {ephemeris_path}")
        
        # Set sidereal mode
        swe.set_sid_mode(ayanamsa)
        logger.info(f"Set sidereal mode to {ayanamsa} (Lahiri)")
        
        # Verify initialization
        try:
            test_jd = swe.julday(2000, 1, 1, 0)
            xx, ret = swe.calc_ut(test_jd, swe.SUN)
            if ret < 0:
                raise RuntimeError(f"Swiss Ephemeris test calculation failed with error code {ret}")
            logger.info("Swiss Ephemeris initialized successfully")
        except Exception as e:
            logger.error(f"Failed to verify Swiss Ephemeris: {str(e)}")
            raise RuntimeError("Failed to initialize Swiss Ephemeris")
    
    def get_planet_position(self, jd: float, planet: int) -> Dict[str, float]:
        """
        Get planet position for a given Julian day
        
        Args:
            jd: Julian day
            planet: Planet ID (e.g., swe.SUN, swe.MOON, etc.)
            
        Returns:
            Dictionary containing longitude, latitude, distance, and speed
            
        Raises:
            RuntimeError: If the calculation fails
        """
        try:
            # Use FLG_SIDEREAL for sidereal positions
            flag = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
            xx, ret = swe.calc_ut(jd, planet, flag)
            
            if ret < 0:
                raise RuntimeError(f"Planet calculation failed with error code {ret}")
            
            return {
                "longitude": xx[0],
                "latitude": xx[1],
                "distance": xx[2],
                "speed": xx[3]
            }
        except Exception as e:
            logger.error(f"Error calculating planet position: {str(e)}")
            raise
    
    def get_ascendant(self, jd: float, lat: float, lon: float) -> Tuple[float, List[float]]:
        """
        Calculate ascendant and house cusps
        
        Args:
            jd: Julian day
            lat: Latitude
            lon: Longitude
            
        Returns:
            Tuple of (ascendant longitude, house cusps)
            
        Raises:
            RuntimeError: If the calculation fails
        """
        try:
            # Use Whole Sign house system
            cusps, ascmc, ret = swe.houses_ex(jd, lat, lon, b'W')
            if ret < 0:
                raise RuntimeError(f"House calculation failed with error code {ret}")
            return ascmc[0], cusps
        except Exception as e:
            logger.error(f"Error calculating ascendant: {str(e)}")
            raise
    
    def get_ayanamsa(self, jd: float) -> float:
        """
        Get ayanamsa value for a given Julian day
        
        Args:
            jd: Julian day
            
        Returns:
            Ayanamsa value in degrees
        """
        return swe.get_ayanamsa(jd)
    
    def julday(self, year: int, month: int, day: int, hour: float = 0.0) -> float:
        """
        Calculate Julian day from date and time
        
        Args:
            year: Year
            month: Month (1-12)
            day: Day (1-31)
            hour: Hour (0-23)
            
        Returns:
            Julian day
        """
        return swe.julday(year, month, day, hour)
    
    def get_planet_dignity(self, planet: int, sign: int) -> str:
        """
        Get planet's dignity in a sign
        
        Args:
            planet: Planet ID
            sign: Sign number (0-11)
            
        Returns:
            Dignity status (Exalted, Debilitated, Own Sign, or Neutral)
        """
        # Classical dignities for the seven planets
        exaltation = {
            swe.SUN: 0,       # Aries
            swe.MOON: 1,      # Taurus
            swe.MARS: 9,      # Capricorn
            swe.MERCURY: 5,   # Virgo
            swe.JUPITER: 3,   # Cancer
            swe.VENUS: 11,    # Pisces
            swe.SATURN: 6     # Libra
        }
        
        debilitation = {
            swe.SUN: 6,       # Libra
            swe.MOON: 7,      # Scorpio
            swe.MARS: 3,      # Cancer
            swe.MERCURY: 11,  # Pisces
            swe.JUPITER: 9,   # Capricorn
            swe.VENUS: 5,     # Virgo
            swe.SATURN: 0     # Aries
        }
        
        own_signs = {
            swe.SUN: [4],            # Leo
            swe.MOON: [3],           # Cancer
            swe.MARS: [0, 7],        # Aries, Scorpio
            swe.MERCURY: [2, 5],     # Gemini, Virgo
            swe.JUPITER: [8, 11],    # Sagittarius, Pisces
            swe.VENUS: [1, 6],       # Taurus, Libra
            swe.SATURN: [9, 10]      # Capricorn, Aquarius
        }
        
        if planet in exaltation and sign == exaltation[planet]:
            return "Exalted"
        elif planet in debilitation and sign == debilitation[planet]:
            return "Debilitated"
        elif planet in own_signs and sign in own_signs[planet]:
            return "Own Sign"
        else:
            return "Neutral"

# Create singleton instance
ephemeris_service = EphemerisService() 