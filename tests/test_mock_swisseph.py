"""Tests for the mock Swiss Ephemeris implementation"""

import pytest
from api.services.mock_swisseph import (
    set_ephe_path,
    set_sid_mode,
    julday,
    get_ayanamsa,
    calc_ut,
    houses_ex,
    enable_mock,
    disable_mock,
    is_mock_enabled,
    SUN,
    MOON,
    MERCURY,
    VENUS,
    MARS,
    JUPITER,
    SATURN,
    MEAN_NODE,
    SIDM_LAHIRI,
    HSYS_WHOLE_SIGN
)

def test_mock_disabled_by_default():
    """Test that mock is disabled by default"""
    assert not is_mock_enabled()

def test_set_ephe_path():
    """Test setting ephemeris path"""
    set_ephe_path("./test_ephemeris")
    # No assertion needed as this is just a mock

def test_set_sid_mode():
    """Test setting sidereal mode"""
    set_sid_mode(SIDM_LAHIRI)
    # No assertion needed as this is just a mock

def test_julday_calculation():
    """Test Julian day calculation"""
    enable_mock()
    jd = julday(2000, 1, 1, 0)
    assert isinstance(jd, float)
    assert jd > 2451545.0  # Should be after J2000
    disable_mock()

def test_get_ayanamsa():
    """Test ayanamsa calculation"""
    enable_mock()
    jd = julday(2000, 1, 1, 0)
    ayanamsa = get_ayanamsa(jd)
    assert isinstance(ayanamsa, float)
    assert 23.0 <= ayanamsa <= 24.0  # Should be around 23.85
    disable_mock()

def test_calc_ut_sun_moon():
    """Test position calculation for Sun and Moon"""
    enable_mock()
    jd = julday(2000, 1, 1, 0)
    
    # Test Sun position
    sun_pos = calc_ut(jd, SUN)
    assert len(sun_pos) == 4
    assert isinstance(sun_pos[0], float)  # Longitude
    assert isinstance(sun_pos[1], float)  # Latitude
    assert isinstance(sun_pos[2], float)  # Distance
    assert isinstance(sun_pos[3], float)  # Speed
    
    # Test Moon position
    moon_pos = calc_ut(jd, MOON)
    assert len(moon_pos) == 4
    assert isinstance(moon_pos[0], float)
    assert isinstance(moon_pos[1], float)
    assert isinstance(moon_pos[2], float)
    assert isinstance(moon_pos[3], float)
    
    disable_mock()

def test_calc_ut_rahu():
    """Test position calculation for Rahu (Mean Node)"""
    enable_mock()
    jd = julday(2000, 1, 1, 0)
    
    rahu_pos = calc_ut(jd, MEAN_NODE)
    assert len(rahu_pos) == 4
    assert isinstance(rahu_pos[0], float)
    assert isinstance(rahu_pos[1], float)
    assert isinstance(rahu_pos[2], float)
    assert isinstance(rahu_pos[3], float)
    assert rahu_pos[3] < 0  # Should be retrograde
    
    disable_mock()

def test_houses_ex():
    """Test house calculation"""
    enable_mock()
    jd = julday(2000, 1, 1, 0)
    
    cusps, ascmc = houses_ex(jd, 0.0, 0.0, HSYS_WHOLE_SIGN)
    
    # Check house cusps
    assert len(cusps) == 13  # 12 houses + 1
    for i in range(13):
        assert isinstance(cusps[i], float)
        assert cusps[i] == i * 30.0  # Should be at 0° of each sign
    
    # Check angles
    assert len(ascmc) == 10
    assert ascmc[0] == 0.0  # Ascendant at 0° Aries
    
    disable_mock()

def test_mock_disabled_raises_error():
    """Test that functions raise error when mock is disabled"""
    disable_mock()
    
    jd = julday(2000, 1, 1, 0)
    
    with pytest.raises(RuntimeError):
        calc_ut(jd, SUN)
    
    with pytest.raises(RuntimeError):
        houses_ex(jd, 0.0, 0.0, HSYS_WHOLE_SIGN) 