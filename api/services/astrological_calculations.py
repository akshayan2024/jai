from datetime import datetime
from typing import List, Dict, Optional
import swisseph as swe
from api.models.astrological import (
    Planet, Sign, PlanetPosition, HousePosition,
    BirthData, HoroscopeResponse, Yoga, DashaPeriod,
    TransitPosition, TransitResponse, Aspect
)
from api.services.yoga_calculations import YogaCalculator
from api.services.dasha_calculations import DashaCalculator
from api.services.aspect_calculations import AspectCalculator

class AstrologicalCalculator:
    """Main calculator for astrological calculations"""
    
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path("ephemeris")
        # Initialize yoga calculator
        self.yoga_calculator = YogaCalculator()
        self.dasha_calculator = DashaCalculator()
        self.aspect_calculator = AspectCalculator()
        
    def calculate_ascendant(self, birth_data: BirthData) -> HousePosition:
        """Calculate the ascendant (Lagna) for given birth data"""
        # Convert date to Julian day
        jd = swe.julday(
            birth_data.date.year,
            birth_data.date.month,
            birth_data.date.day,
            birth_data.date.hour + birth_data.date.minute/60.0
        )
        
        # Calculate ascendant
        result = swe.houses(jd, birth_data.latitude, birth_data.longitude)
        ascendant_degree = result[0]  # Ascendant degree
        
        # Convert to sign and degree
        sign_num = int(ascendant_degree / 30) + 1
        degree = ascendant_degree % 30
        
        return HousePosition(
            house_number=1,
            sign=Sign(sign_num),
            degree=degree
        )
    
    def calculate_planet_positions(self, birth_data: BirthData) -> List[PlanetPosition]:
        """Calculate positions of all planets for given birth data"""
        jd = swe.julday(
            birth_data.date.year,
            birth_data.date.month,
            birth_data.date.day,
            birth_data.date.hour + birth_data.date.minute/60.0
        )
        
        positions = []
        for planet in Planet:
            if planet in [Planet.RAHU, Planet.KETU]:
                # Calculate Rahu/Ketu (Lunar nodes)
                result = swe.calc_ut(jd, swe.MEAN_NODE)
                degree = result[0]
                is_retrograde = result[3] < 0
                
                if planet == Planet.KETU:
                    degree = (degree + 180) % 360
                
                sign_num = int(degree / 30) + 1
                degree_in_sign = degree % 30
                
                positions.append(PlanetPosition(
                    planet=planet,
                    sign=Sign(sign_num),
                    degree=degree_in_sign,
                    is_retrograde=is_retrograde
                ))
            else:
                # Calculate other planets
                planet_id = self._get_planet_id(planet)
                result = swe.calc_ut(jd, planet_id)
                degree = result[0]
                is_retrograde = result[3] < 0
                
                sign_num = int(degree / 30) + 1
                degree_in_sign = degree % 30
                
                positions.append(PlanetPosition(
                    planet=planet,
                    sign=Sign(sign_num),
                    degree=degree_in_sign,
                    is_retrograde=is_retrograde
                ))
        
        return positions
    
    def calculate_houses(self, birth_data: BirthData, ascendant: HousePosition) -> List[HousePosition]:
        """Calculate house positions based on ascendant"""
        houses = []
        ascendant_degree = (ascendant.sign.value - 1) * 30 + ascendant.degree
        
        for i in range(12):
            house_degree = (ascendant_degree + i * 30) % 360
            sign_num = int(house_degree / 30) + 1
            degree = house_degree % 30
            
            houses.append(HousePosition(
                house_number=i + 1,
                sign=Sign(sign_num),
                degree=degree
            ))
        
        return houses
    
    def calculate_yogas(self, planets: List[PlanetPosition], houses: List[HousePosition]) -> List[Yoga]:
        """Calculate yogas based on planet and house positions"""
        return self.yoga_calculator.calculate_yogas(planets, houses)
    
    def calculate_dashas(self, birth_data: BirthData, moon_longitude: float) -> List[DashaPeriod]:
        """Calculate dasha periods based on birth data and moon's longitude"""
        return self.dasha_calculator.calculate_dasha_periods(birth_data.birth_time, moon_longitude)
    
    def calculate_aspects(self, planets: List[PlanetPosition]) -> List[Aspect]:
        """Calculate aspects between planets"""
        return self.aspect_calculator.calculate_aspects(planets)
    
    def calculate_horoscope(self, birth_data: BirthData) -> HoroscopeResponse:
        """Calculate complete horoscope"""
        # Calculate basic elements
        ascendant = self.calculate_ascendant(birth_data)
        planets = self.calculate_planet_positions(birth_data)
        houses = self.calculate_houses(birth_data, ascendant)
        
        # Calculate yogas
        yogas = self.calculate_yogas(planets, houses)
        
        # Calculate dashas
        # Get moon's longitude from planet positions
        moon_position = next(p for p in planets if p.planet == Planet.MOON)
        moon_longitude = moon_position.degree + (moon_position.sign.value - 1) * 30
        dashas = self.calculate_dashas(birth_data, moon_longitude)
        
        # Calculate aspects
        aspects = self.calculate_aspects(planets)
        
        return HoroscopeResponse(
            birth_data=birth_data,
            ascendant=ascendant,
            planets=planets,
            houses=houses,
            yogas=yogas,
            dashas=dashas,
            aspects=aspects
        )
    
    def calculate_transits(self, date: datetime, latitude: float, longitude: float) -> TransitResponse:
        """Calculate current planetary transits"""
        jd = swe.julday(
            date.year,
            date.month,
            date.day,
            date.hour + date.minute/60.0
        )
        
        positions = []
        for planet in Planet:
            if planet in [Planet.RAHU, Planet.KETU]:
                result = swe.calc_ut(jd, swe.MEAN_NODE)
                degree = result[0]
                is_retrograde = result[3] < 0
                
                if planet == Planet.KETU:
                    degree = (degree + 180) % 360
                
                sign_num = int(degree / 30) + 1
                degree_in_sign = degree % 30
                
                positions.append(TransitPosition(
                    planet=planet,
                    current_sign=Sign(sign_num),
                    current_degree=degree_in_sign,
                    is_retrograde=is_retrograde
                ))
            else:
                planet_id = self._get_planet_id(planet)
                result = swe.calc_ut(jd, planet_id)
                degree = result[0]
                is_retrograde = result[3] < 0
                
                sign_num = int(degree / 30) + 1
                degree_in_sign = degree % 30
                
                positions.append(TransitPosition(
                    planet=planet,
                    current_sign=Sign(sign_num),
                    current_degree=degree_in_sign,
                    is_retrograde=is_retrograde
                ))
        
        return TransitResponse(
            date=date,
            positions=positions
        )
    
    def _get_planet_id(self, planet: Planet) -> int:
        """Convert Planet enum to Swiss Ephemeris planet ID"""
        planet_map = {
            Planet.SUN: swe.SUN,
            Planet.MOON: swe.MOON,
            Planet.MARS: swe.MARS,
            Planet.MERCURY: swe.MERCURY,
            Planet.JUPITER: swe.JUPITER,
            Planet.VENUS: swe.VENUS,
            Planet.SATURN: swe.SATURN
        }
        return planet_map[planet] 