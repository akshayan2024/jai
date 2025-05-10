"""
Request data models for JAI API
"""
from pydantic import BaseModel, Field, validator, model_validator
from typing import Optional, List, Any, Dict
from datetime import datetime, date
import requests
import re
import os
import json
import time
import logging
from pathlib import Path
from functools import lru_cache

# Configure logging
logger = logging.getLogger("jai-api.request")

# Create cache directory if it doesn't exist
CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)
GEO_CACHE_FILE = CACHE_DIR / "geocode_cache.json"
TZ_CACHE_FILE = CACHE_DIR / "timezone_cache.json"

# Initialize cache with proper error handling
def load_cache(cache_file: Path, default=None):
    """Safely load a cache file with error handling"""
    if default is None:
        default = {}
    
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading cache from {cache_file}: {str(e)}")
            # If cache is corrupted, try to backup and create new
            try:
                if cache_file.exists():
                    backup_file = cache_file.with_suffix('.bak')
                    logger.warning(f"Creating backup of corrupted cache at {backup_file}")
                    cache_file.rename(backup_file)
            except Exception as e:
                logger.error(f"Failed to backup corrupted cache: {str(e)}")
    
    return default

# Load caches
GEOCODE_CACHE = load_cache(GEO_CACHE_FILE)
TIMEZONE_CACHE = load_cache(TZ_CACHE_FILE)

def save_cache(cache_data: dict, cache_file: Path):
    """Safely save cache with error handling"""
    try:
        # Create a temporary file first
        temp_file = cache_file.with_suffix('.tmp')
        with open(temp_file, "w") as f:
            json.dump(cache_data, f)
        
        # Atomic replacement of the original file
        temp_file.replace(cache_file)
        return True
    except Exception as e:
        logger.error(f"Error saving cache to {cache_file}: {str(e)}")
        return False

