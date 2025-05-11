"""
Ephemeris service module for Swiss Ephemeris calculations.
This module provides a high-level interface to the Swiss Ephemeris library.
"""

import os
import logging
from typing import Dict, List, Tuple, Optional
from contextlib import contextmanager

# Configure logging
logger = logging.getLogger("jai-api.ephemeris")

# Try to import pyswisseph, fall back to mock if not available
try:
    import pyswisseph as swe
    USING_MOCK = False
    logger.info("Using real Swiss Ephemeris library")
except ImportError:
    logger.warning("Swiss Ephemeris library not found, using mock implementation")
    from api.services.mock_swisseph import (
        # Constants
        SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, MEAN_NODE,
        SIDM_LAHIRI,
        HSYS_PLACIDUS, HSYS_KOCH, HSYS_EQUAL, HSYS_WHOLE_SIGN,
        # Functions
        set_ephe_path, set_sid_mode, get_ayanamsa_ut, julday, calc_ut, houses_ex,
        enable_mock, disable_mock, is_mock_enabled, close
    )
    # Enable mock automatically
    enable_mock()
    USING_MOCK = True
    
    # Create mock swe module
    class MockSwe:
        # Planets
        SUN = SUN
        MOON = MOON
        MERCURY = MERCURY
        VENUS = VENUS
        MARS = MARS
        JUPITER = JUPITER
        SATURN = SATURN
        MEAN_NODE = MEAN_NODE
        
        # Sidereal modes
        SIDM_LAHIRI = SIDM_LAHIRI
        
        # House systems
        HSYS_PLACIDUS = HSYS_PLACIDUS
        HSYS_KOCH = HSYS_KOCH
        HSYS_EQUAL = HSYS_EQUAL
        HSYS_WHOLE_SIGN = HSYS_WHOLE_SIGN
        
        # Flags
        FLG_SIDEREAL = 1
        FLG_SWIEPH = 2
        
        @staticmethod
        def set_ephe_path(path):
            return set_ephe_path(path)
        
        @staticmethod
        def set_sid_mode(mode, t0, ayan_t0):
            return set_sid_mode(mode)
        
        @staticmethod
        def get_ayanamsa_ut(jd):
            return get_ayanamsa_ut(jd)
        
        @staticmethod
        def julday(year, month, day, hour):
            return julday(year, month, day, hour)
        
        @staticmethod
        def calc_ut(jd, planet, flags):
            result = calc_ut(jd, planet)
            return result, 0
        
        @staticmethod
        def houses_ex(jd, lat, lon, hsys):
            cusps, ascmc = houses_ex(jd, lat, lon, hsys)
            return cusps, ascmc, 0
        
        @staticmethod
        def close():
            close()
    
    # Replace swe with mock
    swe = MockSwe()

class EphemerisService:
    """Service class for Swiss Ephemeris calculations"""
    
    def __init__(self):
        """Initialize the Swiss Ephemeris service."""
        self._initialized = False
        self._ephe_path = None
        self._sid_mode = None
        self._cleanup_required = False
    
    def initialize(self, ephe_path: str = None, sid_mode: int = swe.SIDM_LAHIRI) -> None:
        """
        Initialize the Swiss Ephemeris service.
        
        Args:
            ephe_path: Path to ephemeris files
            sid_mode: Sidereal mode (default: Lahiri)
            
        Raises:
            RuntimeError: If initialization fails
        """
        try:
            # Set ephemeris path if provided
            if ephe_path:
                self._ephe_path = ephe_path
                swe.set_ephe_path(ephe_path)
                logger.info(f"Set ephemeris path to: {ephe_path}")
            
            # Set sidereal mode
            self._sid_mode = sid_mode
            swe.set_sid_mode(sid_mode, 0, 0)
            logger.info(f"Set sidereal mode to: {sid_mode}")
            
            self._initialized = True
            self._cleanup_required = True
            logger.info("Swiss Ephemeris service initialized successfully")
            
            # Log if using mock implementation
            if USING_MOCK:
                logger.warning("Using mock Swiss Ephemeris implementation")
            
        except Exception as e:
            logger.error(f"Failed to initialize Swiss Ephemeris service: {str(e)}")
            raise RuntimeError(f"Swiss Ephemeris initialization failed: {str(e)}")
    
    def cleanup(self) -> None:
        """
        Clean up Swiss Ephemeris resources.
        
        This method should be called when the service is no longer needed.
        """
        if self._cleanup_required:
            try:
                # Close any open ephemeris files
                swe.close()
                self._initialized = False
                self._cleanup_required = False
                logger.info("Swiss Ephemeris resources cleaned up successfully")
            except Exception as e:
                logger.error(f"Error during Swiss Ephemeris cleanup: {str(e)}")
                raise RuntimeError(f"Swiss Ephemeris cleanup failed: {str(e)}")
    
    @contextmanager
    def ephemeris_context(self, ephe_path: str = None, sid_mode: int = swe.SIDM_LAHIRI):
        """
        Context manager for Swiss Ephemeris operations.
        
        Args:
            ephe_path: Path to ephemeris files
            sid_mode: Sidereal mode (default: Lahiri)
            
        Yields:
            EphemerisService instance
            
        Example:
            with ephemeris_service.ephemeris_context() as ephe:
                result = ephe.get_planet_position(jd, planet)
        """
        try:
            self.initialize(ephe_path, sid_mode)
            yield self
        finally:
            self.cleanup()
    
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
        if not self._initialized:
            raise RuntimeError("Swiss Ephemeris service not initialized")
        
        try:
            # Use FLG_SIDEREAL for sidereal positions
            flag = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
            xx, ret = swe.calc_ut(jd, planet, flag)
            
            if ret < 0 and not USING_MOCK:
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
    
    def get_ascendant(self, jd: float, lat: float, lon: float, house_system: str = 'W') -> Tuple[float, List[float]]:
        """
        Calculate ascendant and house cusps
        
        Args:
            jd: Julian day
            lat: Latitude
            lon: Longitude
            house_system: House system (default: Whole Sign)
            
        Returns:
            Tuple of (ascendant longitude, house cusps)
            
        Raises:
            RuntimeError: If the calculation fails
        """
        if not self._initialized:
            raise RuntimeError("Swiss Ephemeris service not initialized")
        
        try:
            cusps, ascmc, ret = swe.houses_ex(jd, lat, lon, house_system.encode())
            if ret < 0 and not USING_MOCK:
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
        if not self._initialized:
            raise RuntimeError("Swiss Ephemeris service not initialized")
        
        try:
            return swe.get_ayanamsa_ut(jd)
        except Exception as e:
            logger.error(f"Error calculating ayanamsa: {str(e)}")
            raise RuntimeError(f"Ayanamsa calculation failed: {str(e)}")
    
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
        if not self._initialized:
            raise RuntimeError("Swiss Ephemeris service not initialized")
        
        try:
            return swe.julday(year, month, day, hour)
        except Exception as e:
            logger.error(f"Error calculating Julian day: {str(e)}")
            raise RuntimeError(f"Julian day calculation failed: {str(e)}")
    
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