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
    Geocode a place name to get coordinates using multiple geocoding services with fallback.
    Tries OpenCage first if API key is available, then falls back to OpenStreetMap Nominatim.
    
    Args:
        place_name: The name of the place to geocode
        max_retries: Maximum number of retries on failure
        retry_delay: Delay between retries in seconds
        
    Returns:
        Dictionary containing lat, lon, display_name and source
        
    Raises:
        ValueError: If geocoding fails after all retries and fallbacks
    """
    import time
    import random
    import requests
    from urllib.parse import quote
    import os
    
    # Clean and normalize the place name for caching
    cache_key = place_name.lower().strip()
    
    # Check cache first
    if cache_key in GEOCODE_CACHE:
        logger.debug(f"Geocode cache hit for '{place_name}'")
        return GEOCODE_CACHE[cache_key]
    
    # User-Agent is required by Nominatim's usage policy
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    # Try OpenCage first if API key is available
    opencage_api_key = os.environ.get("OPENCAGE_API_KEY")
    if opencage_api_key:
        try:
            url = "https://api.opencagedata.com/geocode/v1/json"
            params = {
                "q": place_name,
                "key": opencage_api_key,
                "no_annotations": 1,
                "limit": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                geo_data = {
                    'lat': result['geometry']['lat'],
                    'lon': result['geometry']['lng'],
                    'display_name': result.get('formatted', place_name),
                    'source': 'opencage'
                }
                
                # Cache the result
                GEOCODE_CACHE[cache_key] = geo_data
                save_cache(GEOCODE_CACHE, GEO_CACHE_FILE)
                logger.info(f"Geocoded '{place_name}' using OpenCage")
                return geo_data
                
        except Exception as e:
            logger.warning(f"OpenCage geocoding failed, falling back to Nominatim: {str(e)}")
    
    # Fall back to Nominatim if OpenCage fails or is not configured
    geocode_url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': place_name,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(geocode_url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or not isinstance(data, list) or len(data) == 0:
                last_error = f"No results found. Response: {response.text}"
                raise ValueError("No results found")
                
            result = data[0]
            
            # Format the result
            geo_data = {
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'display_name': result.get('display_name', place_name),
                'source': 'nominatim'
            }
            
            # Cache the result
            GEOCODE_CACHE[cache_key] = geo_data
            save_cache(GEOCODE_CACHE, GEO_CACHE_FILE)
            
            logger.info(f"Successfully geocoded '{place_name}' to {result['lat']}, {result['lon']}")
            return geo_data
            
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                # Exponential backoff with jitter
                sleep_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Geocoding attempt {attempt + 1} failed, retrying in {sleep_time:.1f}s: {str(e)}")
                time.sleep(sleep_time)
    
    # If we get here, all attempts failed
    logger.error(f"Failed to geocode '{place_name}' after {max_retries + 1} attempts")
    if last_error:
        logger.error(f"Last error: {str(last_error)}")
        raise ValueError(f"Could not determine coordinates for place: {place_name}. Last error: {str(last_error)}")
    raise ValueError(f"Could not determine coordinates for place: {place_name}. Please check the place name and try again.")

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
    """Request model for horoscope data using place-based geocoding"""
    birth_date: str = Field(..., description="Date of birth (supports multiple formats like YYYY-MM-DD, DD-MM-YYYY, DD MMM YYYY, etc.)")
    birth_time: str = Field(..., description="Time of birth (supports formats like HH:MM:SS, HH:MM, HHMM, 12-hour format with AM/PM)")
    place: str = Field(..., description="Place name (city, country) - e.g., 'Chennai, India'")
    ayanamsa: str = Field("lahiri", description="Ayanamsa system (default: lahiri). Options: lahiri, raman, krishnamurti, kp, jyotish_raman")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """
        Validate and normalize birth date format.
        Supports multiple formats for ChatGPT integration.
        """
        # Support standard ISO format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(iso_pattern, v):
            return v
            
        # Try various date formats (DD-MM-YYYY, DD/MM/YYYY, etc.)
        date_formats = [
            '%d-%m-%Y',  # 01-01-1990
            '%d/%m/%Y',  # 01/01/1990
            '%m-%d-%Y',  # 01-01-1990 (US format)
            '%m/%d/%Y',  # 01/01/1990 (US format)
            '%d %b %Y',  # 01 Jan 1990
            '%d %B %Y',  # 01 January 1990
            '%b %d %Y',  # Jan 01 1990
            '%B %d %Y',  # January 01 1990
            '%b %d, %Y', # Jan 01, 1990
            '%B %d, %Y'  # January 01, 1990
        ]
        
        # Try each format
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(v, fmt)
                # Convert to YYYY-MM-DD
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
                
        # If we get here, no format matched
        raise ValueError("Invalid birth date format. Supported formats include: YYYY-MM-DD, DD-MM-YYYY, MM/DD/YYYY, 01 Jan 1990, etc.")
    
    @validator('birth_time')
    def validate_birth_time(cls, v):
        """
        Validate and normalize birth time format.
        Supports multiple formats for ChatGPT integration.
        """
        # Standard format HH:MM:SS
        std_pattern = r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$'
        if re.match(std_pattern, v):
            return v
            
        # HH:MM format (add seconds)
        hhmm_pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
        if re.match(hhmm_pattern, v):
            return f"{v}:00"
            
        # HHMM format (4 digits)
        hhmm_digit_pattern = r'^([01]\d|2[0-3])([0-5]\d)$'
        hhmm_match = re.match(hhmm_digit_pattern, v)
        if hhmm_match:
            return f"{hhmm_match.group(1)}:{hhmm_match.group(2)}:00"
            
        # Try AM/PM format
        am_pm_pattern = r'^(0?\d|1[0-2]):([0-5]\d)(?::([0-5]\d))?\s*(am|pm|AM|PM)$'
        am_pm_match = re.match(am_pm_pattern, v)
        if am_pm_match:
            hour = int(am_pm_match.group(1))
            minute = am_pm_match.group(2)
            second = am_pm_match.group(3) or '00'
            am_pm = am_pm_match.group(4).lower()
            
            # Adjust hour for 24-hour format
            if am_pm == 'pm' and hour < 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0
                
            return f"{hour:02d}:{minute}:{second}"
            
        # If we get here, no format matched
        raise ValueError("Invalid time format. Supported formats include: HH:MM:SS, HH:MM, HHMM, and 12-hour format (e.g., 2:30 PM).")
    
    @model_validator(mode='after')
    def validate_and_geocode(self):
        """Geocode the provided place name to get coordinates and timezone"""
        try:
            # Get coordinates from place name
            geo_data = geocode_place(self.place)
            self.latitude = geo_data["lat"]
            self.longitude = geo_data["lon"]
            
            # Get timezone for the coordinates
            self.timezone_offset = get_timezone(self.latitude, self.longitude)
            
            logger.info(f"Geocoded '{self.place}' to lat: {self.latitude}, lon: {self.longitude}, tz: {self.timezone_offset}")
            return self
                
        except Exception as e:
            # Log the error and raise a user-friendly message
            logger.error(f"Error geocoding place '{self.place}': {str(e)}")
            raise ValueError(f"Could not determine coordinates for place: {self.place}. Please check the place name and try again.")

class TransitRequest(HoroscopeRequest):
    """
    Request model for transit calculations.
    Inherits all fields from HoroscopeRequest and adds transit_date.
    """
    transit_date: str = Field(..., description="Date for the transit calculation (YYYY-MM-DD format)")
    
    @validator('transit_date')
    def validate_transit_date(cls, v):
        try:
            # Parse the date to validate format
            parsed_date = datetime.strptime(v, "%Y-%m-%d")
            
            # Ensure the date is not in the future
            if parsed_date.date() > datetime.now().date():
                logger.warning(f"Transit date {v} is in the future")
                
            return v
        except ValueError:
            raise ValueError("transit_date must be in YYYY-MM-DD format") 