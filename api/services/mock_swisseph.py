"""
Mock implementation of Swiss Ephemeris for testing purposes.
This module provides a mock implementation of the pyswisseph interface.
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any, Optional
import pyswisseph as swe

# Configure logging
logger = logging.getLogger("jai-api.mock_swisseph")

# Constants from pyswisseph
SUN = swe.SUN
MOON = swe.MOON
MERCURY = swe.MERCURY
VENUS = swe.VENUS
MARS = swe.MARS
JUPITER = swe.JUPITER
SATURN = swe.SATURN
URANUS = swe.URANUS
NEPTUNE = swe.NEPTUNE
PLUTO = swe.PLUTO
MEAN_NODE = swe.MEAN_NODE
TRUE_NODE = swe.TRUE_NODE
MEAN_APOGEE = swe.MEAN_APOGEE
OSCU_APOGEE = swe.OSCU_APOGEE
EARTH = swe.EARTH
CHIRON = swe.CHIRON
PHOLUS = swe.PHOLUS
CERES = swe.CERES
PALLAS = swe.PALLAS
JUNO = swe.JUNO
VESTA = swe.VESTA
INTP_APOGEE = swe.INTP_APOGEE
INTP_PERGEE = swe.INTP_PERGEE

# Ayanamsa constants
SIDM_FAGAN_BRADLEY = swe.SIDM_FAGAN_BRADLEY
SIDM_LAHIRI = swe.SIDM_LAHIRI
SIDM_DELUCE = swe.SIDM_DELUCE
SIDM_RAMAN = swe.SIDM_RAMAN
SIDM_USHASHASHI = swe.SIDM_USHASHASHI
SIDM_KRISHNAMURTI = swe.SIDM_KRISHNAMURTI
SIDM_DJWHAL_KHUL = swe.SIDM_DJWHAL_KHUL
SIDM_YUKTESHWAR = swe.SIDM_YUKTESHWAR
SIDM_JN_BHASIN = swe.SIDM_JN_BHASIN
SIDM_BABYL_KUGLER1 = swe.SIDM_BABYL_KUGLER1
SIDM_BABYL_KUGLER2 = swe.SIDM_BABYL_KUGLER2
SIDM_BABYL_KUGLER3 = swe.SIDM_BABYL_KUGLER3
SIDM_BABYL_HUBER = swe.SIDM_BABYL_HUBER
SIDM_BABYL_ETPSC = swe.SIDM_BABYL_ETPSC
SIDM_ALDEBARAN_15TAU = swe.SIDM_ALDEBARAN_15TAU
SIDM_HIPPARCHOS = swe.SIDM_HIPPARCHOS
SIDM_SASSANIAN = swe.SIDM_SASSANIAN
SIDM_GALCENT_MULA_WILHELM = swe.SIDM_GALCENT_MULA_WILHELM
SIDM_J2000 = swe.SIDM_J2000
SIDM_J1900 = swe.SIDM_J1900
SIDM_B1950 = swe.SIDM_B1950
SIDM_SURYASIDDHANTA = swe.SIDM_SURYASIDDHANTA
SIDM_SURYASIDDHANTA_MSUN = swe.SIDM_SURYASIDDHANTA_MSUN
SIDM_ARYABHATA = swe.SIDM_ARYABHATA
SIDM_ARYABHATA_MSUN = swe.SIDM_ARYABHATA_MSUN
SIDM_SS_REVATI = swe.SIDM_SS_REVATI
SIDM_SS_CITRA = swe.SIDM_SS_CITRA
SIDM_TRUE_CITRA = swe.SIDM_TRUE_CITRA
SIDM_TRUE_REVATI = swe.SIDM_TRUE_REVATI
SIDM_TRUE_PUSHYA = swe.SIDM_TRUE_PUSHYA
SIDM_GALCENT_COCHRANE = swe.SIDM_GALCENT_COCHRANE
SIDM_GALEQU_IAU1958 = swe.SIDM_GALEQU_IAU1958
SIDM_GALEQU_TRUE = swe.SIDM_GALEQU_TRUE
SIDM_GALEQU_MULA = swe.SIDM_GALEQU_MULA
SIDM_GALALIGN_MARDYKS = swe.SIDM_GALALIGN_MARDYKS
SIDM_TRUE_MULA = swe.SIDM_TRUE_MULA
SIDM_GALCENT_MULA_WILHELM = swe.SIDM_GALCENT_MULA_WILHELM
SIDM_GALCENT_RAMAN = swe.SIDM_GALCENT_RAMAN
SIDM_GALCENT_KRISHNAMURTI = swe.SIDM_GALCENT_KRISHNAMURTI
SIDM_GALCENT_KUSHAL = swe.SIDM_GALCENT_KUSHAL
SIDM_GALEQU_FIORENZA = swe.SIDM_GALEQU_FIORENZA
SIDM_VALENS_MOON = swe.SIDM_VALENS_MOON
SIDM_LAHIRI_1940 = swe.SIDM_LAHIRI_1940
SIDM_LAHIRI_VP285 = swe.SIDM_LAHIRI_VP285
SIDM_KRISHNAMURTI_VP291 = swe.SIDM_KRISHNAMURTI_VP291
SIDM_LAHIRI_ICRC = swe.SIDM_LAHIRI_ICRC

# House system constants
HSYS_PLACIDUS = swe.HSYS_PLACIDUS
HSYS_KOCH = swe.HSYS_KOCH
HSYS_EQUAL = swe.HSYS_EQUAL
HSYS_VEHLOW_EQUAL = swe.HSYS_VEHLOW_EQUAL
HSYS_WHOLE_SIGN = swe.HSYS_WHOLE_SIGN
HSYS_MERIDIAN = swe.HSYS_MERIDIAN
HSYS_ALCABITUS = swe.HSYS_ALCABITUS
HSYS_CAMPANUS = swe.HSYS_CAMPANUS
HSYS_REGIOMONTANUS = swe.HSYS_REGIOMONTANUS
HSYS_MORINUS = swe.HSYS_MORINUS

# Global variables
_ephe_path = "./ephemeris"
_sid_mode = SIDM_LAHIRI
_mock_enabled = False

def set_ephe_path(path: str) -> None:
    """Set the ephemeris path"""
    global _ephe_path
    _ephe_path = path
    logger.info(f"Set ephemeris path to {path}")

def set_sid_mode(sid_mode: int) -> None:
    """Set the sidereal mode"""
    global _sid_mode
    _sid_mode = sid_mode
    logger.info(f"Set sidereal mode to {sid_mode}")

def get_ayanamsa(jd: float) -> float:
    """Get the ayanamsa value for a given Julian day"""
    # Mock implementation - returns a constant value for testing
    return 23.85

def julday(year: int, month: int, day: int, hour: float = 0.0) -> float:
    """Calculate Julian day from date and time"""
    # Simple implementation for testing
    dt = datetime(year, month, day)
    jd = 1721425.5  # Julian day for 1/1/1
    jd += (dt - datetime(1, 1, 1)).days
    jd += hour / 24.0
    return jd

def calc_ut(jd: float, planet: int) -> Tuple[float, float, float, float]:
    """Calculate planet position for a given Julian day"""
    if not _mock_enabled:
        raise RuntimeError("Mock Swiss Ephemeris is not enabled")
    
    # Mock implementation - returns fixed positions for testing
    positions = {
        SUN: (0.0, 0.0, 1.0, 0.9856),      # Aries 0°
        MOON: (45.0, 0.0, 60.0, 13.1764),   # Taurus 15°
        MERCURY: (90.0, 0.0, 0.4, 1.3833),  # Gemini 0°
        VENUS: (120.0, 0.0, 0.7, 1.2),      # Leo 0°
        MARS: (180.0, 0.0, 1.5, 0.5240),    # Libra 0°
        JUPITER: (240.0, 0.0, 5.2, 0.0833), # Sagittarius 0°
        SATURN: (300.0, 0.0, 9.5, 0.0341),  # Aquarius 0°
        MEAN_NODE: (150.0, 0.0, 0.0, -0.0529), # Virgo 0° (retrograde)
        TRUE_NODE: (150.0, 0.0, 0.0, -0.0529), # Virgo 0° (retrograde)
    }
    
    if planet in positions:
        return positions[planet]
    else:
        return (0.0, 0.0, 1.0, 0.0)  # Default position

def houses_ex(jd: float, lat: float, lon: float, hsys: bytes = HSYS_PLACIDUS) -> Tuple[List[float], List[float]]:
    """Calculate house cusps and angles"""
    if not _mock_enabled:
        raise RuntimeError("Mock Swiss Ephemeris is not enabled")
    
    # Mock implementation - returns fixed house cusps for testing
    # For Whole Sign houses, each house starts at 0° of its sign
    cusps = [0.0] * 13  # 12 houses + 1
    ascmc = [0.0] * 10  # Ascendant, MC, etc.
    
    # Set ascendant to 0° Aries for testing
    ascmc[0] = 0.0
    
    # Set house cusps for Whole Sign system
    for i in range(13):
        cusps[i] = i * 30.0
    
    return cusps, ascmc

def enable_mock() -> None:
    """Enable the mock implementation"""
    global _mock_enabled
    _mock_enabled = True
    logger.info("Mock Swiss Ephemeris enabled")

def disable_mock() -> None:
    """Disable the mock implementation"""
    global _mock_enabled
    _mock_enabled = False
    logger.info("Mock Swiss Ephemeris disabled")

def is_mock_enabled() -> bool:
    """Check if mock implementation is enabled"""
    return _mock_enabled 