"""Tests for mock Swiss Ephemeris implementation"""
import pytest
from datetime import datetime
from api.services.mock_swisseph import (
    set_ephe_path, set_sid_mode, julday, get_ayanamsa,
    calc_ut, houses_ex, USE_MOCK, SUN, MOON, MEAN_NODE
)

def test_mock_disabled_by_default():
    """Test that mock is disabled by default"""
    assert not USE_MOCK

def test_set_ephe_path():
    """Test setting ephemeris path"""
    set_ephe_path("/test/path")
    # No assertion needed as this is just a mock

def test_set_sid_mode():
    """Test setting sidereal mode"""
    set_sid_mode(1)  # Lahiri
    # No assertion needed as this is just a mock

def test_julday_calculation():
    """Test Julian day calculation"""
    # Test with a known date
    jd = julday(2000, 1, 1, 12.0)
    assert isinstance(jd, float)
    assert jd > 2451545.0  # Should be after J2000

def test_get_ayanamsa():
    """Test ayanamsa calculation"""
    jd = julday(2000, 1, 1, 12.0)
    ayanamsa = get_ayanamsa(jd)
    assert isinstance(ayanamsa, float)
    assert 23.0 < ayanamsa < 24.0  # Should be in reasonable range

def test_calc_ut_sun_moon():
    """Test planet position calculation for Sun and Moon"""
    jd = julday(2000, 1, 1, 12.0)
    
    # Test Sun
    sun_pos = calc_ut(jd, SUN)
    assert len(sun_pos) == 6
    assert 0 <= sun_pos[0] < 360  # Longitude
    assert sun_pos[3] > 0  # Speed should be positive
    
    # Test Moon
    moon_pos = calc_ut(jd, MOON)
    assert len(moon_pos) == 6
    assert 0 <= moon_pos[0] < 360  # Longitude
    assert moon_pos[3] > 0  # Speed should be positive

def test_calc_ut_rahu():
    """Test Rahu position calculation"""
    jd = julday(2000, 1, 1, 12.0)
    rahu_pos = calc_ut(jd, MEAN_NODE)
    assert len(rahu_pos) == 6
    assert 0 <= rahu_pos[0] < 360  # Longitude
    assert rahu_pos[3] < 0  # Speed should be negative (retrograde)

def test_houses_ex():
    """Test house calculation"""
    jd = julday(2000, 1, 1, 12.0)
    houses, ascmc = houses_ex(jd, 0.0, 0.0, "P")
    
    # Check house cusps
    assert len(houses) == 13  # 12 houses + placeholder
    assert all(0 <= cusp < 360 for cusp in houses[1:])  # All cusps in valid range
    
    # Check special points
    assert len(ascmc) == 4
    assert all(0 <= point < 360 for point in ascmc)  # All points in valid range

def test_mock_disabled_raises_error():
    """Test that mock functions raise error when disabled"""
    jd = julday(2000, 1, 1, 12.0)
    
    with pytest.raises(RuntimeError):
        calc_ut(jd, SUN)
    
    with pytest.raises(RuntimeError):
        get_ayanamsa(jd)
    
    with pytest.raises(RuntimeError):
        houses_ex(jd, 0.0, 0.0, "P") 