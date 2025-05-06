"""
Tests for the natal chart service.
"""

import math
import pytest
from typing import Dict, Any

from jai_api.services import natal_chart_service
from jai_api.constants import load_all_constants, get_constant
from jai_api.constants.ayanamsa import AYANAMSA_LAHIRI

# Load constants before tests
load_all_constants()

# Test fixture for birth data
@pytest.fixture
def sample_birth_data():
    """Provide sample birth data for testing"""
    return {
        # Jan 1, 2000, 12:00 UTC, Delhi
        "birth_data_1": {
            "julian_day": 2451545.0,
            "ascendant_sign": 4,  # Example ascendant (Cancer)
        },
        # July 15, 1985, 15:30 UTC, New York
        "birth_data_2": {
            "julian_day": 2446262.14583,  
            "ascendant_sign": 9,  # Example ascendant (Sagittarius)
        }
    }

def test_calculate_natal_chart(sample_birth_data):
    """Test natal chart calculation with sample data"""
    # Use the first birth data sample
    data = sample_birth_data["birth_data_1"]
    
    # Calculate natal chart
    result = natal_chart_service.calculate_natal_chart(
        data["julian_day"], 
        data["ascendant_sign"],
        AYANAMSA_LAHIRI
    )
    
    # Basic validation
    assert isinstance(result, list)
    assert len(result) == 9  # 9 planets should be returned
    
    # Check structure of each planet
    for planet_info in result:
        assert isinstance(planet_info, dict)
        assert "planet" in planet_info
        assert "longitude" in planet_info
        assert "sign_index" in planet_info
        assert "sign_name" in planet_info
        assert "house" in planet_info
        assert "is_retrograde" in planet_info
        
        # Planet should be one of the valid planets
        planet_names = [p["name"] for p in get_constant("planets").values()]
        assert planet_info["planet"] in planet_names
        
        # Sign index should be between 1 and 12
        assert 1 <= planet_info["sign_index"] <= 12
        
        # Longitude should be between 0 and 360
        assert 0 <= planet_info["longitude"] < 360

def test_ketu_calculation(sample_birth_data):
    """Test Ketu (South Node) calculation specifically"""
    # Use the second birth data sample
    data = sample_birth_data["birth_data_2"]
    
    # Calculate natal chart
    result = natal_chart_service.calculate_natal_chart(
        data["julian_day"], 
        data["ascendant_sign"],
        AYANAMSA_LAHIRI
    )
    
    # Extract Rahu and Ketu
    rahu = next((p for p in result if p["planet"] == "Rahu"), None)
    ketu = next((p for p in result if p["planet"] == "Ketu"), None)
    
    # Both should exist
    assert rahu is not None
    assert ketu is not None
    
    # Ketu should be 180° from Rahu (with small float precision allowance)
    expected_ketu_longitude = (rahu["longitude"] + 180) % 360
    assert abs(ketu["longitude"] - expected_ketu_longitude) < 0.0001
    
    # Their signs should be 7 houses apart (opposite)
    assert (ketu["sign_index"] - rahu["sign_index"]) % 12 == 6 or (rahu["sign_index"] - ketu["sign_index"]) % 12 == 6

def test_house_calculation():
    """Test house calculation for planets"""
    # Test various combinations
    test_cases = [
        {"planet_sign": 1, "ascendant_sign": 1, "expected_house": 1},  # Same sign
        {"planet_sign": 7, "ascendant_sign": 1, "expected_house": 7},  # 7th house
        {"planet_sign": 1, "ascendant_sign": 12, "expected_house": 2},  # Wrap around
        {"planet_sign": 3, "ascendant_sign": 10, "expected_house": 6},  # Arbitrary case
    ]
    
    for case in test_cases:
        result = natal_chart_service.calculate_planet_house(
            case["planet_sign"], 
            case["ascendant_sign"]
        )
        assert result == case["expected_house"]

def test_natal_chart_consistency(sample_birth_data):
    """Test that planet positions in houses are consistent with their signs"""
    # Use the first birth data sample
    data = sample_birth_data["birth_data_1"]
    ascendant_sign = data["ascendant_sign"]
    
    # Calculate natal chart
    chart = natal_chart_service.calculate_natal_chart(
        data["julian_day"], 
        ascendant_sign,
        AYANAMSA_LAHIRI
    )
    
    # Get houses
    from jai_api.services.ascendant_service import get_houses
    houses = get_houses(ascendant_sign)
    
    # Check each planet's house matches its sign according to house system
    for planet_info in chart:
        sign_index = planet_info["sign_index"]
        house = planet_info["house"]
        
        # In Whole Sign system, verify house placement
        # The house number corresponds to the index where the sign appears in houses
        house_from_sign = houses.index(sign_index) if sign_index in houses else 0
        assert house == house_from_sign 