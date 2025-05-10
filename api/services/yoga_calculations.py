from typing import List, Dict, Set
from api.models.astrological import Planet, Sign, PlanetPosition, HousePosition, Yoga

class YogaCalculator:
    def __init__(self):
        # Define common yogas and their rules
        self.yoga_rules = {
            "Gaja Kesari Yoga": {
                "description": "Formed when Jupiter aspects the Moon or vice versa",
                "planets": {Planet.JUPITER, Planet.MOON},
                "check": self._check_gaja_kesari
            },
            "Budha-Aditya Yoga": {
                "description": "Formed when Mercury and Sun are in conjunction",
                "planets": {Planet.MERCURY, Planet.SUN},
                "check": self._check_budha_aditya
            },
            "Raja Yoga": {
                "description": "Formed when lords of Kendra (1,4,7,10) and Trikona (1,5,9) houses are in conjunction or aspect",
                "planets": set(),  # Dynamic based on house lords
                "check": self._check_raja_yoga
            },
            "Kemadruma Yoga": {
                "description": "Formed when Moon has no planets in adjacent houses",
                "planets": {Planet.MOON},
                "check": self._check_kemadruma
            },
            "Sakata Yoga": {
                "description": "Formed when Jupiter and Moon are in 6-8 relationship",
                "planets": {Planet.JUPITER, Planet.MOON},
                "check": self._check_sakata
            }
        }
    
    def calculate_yogas(self, planets: List[PlanetPosition], houses: List[HousePosition]) -> List[Yoga]:
        """Calculate all applicable yogas based on planet and house positions"""
        yogas = []
        
        # Create lookup dictionaries for faster access
        planet_positions = {p.planet: p for p in planets}
        house_positions = {h.house_number: h for h in houses}
        
        # Check each yoga
        for yoga_name, yoga_info in self.yoga_rules.items():
            if self._check_yoga_planets_present(planet_positions, yoga_info["planets"]):
                if yoga_info["check"](planet_positions, house_positions):
                    yogas.append(Yoga(
                        name=yoga_name,
                        planets=list(yoga_info["planets"]),
                        description=yoga_info["description"],
                        strength=self._calculate_yoga_strength(yoga_name, planet_positions, house_positions)
                    ))
        
        return yogas
    
    def _check_yoga_planets_present(self, planet_positions: Dict[Planet, PlanetPosition], required_planets: Set[Planet]) -> bool:
        """Check if all required planets for a yoga are present"""
        return all(planet in planet_positions for planet in required_planets)
    
    def _check_gaja_kesari(self, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> bool:
        """Check for Gaja Kesari Yoga"""
        jupiter = planet_positions[Planet.JUPITER]
        moon = planet_positions[Planet.MOON]
        
        # Check if Jupiter aspects Moon (trine or opposition)
        jupiter_house = self._get_planet_house(jupiter, house_positions)
        moon_house = self._get_planet_house(moon, house_positions)
        
        return self._is_aspect(jupiter_house, moon_house, [5, 9])  # Trine aspects
    
    def _check_budha_aditya(self, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> bool:
        """Check for Budha-Aditya Yoga"""
        mercury = planet_positions[Planet.MERCURY]
        sun = planet_positions[Planet.SUN]
        
        # Check if Mercury and Sun are in the same sign
        return mercury.sign == sun.sign
    
    def _check_raja_yoga(self, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> bool:
        """Check for Raja Yoga"""
        kendra_houses = {1, 4, 7, 10}
        trikona_houses = {1, 5, 9}
        
        # Get lords of Kendra and Trikona houses
        kendra_lords = self._get_house_lords(kendra_houses, house_positions)
        trikona_lords = self._get_house_lords(trikona_houses, house_positions)
        
        # Check if any Kendra lord aspects any Trikona lord
        for kendra_lord in kendra_lords:
            for trikona_lord in trikona_lords:
                if self._is_aspect(
                    self._get_planet_house(kendra_lord, house_positions),
                    self._get_planet_house(trikona_lord, house_positions),
                    [1, 5, 7, 9]  # Conjunction and major aspects
                ):
                    return True
        
        return False
    
    def _check_kemadruma(self, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> bool:
        """Check for Kemadruma Yoga"""
        moon = planet_positions[Planet.MOON]
        moon_house = self._get_planet_house(moon, house_positions)
        
        # Check if there are any planets in houses 12 and 2 from Moon
        house_12 = (moon_house - 1) % 12 or 12
        house_2 = moon_house % 12 + 1
        
        return not any(p for p in planets if self._get_planet_house(p, house_positions) in {house_12, house_2})
    
    def _check_sakata(self, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> bool:
        """Check for Sakata Yoga"""
        jupiter = planet_positions[Planet.JUPITER]
        moon = planet_positions[Planet.MOON]
        
        jupiter_house = self._get_planet_house(jupiter, house_positions)
        moon_house = self._get_planet_house(moon, house_positions)
        
        # Check if houses are in 6-8 relationship
        return abs(jupiter_house - moon_house) in {6, 8}
    
    def _get_planet_house(self, planet: PlanetPosition, house_positions: Dict[int, HousePosition]) -> int:
        """Get the house number where a planet is placed"""
        for house_num, house in house_positions.items():
            if planet.sign == house.sign:
                return house_num
        return 0
    
    def _get_house_lords(self, houses: Set[int], house_positions: Dict[int, HousePosition]) -> Set[Planet]:
        """Get the lords of the specified houses"""
        lords = set()
        for house_num in houses:
            sign = house_positions[house_num].sign
            # Map sign to its lord
            lord = self._get_sign_lord(sign)
            if lord:
                lords.add(lord)
        return lords
    
    def _get_sign_lord(self, sign: Sign) -> Planet:
        """Get the lord of a zodiac sign"""
        sign_lords = {
            Sign.ARIES: Planet.MARS,
            Sign.TAURUS: Planet.VENUS,
            Sign.GEMINI: Planet.MERCURY,
            Sign.CANCER: Planet.MOON,
            Sign.LEO: Planet.SUN,
            Sign.VIRGO: Planet.MERCURY,
            Sign.LIBRA: Planet.VENUS,
            Sign.SCORPIO: Planet.MARS,
            Sign.SAGITTARIUS: Planet.JUPITER,
            Sign.CAPRICORN: Planet.SATURN,
            Sign.AQUARIUS: Planet.SATURN,
            Sign.PISCES: Planet.JUPITER
        }
        return sign_lords.get(sign)
    
    def _is_aspect(self, house1: int, house2: int, aspects: List[int]) -> bool:
        """Check if two houses are in aspect"""
        if not house1 or not house2:
            return False
        diff = abs(house1 - house2)
        return diff in aspects or (12 - diff) in aspects
    
    def _calculate_yoga_strength(self, yoga_name: str, planet_positions: Dict[Planet, PlanetPosition], house_positions: Dict[int, HousePosition]) -> float:
        """Calculate the strength of a yoga (0.0 to 1.0)"""
        # Basic implementation - can be enhanced with more sophisticated calculations
        base_strength = 0.7  # Base strength for any yoga
        
        # Adjust strength based on house placement
        if yoga_name == "Raja Yoga":
            # Raja Yoga is stronger in Kendra houses
            kendra_houses = {1, 4, 7, 10}
            planets_in_kendra = sum(1 for p in planet_positions.values() 
                                  if self._get_planet_house(p, house_positions) in kendra_houses)
            base_strength += min(0.3, planets_in_kendra * 0.1)
        
        return min(1.0, base_strength) 