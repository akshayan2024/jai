"""
D4 chart (Chaturthamsa) mapping.
This mapping divides each sign into four equal parts (of 7°30' each).
For movable signs (Aries, Cancer, Libra, Capricorn), the quarters map to the movable signs starting with itself.
For fixed signs (Taurus, Leo, Scorpio, Aquarius), the quarters map to the fixed signs starting with itself.
For dual signs (Gemini, Virgo, Sagittarius, Pisces), the quarters map to the dual signs starting with itself.
"""

D4_MAPPING = {
    # Aries (movable sign)
    1: {
        1: 1,   # First quarter -> Aries
        2: 4,   # Second quarter -> Cancer
        3: 7,   # Third quarter -> Libra
        4: 10,  # Fourth quarter -> Capricorn
    },
    # Taurus (fixed sign)
    2: {
        1: 2,   # First quarter -> Taurus
        2: 5,   # Second quarter -> Leo
        3: 8,   # Third quarter -> Scorpio
        4: 11,  # Fourth quarter -> Aquarius
    },
    # Gemini (dual sign)
    3: {
        1: 3,   # First quarter -> Gemini
        2: 6,   # Second quarter -> Virgo
        3: 9,   # Third quarter -> Sagittarius
        4: 12,  # Fourth quarter -> Pisces
    },
    # Cancer (movable sign)
    4: {
        1: 4,   # First quarter -> Cancer
        2: 7,   # Second quarter -> Libra
        3: 10,  # Third quarter -> Capricorn
        4: 1,   # Fourth quarter -> Aries
    },
    # Leo (fixed sign)
    5: {
        1: 5,   # First quarter -> Leo
        2: 8,   # Second quarter -> Scorpio
        3: 11,  # Third quarter -> Aquarius
        4: 2,   # Fourth quarter -> Taurus
    },
    # Virgo (dual sign)
    6: {
        1: 6,   # First quarter -> Virgo
        2: 9,   # Second quarter -> Sagittarius
        3: 12,  # Third quarter -> Pisces
        4: 3,   # Fourth quarter -> Gemini
    },
    # Libra (movable sign)
    7: {
        1: 7,   # First quarter -> Libra
        2: 10,  # Second quarter -> Capricorn
        3: 1,   # Third quarter -> Aries
        4: 4,   # Fourth quarter -> Cancer
    },
    # Scorpio (fixed sign)
    8: {
        1: 8,   # First quarter -> Scorpio
        2: 11,  # Second quarter -> Aquarius
        3: 2,   # Third quarter -> Taurus
        4: 5,   # Fourth quarter -> Leo
    },
    # Sagittarius (dual sign)
    9: {
        1: 9,   # First quarter -> Sagittarius
        2: 12,  # Second quarter -> Pisces
        3: 3,   # Third quarter -> Gemini
        4: 6,   # Fourth quarter -> Virgo
    },
    # Capricorn (movable sign)
    10: {
        1: 10,  # First quarter -> Capricorn
        2: 1,   # Second quarter -> Aries
        3: 4,   # Third quarter -> Cancer
        4: 7,   # Fourth quarter -> Libra
    },
    # Aquarius (fixed sign)
    11: {
        1: 11,  # First quarter -> Aquarius
        2: 2,   # Second quarter -> Taurus
        3: 5,   # Third quarter -> Leo
        4: 8,   # Fourth quarter -> Scorpio
    },
    # Pisces (dual sign)
    12: {
        1: 12,  # First quarter -> Pisces
        2: 3,   # Second quarter -> Gemini
        3: 6,   # Third quarter -> Virgo
        4: 9,   # Fourth quarter -> Sagittarius
    },
} 