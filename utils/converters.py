from datetime import datetime, timedelta
from functools import lru_cache

from ..constants import get_constant

# This will be imported from an ephemeris library like pyswisseph
# For now, we'll stub it out
def julday(year, month, day, hour):
    """
    Stub for Swiss Ephemeris julday function.
    Will be replaced with actual implementation later.
    """
    # This is just a placeholder
    dt = datetime(year, month, day, int(hour), int((hour % 1) * 60), int(((hour % 1) * 60) % 1 * 60))
    return (dt - datetime(1900, 1, 1)).total_seconds() / 86400.0 + 2415020.0

@lru_cache(maxsize=1024)
def convert_to_julian_day(birth_date: str, birth_time: str, timezone_offset: float) -> float:
    """
    Convert date and time to Julian Day.
    
    Args:
        birth_date: Date in YYYY-MM-DD format
        birth_time: Time in HH:MM:SS format
        timezone_offset: Hours offset from UTC
        
    Returns:
        Julian Day number
    """
    # Parse date
    year, month, day = map(int, birth_date.split('-'))
    
    # Parse time
    hour, minute, second = map(int, birth_time.split(':'))
    
    # Convert to decimal hours
    decimal_hour = hour + minute/60.0 + second/3600.0
    
    # Apply timezone offset to get UTC
    utc_decimal_hour = decimal_hour - timezone_offset
    
    # Handle day change if needed
    day_adjustment = 0
    while utc_decimal_hour < 0:
        utc_decimal_hour += 24
        day_adjustment -= 1
    while utc_decimal_hour >= 24:
        utc_decimal_hour -= 24
        day_adjustment += 1
    
    # Adjust date if needed
    if day_adjustment != 0:
        dt = datetime(year, month, day) + timedelta(days=day_adjustment)
        year, month, day = dt.year, dt.month, dt.day
    
    # Calculate Julian day
    return julday(year, month, day, utc_decimal_hour)

def get_ayanamsa_code(ayanamsa_name: str) -> int:
    """
    Convert ayanamsa name to ayanamsa code.
    
    Args:
        ayanamsa_name: Ayanamsa name (lahiri, raman, etc.)
        
    Returns:
        Ayanamsa code as used by the ephemeris library
    """
    # Get mapping from constants
    ayanamsa_mapping = get_constant('ayanamsa_mapping')
    default_ayanamsa = get_constant('default_ayanamsa')
    
    # Convert to lowercase for case-insensitive comparison
    name = ayanamsa_name.lower() if ayanamsa_name else "lahiri"
    
    # Return the code or default if not found
    return ayanamsa_mapping.get(name, default_ayanamsa) 