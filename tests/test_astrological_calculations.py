"""Tests for astrological calculations"""
import pytest
from datetime import datetime
from api.services.astrological_calculations import AstrologicalCalculator, DEBUG_MODE
from api.models.astrological import BirthData, Planet, Sign, HousePosition

def test_debug_mode_disabled_by_default():
    """Test that debug mode is disabled by default"""
    assert not DEBUG_MODE

def test_validation_skipped_when_debug_disabled():
    """Test that chart validation is skipped when debug mode is disabled"""
    calculator = AstrologicalCalculator()
    birth_data = BirthData(
        date=datetime(2000, 1, 1, 12, 0),
        latitude=0.0,
        longitude=0.0,
        timezone="UTC"
    )
    
    # This should not raise any validation errors
    horoscope = calculator.calculate_horoscope(birth_data)
    assert horoscope is not None

def test_planet_positions_no_retrograde_sun_moon():
    """Test that Sun and Moon are never marked retrograde"""
    calculator = AstrologicalCalculator()
    birth_data = BirthData(
        date=datetime(2000, 1, 1, 12, 0),
        latitude=0.0,
        longitude=0.0,
        timezone="UTC"
    )
    
    positions = calculator.calculate_planet_positions(birth_data)
    
    # Find Sun and Moon positions
    sun_pos = next(p for p in positions if p.planet == Planet.SUN)
    moon_pos = next(p for p in positions if p.planet == Planet.MOON)
    
    assert not sun_pos.is_retrograde
    assert not moon_pos.is_retrograde

def test_rahu_ketu_always_retrograde():
    """Test that Rahu and Ketu are always marked retrograde"""
    calculator = AstrologicalCalculator()
    birth_data = BirthData(
        date=datetime(2000, 1, 1, 12, 0),
        latitude=0.0,
        longitude=0.0,
        timezone="UTC"
    )
    
    positions = calculator.calculate_planet_positions(birth_data)
    
    # Find Rahu and Ketu positions
    rahu_pos = next(p for p in positions if p.planet == Planet.RAHU)
    ketu_pos = next(p for p in positions if p.planet == Planet.KETU)
    
    assert rahu_pos.is_retrograde
    assert ketu_pos.is_retrograde

def test_house_sequence():
    """Test that houses follow correct sequence from ascendant"""
    calculator = AstrologicalCalculator()
    birth_data = BirthData(
        date=datetime(2000, 1, 1, 12, 0),
        latitude=0.0,
        longitude=0.0,
        timezone="UTC"
    )
    
    ascendant = calculator.calculate_ascendant(birth_data)
    houses = calculator.calculate_houses(birth_data, ascendant)
    
    # Check house sequence
    for i in range(12):
        expected_sign = Sign((ascendant.sign.value + i - 1) % 12 + 1)
        assert houses[i].sign == expected_sign
        assert houses[i].house_number == i + 1

def test_planet_dignities():
    """Test planet dignity calculations"""
    calculator = AstrologicalCalculator()
    
    # Test Sun in Aries (exalted)
    assert calculator.get_planet_dignity(Planet.SUN, Sign.ARIES) == "Exalted"
    
    # Test Sun in Libra (debilitated)
    assert calculator.get_planet_dignity(Planet.SUN, Sign.LIBRA) == "Debilitated"
    
    # Test Sun in Leo (own sign)
    assert calculator.get_planet_dignity(Planet.SUN, Sign.LEO) == "Own Sign"
    
    # Test Rahu/Ketu (should be neutral)
    assert calculator.get_planet_dignity(Planet.RAHU, Sign.TAURUS) == "Neutral"
    assert calculator.get_planet_dignity(Planet.KETU, Sign.SCORPIO) == "Neutral" 