@lru_cache(maxsize=100)
def geocode_place(place_name: str, max_retries=2, retry_delay=1) -> dict:
    """
    Geocode a place name to get coordinates using OpenStreetMap Nominatim API with caching
    
    Args:
        place_name: The name of the place to geocode
        max_retries: Maximum number of retries on failure
        retry_delay: Delay between retries in seconds
        
    Returns:
        Dictionary containing lat, lon and display_name
        
    Raises:
        ValueError: If geocoding fails after retries
    """
    if not place_name or not place_name.strip():
        raise ValueError("Place name cannot be empty")
    
    # Check cache first
    cache_key = place_name.strip().lower()
    if cache_key in GEOCODE_CACHE:
        logger.debug(f"Geocode cache hit for '{place_name}'")
        return GEOCODE_CACHE[cache_key]
    
    logger.info(f"Geocoding place: '{place_name}'")
    
    # Prepare API request
    geocode_url = f"https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": "1",
        "addressdetails": "1"  # Get address details for better verification
    }
    headers = {
        "User-Agent": "JAI-API/1.0",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    # Try with retries
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(geocode_url, params=params, headers=headers, timeout=5)
            
            # Check for rate limiting or server errors
            if response.status_code == 429:
                if attempt < max_retries:
                    wait_time = retry_delay * (attempt + 1)
                    logger.warning(f"Rate limited by geocoding service. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ValueError("Geocoding service rate limit exceeded. Please try again later.")
            
            if response.status_code >= 500:
                if attempt < max_retries:
                    wait_time = retry_delay * (attempt + 1)
                    logger.warning(f"Geocoding service error ({response.status_code}). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ValueError(f"Geocoding service error: HTTP {response.status_code}")
            
            # Handle non-200 responses
            if response.status_code != 200:
                raise ValueError(f"Geocoding request failed with status code: {response.status_code}")
            
            # Parse response
            results = response.json()
            
            # Check if we got results
            if not results:
                raise ValueError(f"No geocoding results found for '{place_name}'")
            
            # Get coordinates and display name
            place_data = results[0]
            result = {
                "lat": float(place_data["lat"]),
                "lon": float(place_data["lon"]),
                "display_name": place_data["display_name"]
            }
            
            # Verify the data makes sense
            if result["lat"] < -90 or result["lat"] > 90:
                raise ValueError(f"Invalid latitude value: {result['lat']}")
            if result["lon"] < -180 or result["lon"] > 180:
                raise ValueError(f"Invalid longitude value: {result['lon']}")
            
            # Update cache
            GEOCODE_CACHE[cache_key] = result
            save_cache(GEOCODE_CACHE, GEO_CACHE_FILE)
            
            logger.info(f"Successfully geocoded '{place_name}' to {result['lat']}, {result['lon']}")
            return result
            
        except requests.RequestException as e:
            if attempt < max_retries:
                wait_time = retry_delay * (attempt + 1)
                logger.warning(f"Network error during geocoding. Retrying in {wait_time}s... Error: {str(e)}")
                time.sleep(wait_time)
            else:
                logger.error(f"Geocoding failed after {max_retries + 1} attempts: {str(e)}")
                raise ValueError(f"Network error during geocoding: {str(e)}")
        
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing geocoding response: {str(e)}")
            raise ValueError(f"Error processing geocoding results: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error during geocoding: {str(e)}")
            raise ValueError(f"Geocoding failed: {str(e)}")

@lru_cache(maxsize=100)
def get_timezone(lat: float, lon: float, max_retries=2, retry_delay=1) -> float:
    """
    Get timezone offset for coordinates using TimeZoneDB API with caching and fallback
    
    Args:
        lat: Latitude
        lon: Longitude
        max_retries: Maximum number of retries on failure
        retry_delay: Delay between retries in seconds
        
    Returns:
        Timezone offset in hours
    """
    # Input validation
    if lat < -90 or lat > 90:
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
    
    if lon < -180 or lon > 180:
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")
    
    # Create cache key
    cache_key = f"{lat:.4f},{lon:.4f}"
    if cache_key in TIMEZONE_CACHE:
        logger.debug(f"Timezone cache hit for {lat}, {lon}")
        return TIMEZONE_CACHE[cache_key]
    
    logger.info(f"Getting timezone for {lat}, {lon}")
    
    # Get API key from environment
    api_key = os.environ.get("TIMEZONEDB_API_KEY")
    
    if api_key:
        # Use TimeZoneDB API
        tz_url = "https://api.timezonedb.com/v2.1/get-time-zone"
        params = {
            "key": api_key,
            "format": "json",
            "by": "position",
            "lat": lat,
            "lng": lon
        }
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(tz_url, params=params, timeout=5)
                
                if response.status_code != 200:
                    logger.warning(f"TimeZoneDB API returned status code {response.status_code}")
                    if attempt < max_retries:
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    else:
                        logger.warning("Falling back to approximate timezone calculation")
                        break
                
                tz_data = response.json()
                if tz_data.get("status") == "OK":
                    # Convert seconds to hours
                    offset_hours = tz_data["gmtOffset"] / 3600
                    
                    # Update cache
                    TIMEZONE_CACHE[cache_key] = offset_hours
                    save_cache(TIMEZONE_CACHE, TZ_CACHE_FILE)
                    
                    logger.info(f"Timezone for {lat}, {lon} is UTC{'+' if offset_hours >= 0 else ''}{offset_hours}")
                    return offset_hours
                else:
                    logger.warning(f"TimeZoneDB API error: {tz_data.get('message', 'Unknown error')}")
                    if attempt < max_retries:
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    else:
                        logger.warning("Falling back to approximate timezone calculation")
                        break
                    
            except Exception as e:
                logger.warning(f"Error getting timezone from API: {str(e)}")
                if attempt < max_retries:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    logger.warning("Falling back to approximate timezone calculation")
                    break
    else:
        logger.info("No TimeZoneDB API key found, using approximate timezone calculation")
    
    # Fallback: Calculate approximate timezone from longitude
    # 15 degrees of longitude = 1 hour
    offset_hours = round(lon / 15, 4)
    
    # Clamp timezone offset to valid range
    offset_hours = max(-12, min(14, offset_hours))
    
    logger.info(f"Approximate timezone for {lat}, {lon} is UTC{'+' if offset_hours >= 0 else ''}{offset_hours}")
    
    # Update cache with approximate value
    TIMEZONE_CACHE[cache_key] = offset_hours
    save_cache(TIMEZONE_CACHE, TZ_CACHE_FILE)
    
    return offset_hours

class HoroscopeRequest(BaseModel):
    """Base request model for horoscope data"""
    birth_date: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Time of birth (HH:MM:SS)")
    place: Optional[str] = Field(None, description="Place name (city, country) - PREFERRED METHOD")
    latitude: Optional[float] = Field(None, description="Latitude of birth place (alternative to place)")
    longitude: Optional[float] = Field(None, description="Longitude of birth place (alternative to place)")
    timezone_offset: Optional[float] = Field(None, description="Timezone offset in hours (alternative to place)")
    ayanamsa: str = Field("lahiri", description="Ayanamsa system (lahiri, raman, etc.)")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("birth_date must be in YYYY-MM-DD format")
            
    @validator('birth_time')
    def validate_birth_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M:%S")
            return v
        except ValueError:
            try:
                # Try without seconds
                datetime.strptime(v, "%H:%M")
                # Add seconds for consistency
                return f"{v}:00"
            except ValueError:
                raise ValueError("birth_time must be in HH:MM:SS or HH:MM format")
    
    @model_validator(mode='after')
    def validate_location_data(self):
        """Ensure we have either place or complete coordinate data"""
        if self.place:
            # If place is provided, geocode it to get coordinates
            if not all([self.latitude, self.longitude, self.timezone_offset]):
                self._geocode_place()
            return self
        
        # If no place, check if we have coordinates and timezone
        if not all([self.latitude is not None, self.longitude is not None, self.timezone_offset is not None]):
            missing = []
            if self.latitude is None:
                missing.append("latitude")
            if self.longitude is None:
                missing.append("longitude")
            if self.timezone_offset is None:
                missing.append("timezone_offset")
            
            raise ValueError(f"Place name is required (preferred) or all of {', '.join(missing)} must be provided")
        
        return self
    
    def _geocode_place(self):
        """Get latitude, longitude and timezone from place name"""
        try:
            # Get coordinates from place name
            geo_data = geocode_place(self.place)
            self.latitude = geo_data["lat"]
            self.longitude = geo_data["lon"]
            
            # Calculate timezone if not provided
            if self.timezone_offset is None:
                self.timezone_offset = get_timezone(self.latitude, self.longitude)
                
        except Exception as e:
            # Log the error and raise a user-friendly message
            logger.error(f"Error geocoding place '{self.place}': {str(e)}")
            raise ValueError(f"Could not determine coordinates for place: {self.place}. {str(e)}")

class TransitRequest(HoroscopeRequest):
    """Request model for transit calculations"""
    transit_date: str = Field(..., description="Transit date (YYYY-MM-DD)")
    
    @validator('transit_date')
    def validate_transit_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("transit_date must be in YYYY-MM-DD format") 