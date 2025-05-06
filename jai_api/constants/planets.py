"""
Planet definitions with 1-based indexing.
Swiss Ephemeris codes are based on the official Swiss Ephemeris documentation.
"""

PLANETS = {
    1: {"name": "Sun", "sanskrit": "Surya", "swe_code": 0},
    2: {"name": "Moon", "sanskrit": "Chandra", "swe_code": 1},
    3: {"name": "Mars", "sanskrit": "Mangala", "swe_code": 4},
    4: {"name": "Mercury", "sanskrit": "Budha", "swe_code": 2},
    5: {"name": "Jupiter", "sanskrit": "Guru", "swe_code": 5},
    6: {"name": "Venus", "sanskrit": "Shukra", "swe_code": 3},
    7: {"name": "Saturn", "sanskrit": "Shani", "swe_code": 6},
    8: {"name": "Rahu", "sanskrit": "Rahu", "swe_code": 10},  # North Lunar Node (Mean)
    9: {"name": "Ketu", "sanskrit": "Ketu", "swe_code": 11},  # South Lunar Node (calculated from Rahu + 180°)
}

# For easier lookup by planet name
PLANET_NAMES = {planet["name"]: idx for idx, planet in PLANETS.items()}

# For easier lookup by Swiss Ephemeris code
SWE_CODE_TO_PLANET = {planet["swe_code"]: idx for idx, planet in PLANETS.items()} 