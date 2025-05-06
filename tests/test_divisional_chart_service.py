"""
Tests for the divisional chart service.
"""

import math
import pytest
from typing import Dict, Any, List

from jai_api.services import divisional_chart_service
from jai_api.constants import load_all_constants, get_constant
from jai_api.constants.divisional_mappings import DIVISIONAL_MAPPINGS
from jai_api.utils.custom_exceptions import MappingNotFoundError, CalculationError

# Load constants before tests
load_all_constants()

# Test fixture for sample natal chart data
@pytest.fixture
def sample_natal_positions():
    """Provide sample natal positions for testing"""
    return [
        {
            "planet": "Sun",
            "longitude": 280.5,  # 280.5° = 10th sign (Capricorn) at 10.5°
            "sign_index": 10,
            "sign_name": "Capricorn",
            "house": 10,
            "is_retrograde": False
        },
        {
            "planet": "Moon",
            "longitude": 125.75,  # 125.75° = 5th sign (Leo) at 5.75°
            "sign_index": 5,
            "sign_name": "Leo",
            "house": 5,
            "is_retrograde": False
        },
        {
            "planet": "Mars",
            "longitude": 59.2,  # 59.2° = 3rd sign (Gemini) at 29.2°
            "sign_index": 3,
            "sign_name": "Gemini",
            "house": 3,
            "is_retrograde": False
        },
        {
            "planet": "Mercury",
            "longitude": 275.0,  # 275° = 10th sign (Capricorn) at 5°
            "sign_index": 10,
            "sign_name": "Capricorn",
            "house": 10,
            "is_retrograde": True
        },
        {
            "planet": "Jupiter",
            "longitude": 190.3,  # 190.3° = 7th sign (Libra) at 10.3°
            "sign_index": 7,
            "sign_name": "Libra",
            "house": 7,
            "is_retrograde": False
        }
    ]

def test_divisional_span():
    """Test calculation of divisional span"""
    # Test for D9 (Navamsa)
    span = divisional_chart_service.get_divisional_span(9)
    assert span == pytest.approx(3.333333)
    
    # Test for D12 (Dwadasamsa)
    span = divisional_chart_service.get_divisional_span(12)
    assert span == pytest.approx(2.5)
    
    # Test for D30 (Trimshamsha)
    span = divisional_chart_service.get_divisional_span(30)
    assert span == pytest.approx(1.0)

def test_is_divisional_chart_supported():
    """Test checking which divisional charts are supported"""
    # These should be supported
    assert divisional_chart_service.is_divisional_chart_supported("D1")
    assert divisional_chart_service.is_divisional_chart_supported("D9")
    
    # These should not be supported
    assert not divisional_chart_service.is_divisional_chart_supported("D12")
    assert not divisional_chart_service.is_divisional_chart_supported("D27")
    assert not divisional_chart_service.is_divisional_chart_supported("invalid")

def test_map_to_divisional_sign():
    """Test mapping from natal sign to divisional sign"""
    # Using D9 mapping
    d9_mapping = DIVISIONAL_MAPPINGS["D9"]
    
    # Test various mappings
    # Aries 1st division → Aries
    result = divisional_chart_service.map_to_divisional_sign(1, 1, d9_mapping)
    assert result == 1
    
    # Taurus 2nd division → Aquarius
    result = divisional_chart_service.map_to_divisional_sign(2, 2, d9_mapping)
    assert result == 11
    
    # Gemini 9th division → Gemini
    result = divisional_chart_service.map_to_divisional_sign(3, 9, d9_mapping)
    assert result == 3
    
    # Test with invalid values
    with pytest.raises(CalculationError):
        divisional_chart_service.map_to_divisional_sign(1, 10, d9_mapping)  # Invalid division
    
    with pytest.raises(CalculationError):
        divisional_chart_service.map_to_divisional_sign(13, 1, d9_mapping)  # Invalid sign

def test_calculate_divisional_chart(sample_natal_positions):
    """Test calculation of D9 chart positions"""
    # Calculate D9 chart with ascendant in Aries (1)
    result = divisional_chart_service.calculate_divisional_chart(
        sample_natal_positions,
        9,  # D9 chart
        1   # Ascendant in Aries
    )
    
    # Basic validation
    assert isinstance(result, list)
    assert len(result) == len(sample_natal_positions)
    
    # Check structure of each planet
    for planet_info in result:
        assert isinstance(planet_info, dict)
        assert "planet" in planet_info
        assert "divisional_sign_index" in planet_info
        assert "divisional_sign_name" in planet_info
        assert "divisional_house" in planet_info
        assert "is_retrograde" in planet_info
        
        # Sign index should be between 1 and 12
        assert 1 <= planet_info["divisional_sign_index"] <= 12
        
        # House should be calculated correctly based on ascendant
        expected_house = ((planet_info["divisional_sign_index"] - 1) % 12) + 1
        assert planet_info["divisional_house"] == expected_house

def test_d9_specific_mappings(sample_natal_positions):
    """Test specific D9 mappings for accuracy"""
    # Calculate D9 chart
    d9_positions = divisional_chart_service.calculate_divisional_chart(
        sample_natal_positions,
        9,
        1  # Ascendant in Aries
    )
    
    # Get specific planets
    sun = next((p for p in d9_positions if p["planet"] == "Sun"), None)
    moon = next((p for p in d9_positions if p["planet"] == "Moon"), None)
    mars = next((p for p in d9_positions if p["planet"] == "Mars"), None)
    
    # Verify specific mappings
    
    # Sun at 280.5° (Capricorn 10.5°)
    # In D9, each division is 3.33°, so this is the 4th division
    # Capricorn 4th division maps to Aries
    assert sun is not None
    assert sun["divisional_sign_index"] == 1  # Aries
    
    # Moon at 125.75° (Leo 5.75°)
    # In D9, this is the 2nd division
    # Leo 2nd division maps to Taurus
    assert moon is not None
    assert moon["divisional_sign_index"] == 2  # Taurus
    
    # Mars at 59.2° (Gemini 29.2°)
    # In D9, this is the 9th division
    # Gemini 9th division maps to Gemini
    assert mars is not None
    assert mars["divisional_sign_index"] == 3  # Gemini

def test_unsupported_chart():
    """Test behavior with unsupported charts"""
    with pytest.raises(MappingNotFoundError):
        divisional_chart_service.calculate_divisional_chart(
            [],  # Empty natal positions
            12,  # D12 chart (not implemented yet)
            1    # Ascendant
        ) 