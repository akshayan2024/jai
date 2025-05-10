"""Planetary constants for Vedic astrology"""

from enum import Enum
from typing import Dict, List

class Planet(Enum):
    """Vedic planets"""
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"

# Sanskrit names for planets
PLANET_NAMES = {
    Planet.SUN: "Surya",
    Planet.MOON: "Chandra",
    Planet.MARS: "Mangala",
    Planet.MERCURY: "Budha",
    Planet.JUPITER: "Guru",
    Planet.VENUS: "Shukra",
    Planet.SATURN: "Shani",
    Planet.RAHU: "Rahu",
    Planet.KETU: "Ketu"
}

# Vimshottari dasha years
DASHA_YEARS = {
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

# Exaltation signs
EXALTATION_SIGNS = {
    Planet.SUN: 1,     # Aries
    Planet.MOON: 2,    # Taurus
    Planet.MARS: 10,   # Capricorn
    Planet.MERCURY: 6, # Virgo
    Planet.JUPITER: 4, # Cancer
    Planet.VENUS: 12,  # Pisces
    Planet.SATURN: 7   # Libra
}

# Debilitation signs
DEBILITATION_SIGNS = {
    Planet.SUN: 7,     # Libra
    Planet.MOON: 8,    # Scorpio
    Planet.MARS: 4,    # Cancer
    Planet.MERCURY: 12,# Pisces
    Planet.JUPITER: 10,# Capricorn
    Planet.VENUS: 6,   # Virgo
    Planet.SATURN: 1   # Aries
}

# Own signs (signs ruled by planets)
OWN_SIGNS = {
    Planet.SUN: [5],           # Leo
    Planet.MOON: [4],          # Cancer
    Planet.MARS: [1, 8],       # Aries, Scorpio
    Planet.MERCURY: [3, 6],    # Gemini, Virgo
    Planet.JUPITER: [9, 12],   # Sagittarius, Pisces
    Planet.VENUS: [2, 7],      # Taurus, Libra
    Planet.SATURN: [10, 11]    # Capricorn, Aquarius
}

# Swiss Ephemeris planet IDs
SWISS_EPHEM_IDS = {
    Planet.SUN: 0,
    Planet.MOON: 1,
    Planet.MARS: 4,
    Planet.MERCURY: 2,
    Planet.JUPITER: 5,
    Planet.VENUS: 3,
    Planet.SATURN: 6,
    Planet.RAHU: 7  # MEAN_NODE
} 