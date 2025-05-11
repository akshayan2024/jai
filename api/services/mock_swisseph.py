"""
Mock implementation of Swiss Ephemeris for testing purposes.
This module provides a mock implementation of the pyswisseph interface.
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any, Optional

# Configure logging
logger = logging.getLogger("jai-api.mock_swisseph")

# Define constants to match pyswisseph
# Planet IDs
SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
URANUS = 7
NEPTUNE = 8
PLUTO = 9
MEAN_NODE = 10
TRUE_NODE = 11
MEAN_APOGEE = 12
OSCU_APOGEE = 13
EARTH = 14
CHIRON = 15
PHOLUS = 16
CERES = 17
PALLAS = 18
JUNO = 19
VESTA = 20
INTP_APOGEE = 21
INTP_PERGEE = 22

# Ayanamsa constants
SIDM_FAGAN_BRADLEY = 0
SIDM_LAHIRI = 1
SIDM_DELUCE = 2
SIDM_RAMAN = 3
SIDM_USHASHASHI = 4
SIDM_KRISHNAMURTI = 5
SIDM_DJWHAL_KHUL = 6
SIDM_YUKTESHWAR = 7
SIDM_JN_BHASIN = 8
SIDM_BABYL_KUGLER1 = 9
SIDM_BABYL_KUGLER2 = 10
SIDM_BABYL_KUGLER3 = 11
SIDM_BABYL_HUBER = 12
SIDM_BABYL_ETPSC = 13
SIDM_ALDEBARAN_15TAU = 14
SIDM_HIPPARCHOS = 15
SIDM_SASSANIAN = 16
SIDM_GALCENT_MULA_WILHELM = 17
SIDM_J2000 = 18
SIDM_J1900 = 19
SIDM_B1950 = 20
SIDM_SURYASIDDHANTA = 21
SIDM_SURYASIDDHANTA_MSUN = 22
SIDM_ARYABHATA = 23
SIDM_ARYABHATA_MSUN = 24
SIDM_SS_REVATI = 25
SIDM_SS_CITRA = 26
SIDM_TRUE_CITRA = 27
SIDM_TRUE_REVATI = 28
SIDM_TRUE_PUSHYA = 29
SIDM_GALCENT_COCHRANE = 30
SIDM_GALEQU_IAU1958 = 31
SIDM_GALEQU_TRUE = 32
SIDM_GALEQU_MULA = 33
SIDM_GALALIGN_MARDYKS = 34
SIDM_TRUE_MULA = 35
SIDM_GALCENT_MULA_WILHELM = 36
SIDM_GALCENT_RAMAN = 37
SIDM_GALCENT_KRISHNAMURTI = 38
SIDM_GALCENT_KUSHAL = 39
SIDM_GALEQU_FIORENZA = 40
SIDM_VALENS_MOON = 41
SIDM_LAHIRI_1940 = 42
SIDM_LAHIRI_VP285 = 43
SIDM_KRISHNAMURTI_VP291 = 44
SIDM_LAHIRI_ICRC = 45

# House system constants
HSYS_PLACIDUS = b'P'
HSYS_KOCH = b'K'
HSYS_EQUAL = b'E'
HSYS_VEHLOW_EQUAL = b'V'
HSYS_WHOLE_SIGN = b'W'
HSYS_MERIDIAN = b'X'
HSYS_ALCABITUS = b'B'
HSYS_CAMPANUS = b'C'
HSYS_REGIOMONTANUS = b'R'
HSYS_MORINUS = b'M'

# Flag constants
FLG_SIDEREAL = 1
FLG_SWIEPH = 2

# Global variables
_ephe_path = "./ephemeris"
_sid_mode = SIDM_LAHIRI
_mock_enabled = False

def set_ephe_path(path: str) -> None:
    """Set the ephemeris path"""
    global _ephe_path
    _ephe_path = path
    logger.info(f"Set ephemeris path to {path}")

def set_sid_mode(sid_mode: int, t0: float = 0, ayan_t0: float = 0) -> None:
    """Set the sidereal mode"""
    global _sid_mode
    _sid_mode = sid_mode
    logger.info(f"Set sidereal mode to {sid_mode}")

def get_ayanamsa_ut(jd: float) -> float:
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

def calc_ut(jd: float, planet: int, flag: int = 0) -> Tuple[List[float], int]:
    """Calculate planet position for a given Julian day"""
    if not _mock_enabled:
        raise RuntimeError("Mock Swiss Ephemeris is not enabled")
    
    # Mock implementation - returns fixed positions for testing
    positions = {
        SUN: [0.0, 0.0, 1.0, 0.9856],      # Aries 0°
        MOON: [45.0, 0.0, 60.0, 13.1764],   # Taurus 15°
        MERCURY: [90.0, 0.0, 0.4, 1.3833],  # Gemini 0°
        VENUS: [120.0, 0.0, 0.7, 1.2],      # Leo 0°
        MARS: [180.0, 0.0, 1.5, 0.5240],    # Libra 0°
        JUPITER: [240.0, 0.0, 5.2, 0.0833], # Sagittarius 0°
        SATURN: [300.0, 0.0, 9.5, 0.0341],  # Aquarius 0°
        MEAN_NODE: [150.0, 0.0, 0.0, -0.0529], # Virgo 0° (retrograde)
        TRUE_NODE: [150.0, 0.0, 0.0, -0.0529], # Virgo 0° (retrograde)
    }
    
    if planet in positions:
        return positions[planet], 0
    else:
        return [0.0, 0.0, 1.0, 0.0], 0  # Default position

def houses_ex(jd: float, lat: float, lon: float, hsys: bytes = HSYS_PLACIDUS) -> Tuple[List[float], List[float], int]:
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
    
    return cusps, ascmc, 0

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

def close() -> None:
    """Close Swiss Ephemeris resources"""
    logger.info("Mock Swiss Ephemeris close called") 