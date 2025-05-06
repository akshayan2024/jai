"""
Mahadasha service module for Vimshottari Mahadasha calculations.
"""

import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple

from ..utils.logger import get_logger
from ..utils.custom_exceptions import CalculationError
from ..constants import get_constant
from .ephemeris_service import get_planet_position
from ..constants.ayanamsa import AYANAMSA_LAHIRI
from ..constants.nakshatras import get_nakshatra_from_longitude

logger = get_logger(__name__)

def calculate_mahadasha(julian_day: float, birth_date: str, ayanamsa=AYANAMSA_LAHIRI) -> Dict[str, Any]:
    """
    Calculate Vimshottari Mahadasha periods.
    
    Args:
        julian_day (float): Julian day for the calculation
        birth_date (str): Birth date in YYYY-MM-DD format
        ayanamsa (int): Ayanamsa to use
        
    Returns:
        dict: Mahadasha periods with start and end dates
    """
    try:
        logger.debug(f"Calculating Vimshottari Mahadasha: JD={julian_day}")
        
        # Get required constants
        dasha_years = get_constant('dasha_years')
        nakshatra_lords = get_constant('nakshatra_lords')
        planets = get_constant('planets')
        nakshatras = get_constant('nakshatras')
        total_dasha_years = get_constant('total_dasha_years')
        
        # Get Moon's position
        moon_position = get_planet_position(julian_day, 1, ayanamsa)
        moon_longitude = moon_position["longitude"]
        
        # Get Moon's nakshatra
        nakshatra_idx = get_nakshatra_from_longitude(moon_longitude)
        nakshatra = nakshatras[nakshatra_idx]
        nakshatra_name = nakshatra["name"]
        
        # Get ruling planet (lord) of this nakshatra
        nakshatra_lord_idx = nakshatra_lords[nakshatra_idx]
        nakshatra_lord = planets[nakshatra_lord_idx]["name"]
        
        # Calculate balance of dasha
        nakshatra_start = nakshatra["start_degree"]
        nakshatra_end = nakshatra["end_degree"]
        nakshatra_span = nakshatra_end - nakshatra_start
        
        # Current position within nakshatra (0 to 1)
        position_in_nakshatra = (moon_longitude - nakshatra_start) / nakshatra_span
        
        # Balance of current dasha (0 to 1)
        dasha_balance = 1.0 - position_in_nakshatra
        
        # Convert to years
        years_of_first_dasha = dasha_years[nakshatra_lord_idx]
        balance_years = years_of_first_dasha * dasha_balance
        
        # Parse birth date
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        
        # Generate sequence of mahadashas
        mahadashas = []
        current_date = birth_date_obj
        
        # Define the sequence of planets starting with the nakshatra lord
        planet_sequence = []
        found_lord = False
        
        # First find the nakshatra lord in the list
        for idx in range(1, 10):
            if idx == nakshatra_lord_idx:
                found_lord = True
            
            if found_lord:
                planet_sequence.append(idx)
        
        # Then add planets before the nakshatra lord
        for idx in range(1, 10):
            if idx == nakshatra_lord_idx:
                break
            planet_sequence.append(idx)
        
        # First period with balance
        first_planet_idx = nakshatra_lord_idx
        first_planet = planets[first_planet_idx]["name"]
        first_years = balance_years
        first_end_date = current_date + timedelta(days=int(first_years * 365.25))
        
        mahadashas.append({
            "planet": first_planet,
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": first_end_date.strftime("%Y-%m-%d"),
            "years": round(first_years, 2)
        })
        
        current_date = first_end_date
        
        # Generate subsequent periods
        for planet_idx in planet_sequence[1:]:  # Skip the first planet (already calculated)
            planet = planets[planet_idx]["name"]
            years = dasha_years[planet_idx]
            end_date = current_date + timedelta(days=int(years * 365.25))
            
            mahadashas.append({
                "planet": planet,
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "years": years
            })
            
            current_date = end_date
        
        # Return Moon position and mahadasha periods
        return {
            "moon": {
                "longitude": moon_longitude,
                "nakshatra_index": nakshatra_idx,
                "nakshatra_name": nakshatra_name,
                "nakshatra_lord": nakshatra_lord
            },
            "mahadashas": mahadashas
        }
    
    except Exception as e:
        logger.error(f"Error calculating mahadasha: {str(e)}")
        raise CalculationError(f"Failed to calculate mahadasha: {str(e)}")

