from datetime import datetime
from typing import List, Dict, Optional
import swisseph as swe
import logging
from api.models.astrological import (
    Planet, Sign, PlanetPosition, HousePosition,
    BirthData, HoroscopeResponse, Yoga, DashaPeriod,
    TransitPosition, TransitResponse, Aspect
)
from api.services.yoga_calculations import YogaCalculator
from api.services.dasha_calculations import DashaCalculator
from api.services.aspect_calculations import AspectCalculator

# Configure logging
logger = logging.getLogger("jai-api.astrological")

# Debug flag for development features
DEBUG_MODE = False

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
                # Both nodes are always retrograde in nature
                is_retrograde = True
                
                if planet == Planet.KETU:
                    degree = (degree + 180) % 360
                    # Ketu inherits Rahu's speed (both are retrograde)
                    speed = result[3]  # Don't negate the speed
                else:
                    speed = result[3]
                
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
                # Sun and Moon are never retrograde
                if planet in [Planet.SUN, Planet.MOON]:
                    is_retrograde = False
                else:
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
        
        if DEBUG_MODE:
            self._validate_chart(ascendant, planets, houses)
        
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

    def get_planet_dignity(self, planet: Planet, sign: Sign) -> str:
        """Get planet's dignity in a sign"""
        # Classical dignities for the seven planets
        exaltation_signs = {
            Planet.SUN: Sign.ARIES,
            Planet.MOON: Sign.TAURUS,
            Planet.MARS: Sign.CAPRICORN,
            Planet.MERCURY: Sign.VIRGO,
            Planet.JUPITER: Sign.CANCER,
            Planet.VENUS: Sign.PISCES,
            Planet.SATURN: Sign.LIBRA
        }
        
        debilitation_signs = {
            Planet.SUN: Sign.LIBRA,
            Planet.MOON: Sign.SCORPIO,
            Planet.MARS: Sign.CANCER,
            Planet.MERCURY: Sign.PISCES,
            Planet.JUPITER: Sign.CAPRICORN,
            Planet.VENUS: Sign.VIRGO,
            Planet.SATURN: Sign.ARIES
        }
        
        own_signs = {
            Planet.SUN: [Sign.LEO],
            Planet.MOON: [Sign.CANCER],
            Planet.MARS: [Sign.ARIES, Sign.SCORPIO],
            Planet.MERCURY: [Sign.GEMINI, Sign.VIRGO],
            Planet.JUPITER: [Sign.SAGITTARIUS, Sign.PISCES],
            Planet.VENUS: [Sign.TAURUS, Sign.LIBRA],
            Planet.SATURN: [Sign.CAPRICORN, Sign.AQUARIUS]
        }
        
        # Handle Rahu/Ketu separately as they don't have classical dignities
        if planet in [Planet.RAHU, Planet.KETU]:
            return "Neutral"  # Classical texts don't assign dignities to nodes
        
        if sign == exaltation_signs.get(planet):
            return "Exalted"
        elif sign == debilitation_signs.get(planet):
            return "Debilitated"
        elif sign in own_signs.get(planet, []):
            return "Own Sign"
        else:
            return "Neutral"

    def _validate_chart(self, ascendant: HousePosition, planets: List[PlanetPosition], houses: List[HousePosition]):
        """Internal validation for development/debugging only"""
        if not DEBUG_MODE:
            return
            
        # Validate house sequence
        for i in range(12):
            expected_sign = Sign((ascendant.sign.value + i - 1) % 12 + 1)
            if houses[i].sign != expected_sign:
                logger.warning(f"House {i+1} sign mismatch: expected {expected_sign}, got {houses[i].sign}")
        
        # Validate planet-house assignments
        for planet in planets:
            planet_longitude = planet.degree + (planet.sign.value - 1) * 30
            ascendant_longitude = ascendant.degree + (ascendant.sign.value - 1) * 30
            house_number = int((planet_longitude - ascendant_longitude) / 30) % 12 + 1
            
            if house_number < 1 or house_number > 12:
                logger.warning(f"Invalid house number {house_number} for planet {planet.planet}")
            elif planet not in houses[house_number-1].planets:
                logger.warning(f"Planet {planet.planet} not assigned to house {house_number}") 