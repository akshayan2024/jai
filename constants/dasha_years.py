"""
Vimshottari Mahadasha periods in years.
Using 1-based planet indexing.
"""

DASHA_YEARS = {
    1: 6,   # Sun - 6 years
    2: 10,  # Moon - 10 years
    3: 7,   # Mars - 7 years
    4: 17,  # Mercury - 17 years
    5: 16,  # Jupiter - 16 years
    6: 20,  # Venus - 20 years
    7: 19,  # Saturn - 19 years
    8: 18,  # Rahu - 18 years
    9: 7    # Ketu - 7 years
}

# Total Vimshottari cycle is 120 years
TOTAL_DASHA_YEARS = sum(DASHA_YEARS.values())

# Nakshatra lord sequence for Vimshottari dasha
NAKSHATRA_LORDS = {
    1: 8,   # Ashwini - Ketu
    2: 6,   # Bharani - Venus
    3: 1,   # Krittika - Sun
    4: 2,   # Rohini - Moon
    5: 3,   # Mrigashira - Mars
    6: 8,   # Ardra - Rahu
    7: 5,   # Punarvasu - Jupiter
    8: 7,   # Pushya - Saturn
    9: 4,   # Ashlesha - Mercury
    10: 9,  # Magha - Ketu
    11: 6,  # Purva Phalguni - Venus
    12: 1,  # Uttara Phalguni - Sun
    13: 2,  # Hasta - Moon
    14: 3,  # Chitra - Mars
    15: 8,  # Swati - Rahu
    16: 5,  # Vishakha - Jupiter
    17: 7,  # Anuradha - Saturn
    18: 4,  # Jyeshtha - Mercury
    19: 9,  # Mula - Ketu
    20: 6,  # Purva Ashadha - Venus
    21: 1,  # Uttara Ashadha - Sun
    22: 2,  # Shravana - Moon
    23: 3,  # Dhanishta - Mars
    24: 8,  # Shatabhisha - Rahu
    25: 5,  # Purva Bhadrapada - Jupiter
    26: 7,  # Uttara Bhadrapada - Saturn
    27: 4,  # Revati - Mercury
} 