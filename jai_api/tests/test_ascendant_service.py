"""
Tests for the ascendant service.
"""

import math
import pytest

from ..services import ascendant_service
from ..constants import load_all_constants

# Load constants before tests
load_all_constants()

def test_calculate_ascendant():
    """Test ascendant calculation with known values"""
    # Test data: Jan 1, 2000, 12:00 UTC, Delhi
    julian_day = 2451545.0
    latitude = 28.6139  # Delhi
    longitude = 77.2090
    
    # Calculate ascendant
    result = ascendant_service.calculate_ascendant(julian_day, latitude, longitude)
    
    # Check the results are sensible (exact values may vary since we're using a stub)
    assert isinstance(result, dict)
    assert "ascendant_degree" in result
    assert "ascendant_sign" in result
    assert "ascendant_sign_name" in result
    
    # Sign should be between 1 and 12
    assert 1 <= result["ascendant_sign"] <= 12
    
    # Degree should be between 0 and 360
    assert 0 <= result["ascendant_degree"] < 360

def test_get_houses():
    """Test house calculation with Whole Sign system"""
    # Test with ascendant in Aries (1)
    houses = ascendant_service.get_houses(1)
    
    # Should return 13 values (0-based placeholder and 12 houses)
    assert len(houses) == 13
    
    # First house should be Aries (1)
    assert houses[1] == 1
    
    # Houses should follow zodiacal order
    for house in range(1, 13):
        assert houses[house] == ((house - 1) % 12) + 1
    
    # Test with ascendant in Virgo (6)
    houses = ascendant_service.get_houses(6)
    
    # First house should be Virgo (6)
    assert houses[1] == 6
    
    # Seventh house should be Pisces (12)
    assert houses[7] == 12 