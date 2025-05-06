import re
from datetime import datetime

from .custom_exceptions import ValidationError
from ..models.request_models import BirthDataRequest

def validate_birth_data(data: BirthDataRequest) -> None:
    """
    Validate birth data inputs.
    
    Args:
        data: Birth data request object
        
    Raises:
        ValidationError: If validation fails
    """
    # Validate date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data.birth_date):
        raise ValidationError("Invalid date format: must be YYYY-MM-DD")
    
    # Validate time format
    if not re.match(r'^\d{2}:\d{2}:\d{2}$', data.birth_time):
        raise ValidationError("Invalid time format: must be HH:MM:SS")
    
    # Validate latitude
    if data.latitude < -90 or data.latitude > 90:
        raise ValidationError("Invalid latitude: must be between -90 and +90")
    
    # Validate longitude
    if data.longitude < -180 or data.longitude > 180:
        raise ValidationError("Invalid longitude: must be between -180 and +180")
    
    # Validate timezone offset
    if data.timezone_offset < -12 or data.timezone_offset > 14:
        raise ValidationError("Invalid timezone offset: must be between -12 and +14")
    
    # Validate ayanamsa
    if data.ayanamsa not in ["lahiri", "raman", "krishnamurti"]:
        raise ValidationError(
            "Unsupported ayanamsa: allowed values are 'lahiri', 'raman', 'krishnamurti'"
        )
    
    # Validate date is realistic
    try:
        year, month, day = map(int, data.birth_date.split('-'))
        if not (1800 <= year <= 2200):
            raise ValidationError("Year must be between 1800 and 2200")
        datetime(year, month, day)  # Will raise ValueError if date is invalid
    except ValueError:
        raise ValidationError("Invalid date: date does not exist")
    
    # Validate time is realistic
    try:
        hour, minute, second = map(int, data.birth_time.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise ValidationError("Invalid time: hours, minutes, and seconds must be within valid ranges")
    except ValueError:
        raise ValidationError("Invalid time format") 