from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from api.models.astrological import Planet, DashaPeriod

class DashaCalculator:
    """Calculator for Vimshottari Dasha periods"""
    
    # Vimshottari Dasha periods in years
    DASHA_PERIODS = {
        Planet.KETU: 7,
        Planet.VENUS: 20,
        Planet.SUN: 6,
        Planet.MOON: 10,
        Planet.MARS: 7,
        Planet.RAHU: 18,
        Planet.JUPITER: 16,
        Planet.SATURN: 19,
        Planet.MERCURY: 17
    }
    
    # Order of planets in Vimshottari Dasha
    DASHA_ORDER = [
        Planet.KETU,
        Planet.VENUS,
        Planet.SUN,
        Planet.MOON,
        Planet.MARS,
        Planet.RAHU,
        Planet.JUPITER,
        Planet.SATURN,
        Planet.MERCURY
    ]
    
    def __init__(self):
        self.total_dasha_years = sum(self.DASHA_PERIODS.values())
    
    def calculate_moon_nakshatra(self, moon_longitude: float) -> Tuple[int, float]:
        """
        Calculate the nakshatra (lunar mansion) and its degree based on moon's longitude.
        Each nakshatra spans 13°20' (13.3333 degrees).
        """
        nakshatra_number = int(moon_longitude / 13.3333)
        nakshatra_degree = moon_longitude % 13.3333
        return nakshatra_number, nakshatra_degree
    
    def calculate_dasha_balance(self, moon_longitude: float) -> Tuple[Planet, float]:
        """
        Calculate the current dasha lord and remaining balance based on moon's longitude.
        Returns (dasha_lord, remaining_years)
        """
        nakshatra_number, nakshatra_degree = self.calculate_moon_nakshatra(moon_longitude)
        
        # Calculate which dasha lord is active
        dasha_index = nakshatra_number % len(self.DASHA_ORDER)
        dasha_lord = self.DASHA_ORDER[dasha_index]
        
        # Calculate remaining years in current dasha
        total_degrees = 13.3333  # degrees in one nakshatra
        remaining_degrees = total_degrees - nakshatra_degree
        remaining_years = (remaining_degrees / total_degrees) * self.DASHA_PERIODS[dasha_lord]
        
        return dasha_lord, remaining_years
    
    def calculate_sub_periods(self, main_period: DashaPeriod) -> List[DashaPeriod]:
        """
        Calculate sub-periods (bhuktis) for a main dasha period.
        Returns a list of DashaPeriod objects.
        """
        sub_periods = []
        main_planet = main_period.planet
        main_duration = (main_period.end_date - main_period.start_date).days / 365.25
        
        # Find the index of the main period planet in DASHA_ORDER
        main_index = self.DASHA_ORDER.index(main_planet)
        
        # Calculate sub-periods
        current_date = main_period.start_date
        for i in range(len(self.DASHA_ORDER)):
            # Get the sub-period planet
            sub_planet = self.DASHA_ORDER[(main_index + i) % len(self.DASHA_ORDER)]
            
            # Calculate sub-period duration
            sub_duration = (self.DASHA_PERIODS[sub_planet] / self.total_dasha_years) * main_duration
            end_date = current_date + timedelta(days=sub_duration * 365.25)
            
            sub_periods.append(DashaPeriod(
                planet=sub_planet,
                start_date=current_date,
                end_date=end_date
            ))
            
            current_date = end_date
        
        return sub_periods
    
    def calculate_dasha_periods(self, birth_date: datetime, moon_longitude: float) -> List[DashaPeriod]:
        """
        Calculate all dasha periods starting from birth date.
        Returns a list of DashaPeriod objects with sub-periods.
        """
        current_dasha, remaining_years = self.calculate_dasha_balance(moon_longitude)
        current_date = birth_date
        
        dasha_periods = []
        
        # Calculate periods for next 120 years (approximately 4 complete dasha cycles)
        years_covered = 0
        while years_covered < 120:
            # Find current dasha lord's position in the order
            dasha_index = self.DASHA_ORDER.index(current_dasha)
            
            # Calculate period for current dasha
            period_years = remaining_years if years_covered == 0 else self.DASHA_PERIODS[current_dasha]
            end_date = current_date + timedelta(days=period_years * 365.25)
            
            # Create main period
            main_period = DashaPeriod(
                planet=current_dasha,
                start_date=current_date,
                end_date=end_date
            )
            
            # Calculate sub-periods
            main_period.sub_periods = self.calculate_sub_periods(main_period)
            
            dasha_periods.append(main_period)
            
            # Move to next dasha lord
            current_dasha = self.DASHA_ORDER[(dasha_index + 1) % len(self.DASHA_ORDER)]
            current_date = end_date
            years_covered += period_years
            remaining_years = 0
        
        return dasha_periods 