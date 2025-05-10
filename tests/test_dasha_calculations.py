import pytest
from datetime import datetime, timedelta
from api.models.astrological import Planet, DashaPeriod
from api.services.dasha_calculations import DashaCalculator

def test_moon_nakshatra_calculation():
    """Test calculation of moon's nakshatra"""
    calculator = DashaCalculator()
    
    # Test first nakshatra (0-13.3333 degrees)
    nakshatra, degree = calculator.calculate_moon_nakshatra(5.0)
    assert nakshatra == 0
    assert degree == 5.0
    
    # Test second nakshatra (13.3333-26.6666 degrees)
    nakshatra, degree = calculator.calculate_moon_nakshatra(20.0)
    assert nakshatra == 1
    assert abs(degree - 6.6667) < 0.0001
    
    # Test last nakshatra (346.6666-360 degrees)
    nakshatra, degree = calculator.calculate_moon_nakshatra(350.0)
    assert nakshatra == 26
    assert abs(degree - 3.3333) < 0.0001

def test_dasha_balance_calculation():
    """Test calculation of dasha balance"""
    calculator = DashaCalculator()
    
    # Test first nakshatra (Ketu dasha)
    dasha_lord, remaining_years = calculator.calculate_dasha_balance(5.0)
    assert dasha_lord == Planet.KETU
    assert abs(remaining_years - 3.5) < 0.1  # Approximately half of Ketu's 7 years
    
    # Test second nakshatra (Venus dasha)
    dasha_lord, remaining_years = calculator.calculate_dasha_balance(20.0)
    assert dasha_lord == Planet.VENUS
    assert abs(remaining_years - 10.0) < 0.1  # Approximately half of Venus's 20 years

def test_dasha_periods_calculation():
    """Test calculation of dasha periods"""
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    moon_longitude = 5.0  # First nakshatra (Ketu dasha)
    
    periods = calculator.calculate_dasha_periods(birth_date, moon_longitude)
    
    # Verify first few periods
    assert len(periods) > 0
    
    # First period should be Ketu
    assert periods[0].planet == Planet.KETU
    assert periods[0].start_date == birth_date
    expected_end = birth_date + timedelta(days=3.5 * 365.25)  # Half of Ketu's 7 years
    assert abs((periods[0].end_date - expected_end).days) < 2
    
    # Second period should be Venus
    assert periods[1].planet == Planet.VENUS
    assert periods[1].start_date == periods[0].end_date
    expected_end = periods[1].start_date + timedelta(days=20 * 365.25)  # Full Venus period
    assert abs((periods[1].end_date - expected_end).days) < 2
    
    # Third period should be Sun
    assert periods[2].planet == Planet.SUN
    assert periods[2].start_date == periods[1].end_date
    expected_end = periods[2].start_date + timedelta(days=6 * 365.25)  # Full Sun period
    assert abs((periods[2].end_date - expected_end).days) < 2

def test_dasha_periods_cycle():
    """Test that dasha periods follow the correct cycle"""
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    moon_longitude = 5.0
    
    periods = calculator.calculate_dasha_periods(birth_date, moon_longitude)
    
    # Verify the order of planets follows DASHA_ORDER
    expected_order = calculator.DASHA_ORDER
    for i, period in enumerate(periods[:len(expected_order)]):
        assert period.planet == expected_order[i % len(expected_order)]

def test_dasha_periods_duration():
    """Test that dasha periods have correct durations"""
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    moon_longitude = 5.0
    
    periods = calculator.calculate_dasha_periods(birth_date, moon_longitude)
    
    # Skip first period as it's partial
    for period in periods[1:]:
        expected_days = calculator.DASHA_PERIODS[period.planet] * 365.25
        actual_days = (period.end_date - period.start_date).days
        assert abs(actual_days - expected_days) < 2  # Allow 2 days margin for rounding

def test_sub_periods_calculation():
    """Test calculation of sub-periods (bhuktis)"""
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    
    # Create a main period (e.g., Ketu dasha)
    main_period = DashaPeriod(
        planet=Planet.KETU,
        start_date=birth_date,
        end_date=birth_date + timedelta(days=7 * 365.25)  # 7 years
    )
    
    # Calculate sub-periods
    sub_periods = calculator.calculate_sub_periods(main_period)
    
    # Verify sub-periods
    assert len(sub_periods) == len(calculator.DASHA_ORDER)
    
    # First sub-period should be Ketu-Ketu
    assert sub_periods[0].planet == Planet.KETU
    assert sub_periods[0].start_date == birth_date
    
    # Second sub-period should be Ketu-Venus
    assert sub_periods[1].planet == Planet.VENUS
    assert sub_periods[1].start_date == sub_periods[0].end_date
    
    # Verify total duration of sub-periods equals main period duration
    total_sub_duration = sum((p.end_date - p.start_date).days for p in sub_periods)
    main_duration = (main_period.end_date - main_period.start_date).days
    assert abs(total_sub_duration - main_duration) < 2  # Allow 2 days margin for rounding

def test_sub_periods_proportions():
    """Test that sub-period durations are proportional to their total periods"""
    calculator = DashaCalculator()
    birth_date = datetime(1990, 1, 1)
    
    # Create a main period (e.g., Ketu dasha)
    main_period = DashaPeriod(
        planet=Planet.KETU,
        start_date=birth_date,
        end_date=birth_date + timedelta(days=7 * 365.25)  # 7 years
    )
    
    # Calculate sub-periods
    sub_periods = calculator.calculate_sub_periods(main_period)
    
    # Verify proportions
    for sub_period in sub_periods:
        sub_duration = (sub_period.end_date - sub_period.start_date).days
        main_duration = (main_period.end_date - main_period.start_date).days
        expected_proportion = calculator.DASHA_PERIODS[sub_period.planet] / calculator.total_dasha_years
        actual_proportion = sub_duration / main_duration
        assert abs(actual_proportion - expected_proportion) < 0.01  # 1% margin for rounding 