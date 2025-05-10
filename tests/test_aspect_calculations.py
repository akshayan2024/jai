import pytest
from api.models.astrological import Planet, Sign, PlanetPosition, Aspect
from api.services.aspect_calculations import AspectCalculator

def test_absolute_longitude_calculation():
    """Test calculation of absolute longitude from sign and degree"""
    calculator = AspectCalculator()
    
    # Test first sign (Aries)
    position = PlanetPosition(planet=Planet.SUN, sign=Sign.ARIES, degree=15.0)
    assert calculator.calculate_absolute_longitude(position) == 15.0
    
    # Test middle sign (Leo)
    position = PlanetPosition(planet=Planet.SUN, sign=Sign.LEO, degree=20.0)
    assert calculator.calculate_absolute_longitude(position) == 140.0  # (5-1)*30 + 20
    
    # Test last sign (Pisces)
    position = PlanetPosition(planet=Planet.SUN, sign=Sign.PISCES, degree=25.0)
    assert calculator.calculate_absolute_longitude(position) == 355.0  # (12-1)*30 + 25

def test_aspect_distance_calculation():
    """Test calculation of angular distance between positions"""
    calculator = AspectCalculator()
    
    # Test same position
    assert calculator.calculate_aspect_distance(0.0, 0.0) == 0.0
    
    # Test positions in same sign
    assert calculator.calculate_aspect_distance(5.0, 15.0) == 10.0
    
    # Test positions in different signs
    assert calculator.calculate_aspect_distance(350.0, 10.0) == 20.0  # Should take shorter path
    
    # Test opposition
    assert calculator.calculate_aspect_distance(0.0, 180.0) == 180.0

def test_aspect_forming():
    """Test aspect formation detection"""
    calculator = AspectCalculator()
    
    # Test exact conjunction
    assert calculator.is_aspect_forming(0.0, "Conjunction", 10.0)
    
    # Test conjunction within orb
    assert calculator.is_aspect_forming(5.0, "Conjunction", 10.0)
    
    # Test conjunction outside orb
    assert not calculator.is_aspect_forming(15.0, "Conjunction", 10.0)
    
    # Test exact opposition
    assert calculator.is_aspect_forming(180.0, "Opposition", 10.0)
    
    # Test opposition within orb
    assert calculator.is_aspect_forming(175.0, "Opposition", 10.0)
    
    # Test opposition outside orb
    assert not calculator.is_aspect_forming(165.0, "Opposition", 10.0)

def test_aspect_strength_calculation():
    """Test calculation of aspect strength"""
    calculator = AspectCalculator()
    
    # Test exact aspect
    assert calculator.calculate_aspect_strength(0.0, "Conjunction", 10.0) == 1.0
    
    # Test aspect at orb limit
    assert calculator.calculate_aspect_strength(10.0, "Conjunction", 10.0) == 0.0
    
    # Test aspect halfway to orb limit
    assert calculator.calculate_aspect_strength(5.0, "Conjunction", 10.0) == 0.5
    
    # Test aspect beyond orb limit
    assert calculator.calculate_aspect_strength(15.0, "Conjunction", 10.0) == 0.0

def test_planet_aspects():
    """Test getting aspects for specific planets"""
    calculator = AspectCalculator()
    
    # Test regular planet
    aspects = calculator.get_planet_aspects(Planet.SUN)
    assert "Conjunction" in aspects
    assert "Opposition" in aspects
    assert "Trine" in aspects
    
    # Test Jupiter (special aspects)
    aspects = calculator.get_planet_aspects(Planet.JUPITER)
    assert aspects["Trine"] == 8
    assert aspects["Opposition"] == 10
    
    # Test Saturn (special aspects)
    aspects = calculator.get_planet_aspects(Planet.SATURN)
    assert aspects["Square"] == 8
    assert aspects["Trine"] == 8

def test_aspect_calculation():
    """Test calculation of aspects between planets"""
    calculator = AspectCalculator()
    
    # Create test planets
    planets = [
        PlanetPosition(planet=Planet.SUN, sign=Sign.ARIES, degree=15.0),
        PlanetPosition(planet=Planet.MOON, sign=Sign.LEO, degree=15.0),  # Trine to Sun
        PlanetPosition(planet=Planet.MARS, sign=Sign.LIBRA, degree=15.0)  # Opposition to Sun
    ]
    
    aspects = calculator.calculate_aspects(planets)
    
    # Should have aspects between Sun-Moon and Sun-Mars
    assert len(aspects) == 2
    
    # Check Sun-Moon trine
    sun_moon = next(a for a in aspects if a.planet1 == Planet.SUN and a.planet2 == Planet.MOON)
    assert sun_moon.aspect_type == "Trine"
    assert 0.0 < sun_moon.strength <= 1.0
    
    # Check Sun-Mars opposition
    sun_mars = next(a for a in aspects if a.planet1 == Planet.SUN and a.planet2 == Planet.MARS)
    assert sun_mars.aspect_type == "Opposition"
    assert 0.0 < sun_mars.strength <= 1.0

def test_get_aspects_for_planet():
    """Test getting aspects for a specific planet"""
    calculator = AspectCalculator()
    
    # Create test planets and aspects
    planets = [
        PlanetPosition(planet=Planet.SUN, sign=Sign.ARIES, degree=15.0),
        PlanetPosition(planet=Planet.MOON, sign=Sign.LEO, degree=15.0),
        PlanetPosition(planet=Planet.MARS, sign=Sign.LIBRA, degree=15.0)
    ]
    
    all_aspects = calculator.calculate_aspects(planets)
    sun_aspects = calculator.get_aspects_for_planet(Planet.SUN, all_aspects)
    
    assert len(sun_aspects) == 2
    assert all(a.planet1 == Planet.SUN or a.planet2 == Planet.SUN for a in sun_aspects)

def test_get_aspects_between_planets():
    """Test getting aspects between two specific planets"""
    calculator = AspectCalculator()
    
    # Create test planets and aspects
    planets = [
        PlanetPosition(planet=Planet.SUN, sign=Sign.ARIES, degree=15.0),
        PlanetPosition(planet=Planet.MOON, sign=Sign.LEO, degree=15.0),
        PlanetPosition(planet=Planet.MARS, sign=Sign.LIBRA, degree=15.0)
    ]
    
    all_aspects = calculator.calculate_aspects(planets)
    sun_moon_aspects = calculator.get_aspects_between_planets(Planet.SUN, Planet.MOON, all_aspects)
    
    assert len(sun_moon_aspects) == 1
    assert sun_moon_aspects[0].planet1 in [Planet.SUN, Planet.MOON]
    assert sun_moon_aspects[0].planet2 in [Planet.SUN, Planet.MOON] 