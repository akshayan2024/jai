from datetime import datetime
from typing import List, Dict, Optional
import logging
from api.models.astrological import (
    Planet, Sign, PlanetPosition, HousePosition,
    BirthData, HoroscopeResponse, Yoga, DashaPeriod,
    TransitPosition, TransitResponse, Aspect
)
from api.services.yoga_calculations import YogaCalculator
from api.services.dasha_calculations import DashaCalculator
from api.services.aspect_calculations import AspectCalculator
from api.services.ephemeris_service import ephemeris_service
from api.utils.input_validation import validate_extreme_latitude
import os
from datetime import timedelta

# Configure logging
logger = logging.getLogger("jai-api.astrological")

# Debug flag for development features
DEBUG_MODE = False

class AstrologicalCalculator:
    """Main calculator for astrological calculations"""
    
    def __init__(self):
        # Initialize calculators
        self.yoga_calculator = YogaCalculator()
        self.dasha_calculator = DashaCalculator()
        self.aspect_calculator = AspectCalculator()
        self.ephemeris_path = os.environ.get("EPHEMERIS_PATH", "./ephemeris")
        
    def calculate_ascendant(self, birth_data: BirthData) -> HousePosition:
        """Calculate the ascendant (Lagna) for given birth data"""
        # Convert date to Julian day
        jd = ephemeris_service.julday(
            birth_data.date.year,
            birth_data.date.month,
            birth_data.date.day,
            birth_data.date.hour + birth_data.date.minute/60.0
        )
        
        # Calculate ascendant
        asc_longitude, _ = ephemeris_service.get_ascendant(jd, birth_data.latitude, birth_data.longitude)
        
        # Convert to sign and degree
        sign_num = int(asc_longitude / 30) + 1
        degree = asc_longitude % 30
        
        return HousePosition(
            house_number=1,
            sign=Sign(sign_num),
            degree=degree
        )
    
    def calculate_planet_positions(self, birth_data: BirthData) -> List[PlanetPosition]:
        """Calculate positions of all planets for given birth data"""
        jd = ephemeris_service.julday(
            birth_data.date.year,
            birth_data.date.month,
            birth_data.date.day,
            birth_data.date.hour + birth_data.date.minute/60.0
        )
        
        positions = []
        for planet in Planet:
            if planet in [Planet.RAHU, Planet.KETU]:
                # Calculate Rahu/Ketu (Lunar nodes)
                result = ephemeris_service.get_planet_position(jd, swe.MEAN_NODE)
                degree = result["longitude"]
                # Both nodes are always retrograde in nature
                is_retrograde = True
                
                if planet == Planet.KETU:
                    degree = (degree + 180) % 360
                    # Ketu inherits Rahu's speed (both are retrograde)
                    speed = result["speed"]  # Don't negate the speed
                else:
                    speed = result["speed"]
                
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
                result = ephemeris_service.get_planet_position(jd, planet_id)
                degree = result["longitude"]
                # Sun and Moon are never retrograde
                if planet in [Planet.SUN, Planet.MOON]:
                    is_retrograde = False
                else:
                    is_retrograde = result["speed"] < 0
                
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
        jd = ephemeris_service.julday(
            date.year,
            date.month,
            date.day,
            date.hour + date.minute/60.0
        )
        
        positions = []
        for planet in Planet:
            if planet in [Planet.RAHU, Planet.KETU]:
                result = ephemeris_service.get_planet_position(jd, swe.MEAN_NODE)
                degree = result["longitude"]
                is_retrograde = result["speed"] < 0
                
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
                result = ephemeris_service.get_planet_position(jd, planet_id)
                degree = result["longitude"]
                is_retrograde = result["speed"] < 0
                
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
        return ephemeris_service.get_planet_dignity(self._get_planet_id(planet), sign.value - 1)

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

    def calculate_horoscope(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        house_system: str = 'W',
        ayanamsa: int = 1
    ) -> Dict:
        """
        Calculate a complete horoscope.
        
        Args:
            date: Date and time
            latitude: Latitude
            longitude: Longitude
            house_system: House system (default: Whole Sign)
            ayanamsa: Ayanamsa to use (default: Lahiri)
            
        Returns:
            Dictionary containing horoscope data
        """
        # Validate extreme latitude
        validate_extreme_latitude(latitude)
        
        with ephemeris_service.ephemeris_context(
            ephe_path=self.ephemeris_path,
            sid_mode=ayanamsa
        ) as ephe:
            try:
                # Calculate Julian day
                jd = ephe.julday(
                    date.year,
                    date.month,
                    date.day,
                    date.hour + date.minute / 60.0
                )
                
                # Calculate houses
                cusps, ascmc = ephe.get_ascendant(jd, latitude, longitude, house_system)
                
                # Calculate planet positions
                planets = []
                for planet in range(10):  # Sun through Rahu
                    pos = ephe.get_planet_position(jd, planet)
                    planets.append({
                        'planet': planet,
                        'longitude': pos[0],
                        'latitude': pos[1],
                        'distance': pos[2],
                        'speed': pos[3]
                    })
                
                return {
                    'ascendant': ascmc[0],
                    'mc': ascmc[1],
                    'armc': ascmc[2],
                    'vertex': ascmc[3],
                    'equatorial_ascendant': ascmc[4],
                    'house_cusps': cusps,
                    'planets': planets
                }
                
            except Exception as e:
                logger.error(f"Error calculating horoscope: {str(e)}")
                raise RuntimeError(f"Horoscope calculation failed: {str(e)}")
    
    def calculate_transits(
        self,
        birth_date: datetime,
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime,
        house_system: str = 'W',
        ayanamsa: int = 1
    ) -> List[Dict]:
        """
        Calculate planetary transits for a period.
        
        Args:
            birth_date: Birth date and time
            latitude: Latitude
            longitude: Longitude
            start_date: Start date for transits
            end_date: End date for transits
            house_system: House system (default: Whole Sign)
            ayanamsa: Ayanamsa to use (default: Lahiri)
            
        Returns:
            List of transit events
        """
        with ephemeris_service.ephemeris_context(
            ephe_path=self.ephemeris_path,
            sid_mode=ayanamsa
        ) as ephe:
            try:
                # Calculate birth chart
                birth_jd = ephe.julday(
                    birth_date.year,
                    birth_date.month,
                    birth_date.day,
                    birth_date.hour + birth_date.minute / 60.0
                )
                birth_cusps, birth_ascmc = ephe.get_ascendant(
                    birth_jd,
                    latitude,
                    longitude,
                    house_system
                )
                
                # Calculate transits
                transits = []
                current_date = start_date
                while current_date <= end_date:
                    transit_jd = ephe.julday(
                        current_date.year,
                        current_date.month,
                        current_date.day,
                        current_date.hour + current_date.minute / 60.0
                    )
                    
                    # Calculate transit positions
                    for planet in range(10):
                        pos = ephe.get_planet_position(transit_jd, planet)
                        transits.append({
                            'date': current_date,
                            'planet': planet,
                            'longitude': pos[0],
                            'latitude': pos[1],
                            'distance': pos[2],
                            'speed': pos[3]
                        })
                    
                    current_date += timedelta(days=1)
                
                return transits
                
            except Exception as e:
                logger.error(f"Error calculating transits: {str(e)}")
                raise RuntimeError(f"Transit calculation failed: {str(e)}")
    
    def calculate_progressions(
        self,
        birth_date: datetime,
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime,
        house_system: str = 'W',
        ayanamsa: int = 1
    ) -> List[Dict]:
        """
        Calculate secondary progressions for a period.
        
        Args:
            birth_date: Birth date and time
            latitude: Latitude
            longitude: Longitude
            start_date: Start date for progressions
            end_date: End date for progressions
            house_system: House system (default: Whole Sign)
            ayanamsa: Ayanamsa to use (default: Lahiri)
            
        Returns:
            List of progression events
        """
        with ephemeris_service.ephemeris_context(
            ephe_path=self.ephemeris_path,
            sid_mode=ayanamsa
        ) as ephe:
            try:
                # Calculate birth chart
                birth_jd = ephe.julday(
                    birth_date.year,
                    birth_date.month,
                    birth_date.day,
                    birth_date.hour + birth_date.minute / 60.0
                )
                
                # Calculate progressions
                progressions = []
                current_date = start_date
                while current_date <= end_date:
                    # Calculate progressed date (1 day = 1 year)
                    years = (current_date - birth_date).days / 365.25
                    progressed_date = birth_date + timedelta(days=years)
                    
                    progressed_jd = ephe.julday(
                        progressed_date.year,
                        progressed_date.month,
                        progressed_date.day,
                        progressed_date.hour + progressed_date.minute / 60.0
                    )
                    
                    # Calculate progressed positions
                    for planet in range(10):
                        pos = ephe.get_planet_position(progressed_jd, planet)
                        progressions.append({
                            'date': current_date,
                            'planet': planet,
                            'longitude': pos[0],
                            'latitude': pos[1],
                            'distance': pos[2],
                            'speed': pos[3]
                        })
                    
                    current_date += timedelta(days=1)
                
                return progressions
                
            except Exception as e:
                logger.error(f"Error calculating progressions: {str(e)}")
                raise RuntimeError(f"Progression calculation failed: {str(e)}") 