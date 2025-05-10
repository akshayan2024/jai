"""
Tests for Vedic house calculations to verify correct house-sign relationships.

These tests check that when a specific ascendant is given, the houses follow
the correct sequencing according to the Vedic Whole Sign house system.
"""
import pytest
import logging
import sys
from datetime import datetime
from api.services.calculation import (
    calculate_ascendant, 
    calculate_planets, 
    calculate_houses,
    validate_d1_chart,
    ZODIAC_SIGNS
)

# Set up logging for tests
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("test_vedic_houses")

# Test data for different ascendants
TEST_CASES = [
    # Aries Ascendant (Sign 0)
    {
        "name": "Aries Ascendant",
        "birth_date": "2023-04-01",
        "birth_time": "12:00:00",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "timezone_offset": 5.5,
        "expected_asc_sign": "Aries",
        "expected_house_signs": {
            1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
            5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
            9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
        }
    },
    # Capricorn Ascendant (Sign 9)
    {
        "name": "Capricorn Ascendant", 
        "birth_date": "2023-01-05",
        "birth_time": "07:30:00",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "timezone_offset": 5.5,
        "expected_asc_sign": "Capricorn",
        "expected_house_signs": {
            1: "Capricorn", 2: "Aquarius", 3: "Pisces", 4: "Aries",
            5: "Taurus", 6: "Gemini", 7: "Cancer", 8: "Leo",
            9: "Virgo", 10: "Libra", 11: "Scorpio", 12: "Sagittarius"
        }
    }
]

def test_house_sign_relationships():
    """
    Test that houses follow the correct sign sequence for various ascendants.
    
    In Vedic Whole Sign house system:
    - The 1st house is always the same sign as the ascendant
    - Each house corresponds to one complete sign
    - Houses follow the natural sequence of signs from the ascendant
    """
    logger.info("Starting Vedic house calculations tests")
    
    for test_case in TEST_CASES:
        logger.info(f"Testing {test_case['name']}")
        
        # Calculate ascendant
        ascendant = calculate_ascendant(
            birth_date=test_case['birth_date'],
            birth_time=test_case['birth_time'],
            latitude=test_case['latitude'],
            longitude=test_case['longitude'],
            timezone_offset=test_case['timezone_offset'],
            ayanamsa="lahiri"
        )
        
        # Verify ascendant sign
        assert ascendant.sign == test_case['expected_asc_sign'], \
            f"Expected ascendant {test_case['expected_asc_sign']}, got {ascendant.sign}"
        
        # Calculate houses
        houses = calculate_houses(
            birth_date=test_case['birth_date'],
            birth_time=test_case['birth_time'],
            latitude=test_case['latitude'],
            longitude=test_case['longitude'],
            timezone_offset=test_case['timezone_offset'],
            ayanamsa="lahiri"
        )
        
        # Verify house-sign relationships
        for house in houses:
            expected_sign = test_case['expected_house_signs'][house.house_number]
            assert house.sign == expected_sign, \
                f"House {house.house_number}: Expected {expected_sign}, got {house.sign}"
        
        # Calculate planets
        planets = calculate_planets(
            birth_date=test_case['birth_date'],
            birth_time=test_case['birth_time'],
            latitude=test_case['latitude'],
            longitude=test_case['longitude'],
            timezone_offset=test_case['timezone_offset'],
            ayanamsa="lahiri"
        )
        
        # Validate complete D1 chart
        validate_d1_chart(ascendant, planets, houses)
        
        logger.info(f"Test case {test_case['name']} passed!")
    
    logger.info("All tests passed successfully!") 