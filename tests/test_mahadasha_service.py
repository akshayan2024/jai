"""
Tests for the mahadasha service.
"""

import math
import pytest
from datetime import datetime, timedelta
from typing import Dict, Any, List

from jai_api.services import mahadasha_service
from jai_api.constants import load_all_constants, get_constant
from jai_api.constants.ayanamsa import AYANAMSA_LAHIRI
from jai_api.utils.custom_exceptions import CalculationError

# Load constants before tests
load_all_constants()

@pytest.fixture
def sample_birth_data():
    """Provide sample birth data for testing"""
    return {
        # Sample birth data with Moon in different nakshatras
        "birth_data_1": {
            "julian_day": 2451545.0,  # Jan 1, 2000, 12:00 UTC
            "birth_date": "2000-01-01"
        },
        "birth_data_2": {
            "julian_day": 2446262.14583,  # July 15, 1985, 15:30 UTC
            "birth_date": "1985-07-15"
        }
    }

def test_get_balance_years():
    """Test calculation of balance years in current mahadasha"""
    # Test with specific Julian day where Moon is at known position
    julian_day = 2451545.0  # Example date
    
    # Calculate balance
    planet, balance_years = mahadasha_service.get_balance_years(julian_day, AYANAMSA_LAHIRI)
    
    # Basic validation
    assert isinstance(planet, str)
    assert isinstance(balance_years, float)
    
    # Balance should be between 0 and the maximum years for the planet
    dasha_years = get_constant('dasha_years')
    planet_names = {planet["name"]: idx for idx, planet in get_constant('planets').items()}
    planet_idx = planet_names.get(planet)
    
    max_years = dasha_years[planet_idx]
    assert 0 <= balance_years <= max_years

def test_calculate_mahadasha(sample_birth_data):
    """Test calculation of mahadasha periods"""
    # Use the first birth data sample
    data = sample_birth_data["birth_data_1"]
    
    # Calculate mahadasha
    result = mahadasha_service.calculate_mahadasha(
        data["julian_day"], 
        data["birth_date"],
        AYANAMSA_LAHIRI
    )
    
    # Basic validation
    assert isinstance(result, dict)
    assert "moon" in result
    assert "mahadashas" in result
    
    # Check moon data
    moon_data = result["moon"]
    assert "longitude" in moon_data
    assert "nakshatra_index" in moon_data
    assert "nakshatra_name" in moon_data
    assert "nakshatra_lord" in moon_data
    
    # Check mahadasha structure
    mahadashas = result["mahadashas"]
    assert isinstance(mahadashas, list)
    assert len(mahadashas) == 9  # Should have 9 periods (one for each planet)
    
    # Check structure of each period
    for period in mahadashas:
        assert "planet" in period
        assert "start_date" in period
        assert "end_date" in period
        assert "years" in period
        
        # Validate date format
        start_date = datetime.strptime(period["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(period["end_date"], "%Y-%m-%d")
        
        # End date should be after start date
        assert end_date > start_date
        
        # Planet should be one of the valid planets
        planet_names = [p["name"] for p in get_constant("planets").values()]
        assert period["planet"] in planet_names

def test_mahadasha_sequence(sample_birth_data):
    """Test that mahadasha periods follow the correct sequence"""
    # Use the second birth data sample
    data = sample_birth_data["birth_data_2"]
    
    result = mahadasha_service.calculate_mahadasha(
        data["julian_day"], 
        data["birth_date"], 
        AYANAMSA_LAHIRI
    )
    
    # Get the periods
    periods = result["mahadashas"]
    
    # Each period's start date should be the previous period's end date
    for i in range(1, len(periods)):
        assert periods[i]["start_date"] == periods[i-1]["end_date"]
    
    # First period's balance should be less than the full period
    # for that planet, others should be full
    nakshatra_lord = result["moon"]["nakshatra_lord"]
    first_period = periods[0]
    assert first_period["planet"] == nakshatra_lord
    
    # First period should have partial years, others should have full years
    planets = get_constant('planets')
    dasha_years = get_constant('dasha_years')
    planet_names = {planet["name"]: idx for idx, planet in planets.items()}
    
    for i, period in enumerate(periods):
        planet_idx = planet_names[period["planet"]]
        
        if i == 0:  # First period (partial)
            assert period["years"] < dasha_years[planet_idx]
        else:  # Full periods
            assert period["years"] == dasha_years[planet_idx]

def test_calculate_antardasha():
    """Test calculation of antardasha periods"""
    # Create a sample mahadasha period
    mahadasha_period = {
        "planet": "Sun",
        "start_date": "2000-01-01",
        "end_date": "2006-01-01",
        "years": 6
    }
    
    # Calculate antardashas
    result = mahadasha_service.calculate_antardasha(mahadasha_period)
    
    # Basic validation
    assert isinstance(result, dict)
    assert "antardashas" in result
    
    antardashas = result["antardashas"]
    assert isinstance(antardashas, list)
    assert len(antardashas) == 9  # Should have 9 sub-periods
    
    # Check structure of each sub-period
    for sub_period in antardashas:
        assert "planet" in sub_period
        assert "start_date" in sub_period
        assert "end_date" in sub_period
        assert "months" in sub_period
        
        # Validate date format
        start_date = datetime.strptime(sub_period["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(sub_period["end_date"], "%Y-%m-%d")
        
        # End date should be after start date
        assert end_date > start_date
    
    # First antardasha should start on mahadasha start date
    assert antardashas[0]["start_date"] == mahadasha_period["start_date"]
    
    # Last antardasha should end on mahadasha end date
    assert antardashas[-1]["end_date"] == mahadasha_period["end_date"]
    
    # Each sub-period's start date should be the previous period's end date
    for i in range(1, len(antardashas)):
        assert antardashas[i]["start_date"] == antardashas[i-1]["end_date"]
    
    # First antardasha should be the same planet as the mahadasha
    assert antardashas[0]["planet"] == mahadasha_period["planet"]

def test_antardasha_proportions():
    """Test that antardasha durations are proportional to mahadasha years"""
    # Create a sample mahadasha period
    mahadasha_period = {
        "planet": "Jupiter",
        "start_date": "2000-01-01",
        "end_date": "2016-01-01",
        "years": 16
    }
    
    # Calculate antardashas
    result = mahadasha_service.calculate_antardasha(mahadasha_period)
    antardashas = result["antardashas"]
    
    # Get dasha years for each planet
    dasha_years = get_constant('dasha_years')
    planets = get_constant('planets')
    planet_names = {planet["name"]: idx for idx, planet in planets.items()}
    
    # Check that each sub-period duration is proportional
    total_months = 0
    for sub_period in antardashas:
        planet_idx = planet_names[sub_period["planet"]]
        planet_years = dasha_years[planet_idx]
        
        # Calculate expected proportion
        expected_proportion = planet_years / 120.0
        expected_months = mahadasha_period["years"] * 12 * expected_proportion
        
        # Allow small rounding differences
        assert abs(sub_period["months"] - expected_months) < 0.2
        
        total_months += sub_period["months"]
    
    # Total months should equal mahadasha years * 12
    assert abs(total_months - (mahadasha_period["years"] * 12)) < 0.5 