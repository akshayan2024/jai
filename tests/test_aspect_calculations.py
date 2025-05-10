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

def test_aspect_calculator_initialization():
    """Test that aspect calculator initializes correctly"""
    calculator = AspectCalculator()
    assert calculator is not None
    assert hasattr(calculator, 'aspect_definitions')
    assert len(calculator.aspect_definitions) > 0

def test_conjunction_aspect():
    """Test detection of conjunction aspect"""
    calculator = AspectCalculator()
    
    # Create positions for a conjunction (planets in same sign)
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.ARIES, degree=15.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    conjunction = next((a for a in aspects if a.aspect_type == "Conjunction"), None)
    
    assert conjunction is not None
    assert conjunction.planet1 == Planet.MARS
    assert conjunction.planet2 == Planet.SATURN
    assert conjunction.distance == 5.0
    assert conjunction.strength > 0.0

def test_opposition_aspect():
    """Test detection of opposition aspect"""
    calculator = AspectCalculator()
    
    # Create positions for an opposition (planets 180 degrees apart)
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.LIBRA, degree=10.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    opposition = next((a for a in aspects if a.aspect_type == "Opposition"), None)
    
    assert opposition is not None
    assert opposition.planet1 == Planet.MARS
    assert opposition.planet2 == Planet.SATURN
    assert opposition.distance == 180.0
    assert opposition.strength > 0.0

def test_trine_aspect():
    """Test detection of trine aspect"""
    calculator = AspectCalculator()
    
    # Create positions for a trine (planets 120 degrees apart)
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.LEO, degree=10.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    trine = next((a for a in aspects if a.aspect_type == "Trine"), None)
    
    assert trine is not None
    assert trine.planet1 == Planet.MARS
    assert trine.planet2 == Planet.SATURN
    assert trine.distance == 120.0
    assert trine.strength > 0.0

def test_square_aspect():
    """Test detection of square aspect"""
    calculator = AspectCalculator()
    
    # Create positions for a square (planets 90 degrees apart)
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.CANCER, degree=10.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    square = next((a for a in aspects if a.aspect_type == "Square"), None)
    
    assert square is not None
    assert square.planet1 == Planet.MARS
    assert square.planet2 == Planet.SATURN
    assert square.distance == 90.0
    assert square.strength > 0.0

def test_sextile_aspect():
    """Test detection of sextile aspect"""
    calculator = AspectCalculator()
    
    # Create positions for a sextile (planets 60 degrees apart)
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.GEMINI, degree=10.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    sextile = next((a for a in aspects if a.aspect_type == "Sextile"), None)
    
    assert sextile is not None
    assert sextile.planet1 == Planet.MARS
    assert sextile.planet2 == Planet.SATURN
    assert sextile.distance == 60.0
    assert sextile.strength > 0.0

def test_aspect_strength_calculation():
    """Test that aspect strength is calculated correctly"""
    calculator = AspectCalculator()
    
    # Create positions for a strong conjunction
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.ARIES, degree=10.5, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    conjunction = next((a for a in aspects if a.aspect_type == "Conjunction"), None)
    
    assert conjunction is not None
    assert 0.0 < conjunction.strength <= 1.0
    assert conjunction.strength > 0.9  # Very close conjunction should have high strength

def test_no_aspect_detection():
    """Test that no aspects are detected when planets are too far apart"""
    calculator = AspectCalculator()
    
    # Create positions that don't form any aspects
    positions = [
        PlanetPosition(planet=Planet.MARS, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.SATURN, sign=Sign.VIRGO, degree=20.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    assert len(aspects) == 0

def test_special_aspects():
    """Test detection of special aspects for specific planets"""
    calculator = AspectCalculator()
    
    # Test Jupiter's special aspects
    positions = [
        PlanetPosition(planet=Planet.JUPITER, sign=Sign.ARIES, degree=10.0, is_retrograde=False),
        PlanetPosition(planet=Planet.MARS, sign=Sign.CANCER, degree=10.0, is_retrograde=False)
    ]
    
    aspects = calculator.calculate_aspects(positions)
    jupiter_aspect = next((a for a in aspects if a.planet1 == Planet.JUPITER), None)
    
    assert jupiter_aspect is not None
    assert jupiter_aspect.aspect_type == "Jupiter Special"
    assert jupiter_aspect.strength > 0.0 