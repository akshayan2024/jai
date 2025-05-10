from typing import List, Dict, Tuple, Set
from api.models.astrological import Planet, Sign, PlanetPosition, Aspect

class AspectCalculator:
    """Calculator for planetary aspects"""
    
    # Major aspects and their orb allowances
    MAJOR_ASPECTS = {
        "Conjunction": 10,    # 0 degrees
        "Opposition": 10,     # 180 degrees
        "Trine": 8,          # 120 degrees
        "Square": 8,         # 90 degrees
        "Sextile": 6         # 60 degrees
    }
    
    # Special aspects for specific planets
    SPECIAL_ASPECTS = {
        Planet.JUPITER: {
            "Trine": 8,      # 120 degrees
            "Opposition": 10  # 180 degrees
        },
        Planet.SATURN: {
            "Trine": 8,      # 120 degrees
            "Opposition": 10, # 180 degrees
            "Square": 8      # 90 degrees
        },
        Planet.MARS: {
            "Square": 8,     # 90 degrees
            "Opposition": 10, # 180 degrees
            "Trine": 8       # 120 degrees
        }
    }
    
    def __init__(self):
        self.aspect_angles = {
            "Conjunction": 0,
            "Opposition": 180,
            "Trine": 120,
            "Square": 90,
            "Sextile": 60
        }
    
    def calculate_absolute_longitude(self, position: PlanetPosition) -> float:
        """Calculate absolute longitude (0-360) from sign and degree"""
        return (position.sign.value - 1) * 30 + position.degree
    
    def calculate_aspect_distance(self, pos1: float, pos2: float) -> float:
        """Calculate the angular distance between two positions"""
        diff = abs(pos1 - pos2)
        return min(diff, 360 - diff)
    
    def is_aspect_forming(self, distance: float, aspect_type: str, orb: float) -> bool:
        """Check if an aspect is forming within the given orb"""
        aspect_angle = self.aspect_angles[aspect_type]
        return abs(distance - aspect_angle) <= orb
    
    def calculate_aspect_strength(self, distance: float, aspect_type: str, orb: float) -> float:
        """Calculate the strength of an aspect (0.0 to 1.0)"""
        aspect_angle = self.aspect_angles[aspect_type]
        deviation = abs(distance - aspect_angle)
        return max(0.0, 1.0 - (deviation / orb))
    
    def get_planet_aspects(self, planet: Planet) -> Dict[str, float]:
        """Get the aspects and orbs for a specific planet"""
        aspects = self.MAJOR_ASPECTS.copy()
        if planet in self.SPECIAL_ASPECTS:
            aspects.update(self.SPECIAL_ASPECTS[planet])
        return aspects
    
    def calculate_aspects(self, planets: List[PlanetPosition]) -> List[Aspect]:
        """Calculate all aspects between planets"""
        aspects = []
        planet_positions = {p.planet: p for p in planets}
        
        # Calculate aspects for each planet pair
        for p1 in planets:
            p1_longitude = self.calculate_absolute_longitude(p1)
            p1_aspects = self.get_planet_aspects(p1.planet)
            
            for p2 in planets:
                if p1.planet == p2.planet:
                    continue
                
                p2_longitude = self.calculate_absolute_longitude(p2)
                distance = self.calculate_aspect_distance(p1_longitude, p2_longitude)
                
                # Check each possible aspect
                for aspect_type, orb in p1_aspects.items():
                    if self.is_aspect_forming(distance, aspect_type, orb):
                        strength = self.calculate_aspect_strength(distance, aspect_type, orb)
                        aspects.append(Aspect(
                            planet1=p1.planet,
                            planet2=p2.planet,
                            aspect_type=aspect_type,
                            distance=distance,
                            strength=strength
                        ))
        
        return aspects
    
    def get_aspects_for_planet(self, planet: Planet, all_aspects: List[Aspect]) -> List[Aspect]:
        """Get all aspects involving a specific planet"""
        return [a for a in all_aspects if a.planet1 == planet or a.planet2 == planet]
    
    def get_aspects_between_planets(self, planet1: Planet, planet2: Planet, all_aspects: List[Aspect]) -> List[Aspect]:
        """Get all aspects between two specific planets"""
        return [a for a in all_aspects if 
                (a.planet1 == planet1 and a.planet2 == planet2) or 
                (a.planet1 == planet2 and a.planet2 == planet1)] 