"""
D3 chart (Drekkana) mapping.
This mapping divides each sign into three equal parts (of 10° each).
For the first drekkana (0-10°), it's mapped to the sign itself.
For the second drekkana (10-20°), it's mapped to the 5th sign from it (same element).
For the third drekkana (20-30°), it's mapped to the 9th sign from it (same element).
"""

D3_MAPPING = {
    # Aries
    1: {
        1: 1,   # First drekkana -> Aries
        2: 5,   # Second drekkana -> Leo
        3: 9,   # Third drekkana -> Sagittarius
    },
    # Taurus
    2: {
        1: 2,   # First drekkana -> Taurus
        2: 6,   # Second drekkana -> Virgo
        3: 10,  # Third drekkana -> Capricorn
    },
    # Gemini
    3: {
        1: 3,   # First drekkana -> Gemini
        2: 7,   # Second drekkana -> Libra
        3: 11,  # Third drekkana -> Aquarius
    },
    # Cancer
    4: {
        1: 4,   # First drekkana -> Cancer
        2: 8,   # Second drekkana -> Scorpio
        3: 12,  # Third drekkana -> Pisces
    },
    # Leo
    5: {
        1: 5,   # First drekkana -> Leo
        2: 9,   # Second drekkana -> Sagittarius
        3: 1,   # Third drekkana -> Aries
    },
    # Virgo
    6: {
        1: 6,   # First drekkana -> Virgo
        2: 10,  # Second drekkana -> Capricorn
        3: 2,   # Third drekkana -> Taurus
    },
    # Libra
    7: {
        1: 7,   # First drekkana -> Libra
        2: 11,  # Second drekkana -> Aquarius
        3: 3,   # Third drekkana -> Gemini
    },
    # Scorpio
    8: {
        1: 8,   # First drekkana -> Scorpio
        2: 12,  # Second drekkana -> Pisces
        3: 4,   # Third drekkana -> Cancer
    },
    # Sagittarius
    9: {
        1: 9,   # First drekkana -> Sagittarius
        2: 1,   # Second drekkana -> Aries
        3: 5,   # Third drekkana -> Leo
    },
    # Capricorn
    10: {
        1: 10,  # First drekkana -> Capricorn
        2: 2,   # Second drekkana -> Taurus
        3: 6,   # Third drekkana -> Virgo
    },
    # Aquarius
    11: {
        1: 11,  # First drekkana -> Aquarius
        2: 3,   # Second drekkana -> Gemini
        3: 7,   # Third drekkana -> Libra
    },
    # Pisces
    12: {
        1: 12,  # First drekkana -> Pisces
        2: 4,   # Second drekkana -> Cancer
        3: 8,   # Third drekkana -> Scorpio
    },
} 