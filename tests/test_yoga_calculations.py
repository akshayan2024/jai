"""Tests for yoga calculations"""
import pytest
from datetime import datetime
from api.models.astrological import (
    Planet, Sign, PlanetPosition, HousePosition,
    BirthData, Yoga
)
from api.services.yoga_calculations import YogaCalculator

def test_gaja_kesari_yoga():
    """Test Gaja Kesari Yoga calculation"""
    # Create test data
    planets = [
        PlanetPosition(planet=Planet.JUPITER, sign=Sign.LEO, degree=15.0, is_retrograde=False),
        PlanetPosition(planet=Planet.MOON, sign=Sign.SAGITTARIUS, degree=20.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=1, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=2, sign=Sign.TAURUS, degree=0.0),
        HousePosition(house_number=3, sign=Sign.GEMINI, degree=0.0),
        HousePosition(house_number=4, sign=Sign.CANCER, degree=0.0),
        HousePosition(house_number=5, sign=Sign.LEO, degree=0.0),
        HousePosition(house_number=6, sign=Sign.VIRGO, degree=0.0),
        HousePosition(house_number=7, sign=Sign.LIBRA, degree=0.0),
        HousePosition(house_number=8, sign=Sign.SCORPIO, degree=0.0),
        HousePosition(house_number=9, sign=Sign.SAGITTARIUS, degree=0.0),
        HousePosition(house_number=10, sign=Sign.CAPRICORN, degree=0.0),
        HousePosition(house_number=11, sign=Sign.AQUARIUS, degree=0.0),
        HousePosition(house_number=12, sign=Sign.PISCES, degree=0.0)
    ]
    
    calculator = YogaCalculator()
    yogas = calculator.calculate_yogas(planets, houses)
    
    # Check if Gaja Kesari Yoga is present
    gaja_kesari = next((y for y in yogas if y.name == "Gaja Kesari Yoga"), None)
    assert gaja_kesari is not None
    assert gaja_kesari.planets == [Planet.JUPITER, Planet.MOON]
    assert 0.0 <= gaja_kesari.strength <= 1.0

def test_budha_aditya_yoga():
    """Test Budha-Aditya Yoga calculation"""
    # Create test data
    planets = [
        PlanetPosition(planet=Planet.MERCURY, sign=Sign.LEO, degree=15.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SUN, sign=Sign.LEO, degree=20.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=1, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=2, sign=Sign.TAURUS, degree=0.0),
        HousePosition(house_number=3, sign=Sign.GEMINI, degree=0.0),
        HousePosition(house_number=4, sign=Sign.CANCER, degree=0.0),
        HousePosition(house_number=5, sign=Sign.LEO, degree=0.0),
        HousePosition(house_number=6, sign=Sign.VIRGO, degree=0.0),
        HousePosition(house_number=7, sign=Sign.LIBRA, degree=0.0),
        HousePosition(house_number=8, sign=Sign.SCORPIO, degree=0.0),
        HousePosition(house_number=9, sign=Sign.SAGITTARIUS, degree=0.0),
        HousePosition(house_number=10, sign=Sign.CAPRICORN, degree=0.0),
        HousePosition(house_number=11, sign=Sign.AQUARIUS, degree=0.0),
        HousePosition(house_number=12, sign=Sign.PISCES, degree=0.0)
    ]
    
    calculator = YogaCalculator()
    yogas = calculator.calculate_yogas(planets, houses)
    
    # Check if Budha-Aditya Yoga is present
    budha_aditya = next((y for y in yogas if y.name == "Budha-Aditya Yoga"), None)
    assert budha_aditya is not None
    assert budha_aditya.planets == [Planet.MERCURY, Planet.SUN]
    assert 0.0 <= budha_aditya.strength <= 1.0

def test_kemadruma_yoga():
    """Test Kemadruma Yoga calculation"""
    # Create test data with Moon alone
    planets = [
        PlanetPosition(planet=Planet.MOON, sign=Sign.LEO, degree=15.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=1, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=2, sign=Sign.TAURUS, degree=0.0),
        HousePosition(house_number=3, sign=Sign.GEMINI, degree=0.0),
        HousePosition(house_number=4, sign=Sign.CANCER, degree=0.0),
        HousePosition(house_number=5, sign=Sign.LEO, degree=0.0),
        HousePosition(house_number=6, sign=Sign.VIRGO, degree=0.0),
        HousePosition(house_number=7, sign=Sign.LIBRA, degree=0.0),
        HousePosition(house_number=8, sign=Sign.SCORPIO, degree=0.0),
        HousePosition(house_number=9, sign=Sign.SAGITTARIUS, degree=0.0),
        HousePosition(house_number=10, sign=Sign.CAPRICORN, degree=0.0),
        HousePosition(house_number=11, sign=Sign.AQUARIUS, degree=0.0),
        HousePosition(house_number=12, sign=Sign.PISCES, degree=0.0)
    ]
    
    calculator = YogaCalculator()
    yogas = calculator.calculate_yogas(planets, houses)
    
    # Check if Kemadruma Yoga is present
    kemadruma = next((y for y in yogas if y.name == "Kemadruma Yoga"), None)
    assert kemadruma is not None
    assert kemadruma.planets == [Planet.MOON]
    assert 0.0 <= kemadruma.strength <= 1.0

