"""
Mock implementation of Swiss Ephemeris for development purposes
This file contains basic functionality to simulate the Swiss Ephemeris library
"""
import math
import random
from datetime import datetime
import logging
from typing import List, Tuple
from api.models.astrological import Planet, Sign

# Configure logging
logger = logging.getLogger("jai-api.mock_swisseph")

# Debug flag to control mock usage
USE_MOCK = False

# Constants for planetary indices (Vedic planets only)
SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
MEAN_NODE = 7  # Rahu

# Constants for ayanamsa options
SIDM_LAHIRI = 1
SIDM_RAMAN = 2
SIDM_KRISHNAMURTI = 3

# Global state
_ephe_path = "./ephemeris"
_sid_mode = SIDM_LAHIRI

def set_ephe_path(path):
    """Set ephemeris path - mock implementation"""
    global _ephe_path
    _ephe_path = path
    if USE_MOCK:
        logger.info(f"Mock: Set ephemeris path to {path}")

def set_sid_mode(mode):
    """Set sidereal mode - mock implementation"""
    global _sid_mode
    _sid_mode = mode
    if USE_MOCK:
        logger.info(f"Mock: Set ayanamsa mode to {mode}")

def julday(year, month, day, hour):
    """Calculate Julian day number - simplified implementation"""
    if not USE_MOCK:
        raise RuntimeError("Mock Swiss Ephemeris is disabled")
        
    dt = datetime(year, month, day, int(hour), int((hour*60) % 60), int((hour*3600) % 60))
    # Simplified Julian day calculation
    jd = 2451545.0 + (dt - datetime(2000, 1, 1, 12, 0, 0)).total_seconds() / 86400.0
    logger.debug(f"Mock: Calculated JD {jd} for {year}-{month}-{day} {hour}h")
    return jd

def get_ayanamsa(jd):
    """Get ayanamsa value - mock implementation"""
    if not USE_MOCK:
        raise RuntimeError("Mock Swiss Ephemeris is disabled")
        
    # Different offsets based on ayanamsa system
    if _sid_mode == SIDM_LAHIRI:
        offset = 23.85
    elif _sid_mode == SIDM_KRISHNAMURTI:
        offset = 23.86
    elif _sid_mode == SIDM_RAMAN:
        offset = 23.88
    else:
        offset = 23.85  # Default
    
    # Slight adjustment based on Julian day
    offset += (jd - 2451545.0) * 0.0001
    return offset

def calc_ut(jd, planet_id):
    """Calculate planetary position - mock implementation"""
    if not USE_MOCK:
        raise RuntimeError("Mock Swiss Ephemeris is disabled")
        
    # Base longitude calculation using simple simulation
    base_long = (jd % 365.25) * (360/365.25)
    
    # Add offsets for different planets (Vedic planets only)
    planet_offsets = {
        SUN: 0,
        MOON: base_long * 12,  # Moon moves ~12x faster
        MERCURY: 30,
        VENUS: 60,
        MARS: 120,
        JUPITER: 180,
        SATURN: 240,
        MEAN_NODE: 150
    }
    
    # Add the planet-specific offset
    longitude = (base_long + planet_offsets.get(planet_id, 0)) % 360
    
    # Add some random variation to make it seem less mechanical
    longitude += random.uniform(-2, 2)
    longitude %= 360
    
    # Calculate other parameters
    latitude = random.uniform(-2, 2) if planet_id != SUN else 0
    distance = 1.0 + random.uniform(0, 0.1)
    
    # Calculate speed (negative for retrograde)
    if planet_id in [SUN, MOON]:
        speed = random.uniform(0.5, 1.0)  # Never retrograde
    elif planet_id == MEAN_NODE:
        speed = random.uniform(-0.5, -0.1)  # Always retrograde
    else:
        speed = random.uniform(-0.5, 1.5)
        if random.random() < 0.2:
            speed *= -1  # 20% chance of retrograde for other planets
    
    return [longitude, latitude, distance, speed, 0, 0]

def houses_ex(jd, lat, lon, hsys):
    """Calculate houses - mock implementation"""
    if not USE_MOCK:
        raise RuntimeError("Mock Swiss Ephemeris is disabled")
        
    # Create house cusps
    houses_cusps = [0]  # 1-based index, so add a placeholder at 0
    
    # Calculate ascendant (first house cusp)
    asc_longitude = (jd % 365.25) * (360/365.25)
    houses_cusps.append(asc_longitude)
    
    # Calculate other house cusps 
    for i in range(2, 13):
        # Simple 30-degree houses
        cusp = (asc_longitude + (i-1) * 30) % 360
        houses_cusps.append(cusp)
    
    # Calculate special points
    ascmc = [
        asc_longitude,
        (asc_longitude + 270) % 360,  # MC is roughly opposite side
        (asc_longitude + 90) % 360,   # ARMC
        (asc_longitude + 45) % 360,   # Vertex - simplified
    ]
    
    return houses_cusps, ascmc 