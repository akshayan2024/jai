"""
Tests for input validation utilities.
"""
import pytest
from datetime import datetime, timedelta
from api.utils.input_validation import (
    validate_date_range,
    validate_coordinates,
    validate_house_system,
    validate_ayanamsa,
    validate_planet,
    validate_extreme_latitude,
    CalculationInput,
    ValidationError
)

def test_validate_date_range_valid():
    """Test valid date range validation."""
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2000, 1, 2)
    validate_date_range(start_date, end_date)  # Should not raise

def test_validate_date_range_invalid_order():
    """Test date range validation with invalid order."""
    start_date = datetime(2000, 1, 2)
    end_date = datetime(2000, 1, 1)
    with pytest.raises(ValidationError) as exc_info:
        validate_date_range(start_date, end_date)
    assert "Start date must be before end date" in str(exc_info.value)

def test_validate_date_range_out_of_bounds():
    """Test date range validation with out of bounds dates."""
    start_date = datetime(1899, 1, 1)
    end_date = datetime(2000, 1, 1)
    with pytest.raises(ValidationError) as exc_info:
        validate_date_range(start_date, end_date)
    assert "Date range must be between" in str(exc_info.value)

def test_validate_coordinates_valid():
    """Test valid coordinate validation."""
    validate_coordinates(0.0, 0.0)  # Should not raise
    validate_coordinates(45.0, -120.0)  # Should not raise
    validate_coordinates(-45.0, 120.0)  # Should not raise

def test_validate_coordinates_invalid_latitude():
    """Test coordinate validation with invalid latitude."""
    with pytest.raises(ValidationError) as exc_info:
        validate_coordinates(91.0, 0.0)
    assert "Latitude must be between" in str(exc_info.value)

def test_validate_coordinates_invalid_longitude():
    """Test coordinate validation with invalid longitude."""
    with pytest.raises(ValidationError) as exc_info:
        validate_coordinates(0.0, 181.0)
    assert "Longitude must be between" in str(exc_info.value)

def test_validate_coordinates_non_numeric():
    """Test coordinate validation with non-numeric values."""
    with pytest.raises(ValidationError) as exc_info:
        validate_coordinates("45.0", 0.0)
    assert "Coordinates must be numeric values" in str(exc_info.value)

def test_validate_house_system_valid():
    """Test valid house system validation."""
    validate_house_system('W')  # Should not raise
    validate_house_system('P')  # Should not raise
    validate_house_system('K')  # Should not raise

def test_validate_house_system_invalid():
    """Test house system validation with invalid system."""
    with pytest.raises(ValidationError) as exc_info:
        validate_house_system('X')
    assert "Invalid house system" in str(exc_info.value)

def test_validate_ayanamsa_valid():
    """Test valid ayanamsa validation."""
    validate_ayanamsa(1)  # Lahiri
    validate_ayanamsa(0)  # Fagan/Bradley
    validate_ayanamsa(3)  # Raman

def test_validate_ayanamsa_invalid():
    """Test ayanamsa validation with invalid value."""
    with pytest.raises(ValidationError) as exc_info:
        validate_ayanamsa(999)
    assert "Invalid ayanamsa" in str(exc_info.value)

def test_validate_planet_valid():
    """Test valid planet validation."""
    validate_planet(0)  # Sun
    validate_planet(1)  # Moon
    validate_planet(2)  # Mercury

def test_validate_planet_invalid():
    """Test planet validation with invalid value."""
    with pytest.raises(ValidationError) as exc_info:
        validate_planet(999)
    assert "Invalid planet" in str(exc_info.value)

def test_validate_extreme_latitude_valid():
    """Test valid extreme latitude validation."""
    validate_extreme_latitude(0.0)  # Should not raise
    validate_extreme_latitude(45.0)  # Should not raise
    validate_extreme_latitude(-45.0)  # Should not raise

def test_validate_extreme_latitude_invalid():
    """Test extreme latitude validation with invalid value."""
    with pytest.raises(ValidationError) as exc_info:
        validate_extreme_latitude(67.0)
    assert "House calculations may be inaccurate" in str(exc_info.value)

def test_calculation_input_valid():
    """Test valid calculation input validation."""
    input_data = {
        'date': datetime(2000, 1, 1),
        'latitude': 45.0,
        'longitude': -120.0,
        'house_system': 'W',
        'ayanamsa': 1
    }
    calc_input = CalculationInput(**input_data)
    assert calc_input.date == input_data['date']
    assert calc_input.latitude == input_data['latitude']
    assert calc_input.longitude == input_data['longitude']
    assert calc_input.house_system == input_data['house_system']
    assert calc_input.ayanamsa == input_data['ayanamsa']

def test_calculation_input_invalid_date():
    """Test calculation input validation with invalid date."""
    input_data = {
        'date': datetime(1899, 1, 1),
        'latitude': 45.0,
        'longitude': -120.0,
        'house_system': 'W',
        'ayanamsa': 1
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationInput(**input_data)
    assert "Date must be between" in str(exc_info.value)

def test_calculation_input_invalid_coordinates():
    """Test calculation input validation with invalid coordinates."""
    input_data = {
        'date': datetime(2000, 1, 1),
        'latitude': 91.0,
        'longitude': -120.0,
        'house_system': 'W',
        'ayanamsa': 1
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationInput(**input_data)
    assert "Latitude must be between" in str(exc_info.value)

def test_calculation_input_invalid_house_system():
    """Test calculation input validation with invalid house system."""
    input_data = {
        'date': datetime(2000, 1, 1),
        'latitude': 45.0,
        'longitude': -120.0,
        'house_system': 'X',
        'ayanamsa': 1
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationInput(**input_data)
    assert "Invalid house system" in str(exc_info.value)

def test_calculation_input_invalid_ayanamsa():
    """Test calculation input validation with invalid ayanamsa."""
    input_data = {
        'date': datetime(2000, 1, 1),
        'latitude': 45.0,
        'longitude': -120.0,
        'house_system': 'W',
        'ayanamsa': 999
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationInput(**input_data)
    assert "Invalid ayanamsa" in str(exc_info.value) 