def calculate_antardasha(mahadasha: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate Antardasha (sub-periods) for a Mahadasha period.
    
    Args:
        mahadasha (dict): Mahadasha period information
        
    Returns:
        dict: Mahadasha with antardasha periods
    """
    try:
        # Get planet data
        planets = get_constant('planets')
        dasha_years = get_constant('dasha_years')
        planet_names = {planet["name"]: idx for idx, planet in planets.items()}
        
        mahadasha_planet = mahadasha["planet"]
        start_date_str = mahadasha["start_date"]
        years = mahadasha["years"]
        
        # Get the planet index for the mahadasha
        planet_idx = planet_names.get(mahadasha_planet)
        if not planet_idx:
            raise CalculationError(f"Invalid planet name: {mahadasha_planet}")
        
        # Define the sequence of planets for antardashas
        # Start with the mahadasha planet
        antardasha_sequence = []
        found_planet = False
        
        # First find the mahadasha planet in the list
        for idx in range(1, 10):
            if idx == planet_idx:
                found_planet = True
            
            if found_planet:
                antardasha_sequence.append(idx)
        
        # Then add planets before the mahadasha planet
        for idx in range(1, 10):
            if idx == planet_idx:
                break
            antardasha_sequence.append(idx)
        
        # Parse start date
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        
        # Calculate antardasha periods
        antardashas = []
        current_date = start_date
        
        for antardasha_planet_idx in antardasha_sequence:
            antardasha_planet = planets[antardasha_planet_idx]["name"]
            
            # Calculate proportion and duration
            planet_years = dasha_years[antardasha_planet_idx]
            proportion = planet_years / 120.0
            
            antardasha_years = years * proportion
            antardasha_days = int(antardasha_years * 365.25)
            
            # Calculate end date
            end_date = current_date + timedelta(days=antardasha_days)
            
            # Add to antardashas
            antardashas.append({
                "planet": antardasha_planet,
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "months": round(antardasha_years * 12, 1)
            })
            
            current_date = end_date
        
        # Update mahadasha with antardashas
        result = mahadasha.copy()
        result["antardashas"] = antardashas
        
        return result
    
    except Exception as e:
        logger.error(f"Error calculating antardasha: {str(e)}")
        raise CalculationError(f"Failed to calculate antardasha: {str(e)}")

def get_balance_years(julian_day: float, ayanamsa=AYANAMSA_LAHIRI) -> Tuple[str, float]:
    """
    Calculate balance of years in the current mahadasha.
    
    Args:
        julian_day (float): Julian day for the calculation
        ayanamsa (int): Ayanamsa to use
        
    Returns:
        tuple: (Planet name, balance years)
    """
    try:
        # Get required constants
        dasha_years = get_constant('dasha_years')
        nakshatra_lords = get_constant('nakshatra_lords')
        planets = get_constant('planets')
        nakshatras = get_constant('nakshatras')
        
        # Get Moon's position
        moon_position = get_planet_position(julian_day, 1, ayanamsa)
        moon_longitude = moon_position["longitude"]
        
        # Get Moon's nakshatra
        nakshatra_idx = get_nakshatra_from_longitude(moon_longitude)
        
        # Get ruling planet of this nakshatra
        nakshatra_lord_idx = nakshatra_lords[nakshatra_idx]
        nakshatra_lord = planets[nakshatra_lord_idx]["name"]
        
        # Calculate balance of dasha
        nakshatra_start = nakshatras[nakshatra_idx]["start_degree"]
        nakshatra_end = nakshatras[nakshatra_idx]["end_degree"]
        nakshatra_span = nakshatra_end - nakshatra_start
        
        # Current position within nakshatra (0 to 1)
        position_in_nakshatra = (moon_longitude - nakshatra_start) / nakshatra_span
        
        # Balance of current dasha (0 to 1)
        dasha_balance = 1.0 - position_in_nakshatra
        
        # Convert to years
        years_of_dasha = dasha_years[nakshatra_lord_idx]
        balance_years = years_of_dasha * dasha_balance
        
        return (nakshatra_lord, balance_years)
    
    except Exception as e:
        logger.error(f"Error calculating dasha balance: {str(e)}")
        raise CalculationError(f"Failed to calculate dasha balance: {str(e)}")

def calculate_pratyantardasha(antardasha: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate Pratyantardasha (sub-sub-periods) for an Antardasha period.
    
    Args:
        antardasha (dict): Antardasha period information
        
    Returns:
        dict: Antardasha with pratyantardasha periods
    """
    try:
        # Get planet data
        planets = get_constant('planets')
        dasha_years = get_constant('dasha_years')
        planet_names = {planet["name"]: idx for idx, planet in planets.items()}
        
        antardasha_planet = antardasha["planet"]
        start_date_str = antardasha["start_date"]
        end_date_str = antardasha["end_date"]
        
        # Calculate total months
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        # Calculate duration in days, then convert to months
        duration_days = (end_date - start_date).days
        total_months = duration_days / 30.4375  # Average days per month
        
        # Get the planet index for the antardasha
        planet_idx = planet_names.get(antardasha_planet)
        if not planet_idx:
            raise CalculationError(f"Invalid planet name: {antardasha_planet}")
        
        # Define the sequence of planets for pratyantardashas
        # Start with the antardasha planet
        pratyantardasha_sequence = []
        found_planet = False
        
        # First find the antardasha planet in the list
        for idx in range(1, 10):
            if idx == planet_idx:
                found_planet = True
            
            if found_planet:
                pratyantardasha_sequence.append(idx)
        
        # Then add planets before the antardasha planet
        for idx in range(1, 10):
            if idx == planet_idx:
                break
            pratyantardasha_sequence.append(idx)
        
        # Calculate pratyantardasha periods
        pratyantardashas = []
        current_date = start_date
        
        for pratyantardasha_planet_idx in pratyantardasha_sequence:
            pratyantardasha_planet = planets[pratyantardasha_planet_idx]["name"]
            
            # Calculate proportion and duration
            planet_years = dasha_years[pratyantardasha_planet_idx]
            proportion = planet_years / 120.0
            
            # Calculate duration in days
            pratyantardasha_months = total_months * proportion
            pratyantardasha_days = int(pratyantardasha_months * 30.4375)
            
            # Calculate end date (make sure not to exceed the antardasha end date)
            end_date_calculated = current_date + timedelta(days=pratyantardasha_days)
            if end_date_calculated > end_date:
                end_date_calculated = end_date
            
            # Add to pratyantardashas
            pratyantardashas.append({
                "planet": pratyantardasha_planet,
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": end_date_calculated.strftime("%Y-%m-%d"),
                "days": (end_date_calculated - current_date).days
            })
            
            current_date = end_date_calculated
            
            # If we've reached the end date, break out of the loop
            if current_date >= end_date:
                break
        
        # Update antardasha with pratyantardashas
        result = antardasha.copy()
        result["pratyantardashas"] = pratyantardashas
        
        return result
    
    except Exception as e:
        logger.error(f"Error calculating pratyantardasha: {str(e)}")
        raise CalculationError(f"Failed to calculate pratyantardasha: {str(e)}") 