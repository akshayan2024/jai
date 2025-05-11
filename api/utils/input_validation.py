"""
Input validation utilities for the JAI API.
"""
from datetime import datetime
from typing import Tuple, Optional
from pydantic import BaseModel, Field, validator
import logging

logger = logging.getLogger(__name__)

# Constants for validation
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0
MIN_YEAR = 1900
MAX_YEAR = 2100

class ValidationError(Exception):
    """Custom validation error with detailed message."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

def validate_date_range(start_date: datetime, end_date: datetime) -> None:
    """
    Validate date range for calculations.
    
    Args:
        start_date: Start date for calculations
        end_date: End date for calculations
        
    Raises:
        ValidationError: If date range is invalid
    """
    if not start_date or not end_date:
        raise ValidationError("Both start and end dates are required", "date_range")
    
    if start_date > end_date:
        raise ValidationError("Start date must be before end date", "date_range")
    
    if start_date.year < MIN_YEAR or end_date.year > MAX_YEAR:
        raise ValidationError(
            f"Date range must be between {MIN_YEAR} and {MAX_YEAR}",
            "date_range"
        )

def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Validate geographical coordinates.
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        
    Raises:
        ValidationError: If coordinates are invalid
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        raise ValidationError("Coordinates must be numeric values", "coordinates")
    
    if latitude < MIN_LATITUDE or latitude > MAX_LATITUDE:
        raise ValidationError(
            f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE} degrees",
            "latitude"
        )
    
    if longitude < MIN_LONGITUDE or longitude > MAX_LONGITUDE:
        raise ValidationError(
            f"Longitude must be between {MIN_LONGITUDE} and {MAX_LONGITUDE} degrees",
            "longitude"
        )

def validate_house_system(house_system: str) -> None:
    """
    Validate house system parameter.
    
    Args:
        house_system: House system identifier
        
    Raises:
        ValidationError: If house system is invalid
    """
    valid_systems = ['W', 'P', 'K', 'O', 'R', 'C', 'A', 'E', 'B']
    if house_system not in valid_systems:
        raise ValidationError(
            f"Invalid house system. Must be one of: {', '.join(valid_systems)}",
            "house_system"
        )

def validate_ayanamsa(ayanamsa: int) -> None:
    """
    Validate ayanamsa parameter.
    
    Args:
        ayanamsa: Ayanamsa identifier
        
    Raises:
        ValidationError: If ayanamsa is invalid
    """
    valid_ayanamsas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    if ayanamsa not in valid_ayanamsas:
        raise ValidationError(
            f"Invalid ayanamsa. Must be one of: {', '.join(map(str, valid_ayanamsas))}",
            "ayanamsa"
        )

def validate_planet(planet: int) -> None:
    """
    Validate planet parameter.
    
    Args:
        planet: Planet identifier
        
    Raises:
        ValidationError: If planet is invalid
    """
    valid_planets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    if planet not in valid_planets:
        raise ValidationError(
            f"Invalid planet. Must be one of: {', '.join(map(str, valid_planets))}",
            "planet"
        )

def validate_extreme_latitude(latitude: float) -> None:
    """
    Validate latitude for house calculations at extreme latitudes.
    
    Args:
        latitude: Latitude in degrees
        
    Raises:
        ValidationError: If latitude is too extreme for house calculations
    """
    if abs(latitude) > 66.5:  # Arctic/Antarctic circles
        raise ValidationError(
            "House calculations may be inaccurate at extreme latitudes (beyond 66.5° N/S)",
            "latitude"
        )

class CalculationInput(BaseModel):
    """Base model for calculation inputs with validation."""
    date: datetime
    latitude: float
    longitude: float
    house_system: str = 'W'  # Default to Whole Sign
    ayanamsa: int = 1  # Default to Lahiri
    
    @validator('date')
    def validate_date(cls, v):
        if v.year < MIN_YEAR or v.year > MAX_YEAR:
            raise ValidationError(
                f"Date must be between {MIN_YEAR} and {MAX_YEAR}",
                "date"
            )
        return v
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if v < MIN_LATITUDE or v > MAX_LATITUDE:
            raise ValidationError(
                f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE} degrees",
                "latitude"
            )
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if v < MIN_LONGITUDE or v > MAX_LONGITUDE:
            raise ValidationError(
                f"Longitude must be between {MIN_LONGITUDE} and {MAX_LONGITUDE} degrees",
                "longitude"
            )
        return v
    
    @validator('house_system')
    def validate_house_system(cls, v):
        valid_systems = ['W', 'P', 'K', 'O', 'R', 'C', 'A', 'E', 'B']
        if v not in valid_systems:
            raise ValidationError(
                f"Invalid house system. Must be one of: {', '.join(valid_systems)}",
                "house_system"
            )
        return v
    
    @validator('ayanamsa')
    def validate_ayanamsa(cls, v):
        valid_ayanamsas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
        if v not in valid_ayanamsas:
            raise ValidationError(
                f"Invalid ayanamsa. Must be one of: {', '.join(map(str, valid_ayanamsas))}",
                "ayanamsa"
            )
        return v 