def test_no_yogas():
    """Test when no yogas are present"""
    # Create test data with no yoga-forming combinations
    planets = [
        PlanetPosition(planet=Planet.SUN, sign=Sign.ARIES, degree=15.0, is_retrograde=False),
        PlanetPosition(planet=Planet.MOON, sign=Sign.TAURUS, degree=20.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=1, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=2, sign=Sign.TAURUS, degree=0.0),
        HousePosition(house_number=3, sign=Sign.GEMINI, degree=0.0),
        HousePosition(house_number=4, sign=Sign.CANCER, degree=0.0),
        HousePosition(house_number=5, sign=Sign.LEO, degree=0.0),
        HousePosition(house_number=6, sign=Sign.VIRGO, degree=0.0),
        HousePosition(house_number=7, sign=Sign.LIBRA, degree=0.0),
        HousePosition(house_number=8, sign=Sign.SCORPIO, degree=0.0),
        HousePosition(house_number=9, sign=Sign.SAGITTARIUS, degree=0.0),
        HousePosition(house_number=10, sign=Sign.CAPRICORN, degree=0.0),
        HousePosition(house_number=11, sign=Sign.AQUARIUS, degree=0.0),
        HousePosition(house_number=12, sign=Sign.PISCES, degree=0.0)
    ]
    
    calculator = YogaCalculator()
    yogas = calculator.calculate_yogas(planets, houses)
    
    # Check that no yogas are present
    assert len(yogas) == 0

def test_yoga_calculator_initialization():
    """Test that yoga calculator initializes correctly"""
    calculator = YogaCalculator()
    assert calculator is not None
    assert hasattr(calculator, 'yoga_definitions')
    assert len(calculator.yoga_definitions) > 0

def test_raja_yoga_detection():
    """Test detection of Raja Yoga"""
    calculator = YogaCalculator()
    
    # Create positions for Raja Yoga (Jupiter in 9th house, Venus in 10th)
    positions = [
        PlanetPosition(planet=Planet.JUPITER, sign=Sign.ARIES, degree=15.0, is_retrograde=False),
        PlanetPosition(planet=Planet.VENUS, sign=Sign.TAURUS, degree=20.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=9, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=10, sign=Sign.TAURUS, degree=0.0)
    ]
    
    yogas = calculator.calculate_yogas(positions, houses)
    raja_yoga = next((y for y in yogas if y.name == "Raja Yoga"), None)
    
    assert raja_yoga is not None
    assert "Jupiter" in raja_yoga.planets
    assert "Venus" in raja_yoga.planets
    assert raja_yoga.strength > 0.0

def test_budha_aditya_yoga_detection():
    """Test detection of Budha-Aditya Yoga"""
    calculator = YogaCalculator()
    
    # Create positions for Budha-Aditya Yoga (Mercury and Sun in same sign)
    positions = [
        PlanetPosition(planet=Planet.MERCURY, sign=Sign.LEO, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SUN, sign=Sign.LEO, degree=15.0, is_retrograde=False)
    ]
    
    houses = [HousePosition(house_number=i, sign=Sign.ARIES, degree=0.0) for i in range(1, 13)]
    
    yogas = calculator.calculate_yogas(positions, houses)
    budha_aditya = next((y for y in yogas if y.name == "Budha-Aditya Yoga"), None)
    
    assert budha_aditya is not None
    assert "Mercury" in budha_aditya.planets
    assert "Sun" in budha_aditya.planets
    assert budha_aditya.strength > 0.0

def test_gaja_kesari_yoga_detection():
    """Test detection of Gaja Kesari Yoga"""
    calculator = YogaCalculator()
    
    # Create positions for Gaja Kesari Yoga (Jupiter in kendra from Moon)
    positions = [
        PlanetPosition(planet=Planet.JUPITER, sign=Sign.CANCER, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.MOON, sign=Sign.ARIES, degree=15.0, is_retrograde=False)
    ]
    
    houses = [HousePosition(house_number=i, sign=Sign.ARIES, degree=0.0) for i in range(1, 13)]
    
    yogas = calculator.calculate_yogas(positions, houses)
    gaja_kesari = next((y for y in yogas if y.name == "Gaja Kesari Yoga"), None)
    
    assert gaja_kesari is not None
    assert "Jupiter" in gaja_kesari.planets
    assert "Moon" in gaja_kesari.planets
    assert gaja_kesari.strength > 0.0

def test_no_yoga_detection():
    """Test that no yogas are detected when conditions aren't met"""
    calculator = YogaCalculator()
    
    # Create positions that don't form any yogas
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.GEMINI, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.VIRGO, degree=20.0, is_retrograde=False)
    ]
    
    houses = [HousePosition(house_number=i, sign=Sign.ARIES, degree=0.0) for i in range(1, 13)]
    
    yogas = calculator.calculate_yogas(positions, houses)
    assert len(yogas) == 0

def test_yoga_strength_calculation():
    """Test that yoga strength is calculated correctly"""
    calculator = YogaCalculator()
    
    # Create positions for a strong Raja Yoga
    positions = [
        PlanetPosition(planet=Planet.JUPITER, sign=Sign.ARIES, degree=15.0, is_retrograde=False),
        PlanetPosition(planet=Planet.VENUS, sign=Sign.TAURUS, degree=20.0, is_retrograde=False)
    ]
    
    houses = [
        HousePosition(house_number=9, sign=Sign.ARIES, degree=0.0),
        HousePosition(house_number=10, sign=Sign.TAURUS, degree=0.0)
    ]
    
    yogas = calculator.calculate_yogas(positions, houses)
    raja_yoga = next((y for y in yogas if y.name == "Raja Yoga"), None)
    
    assert raja_yoga is not None
    assert 0.0 < raja_yoga.strength <= 1.0 