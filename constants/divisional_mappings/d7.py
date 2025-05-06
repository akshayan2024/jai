"""
D7 chart (Saptamsa) mapping.
This mapping divides each sign into seven equal parts (of 4°17'8.6" each).
For odd signs, the seven divisions map to successive signs starting from the sign itself.
For even signs, the seven divisions map to successive signs starting from the seventh sign from itself.
"""

D7_MAPPING = {
    # Aries (odd sign)
    1: {
        1: 1,   # First division -> Aries
        2: 2,   # Second division -> Taurus
        3: 3,   # Third division -> Gemini
        4: 4,   # Fourth division -> Cancer
        5: 5,   # Fifth division -> Leo
        6: 6,   # Sixth division -> Virgo
        7: 7,   # Seventh division -> Libra
    },
    # Taurus (even sign)
    2: {
        1: 8,   # First division -> Scorpio
        2: 9,   # Second division -> Sagittarius
        3: 10,  # Third division -> Capricorn
        4: 11,  # Fourth division -> Aquarius
        5: 12,  # Fifth division -> Pisces
        6: 1,   # Sixth division -> Aries
        7: 2,   # Seventh division -> Taurus
    },
    # Gemini (odd sign)
    3: {
        1: 3,   # First division -> Gemini
        2: 4,   # Second division -> Cancer
        3: 5,   # Third division -> Leo
        4: 6,   # Fourth division -> Virgo
        5: 7,   # Fifth division -> Libra
        6: 8,   # Sixth division -> Scorpio
        7: 9,   # Seventh division -> Sagittarius
    },
    # Cancer (even sign)
    4: {
        1: 10,  # First division -> Capricorn
        2: 11,  # Second division -> Aquarius
        3: 12,  # Third division -> Pisces
        4: 1,   # Fourth division -> Aries
        5: 2,   # Fifth division -> Taurus
        6: 3,   # Sixth division -> Gemini
        7: 4,   # Seventh division -> Cancer
    },
    # Leo (odd sign)
    5: {
        1: 5,   # First division -> Leo
        2: 6,   # Second division -> Virgo
        3: 7,   # Third division -> Libra
        4: 8,   # Fourth division -> Scorpio
        5: 9,   # Fifth division -> Sagittarius
        6: 10,  # Sixth division -> Capricorn
        7: 11,  # Seventh division -> Aquarius
    },
    # Virgo (even sign)
    6: {
        1: 12,  # First division -> Pisces
        2: 1,   # Second division -> Aries
        3: 2,   # Third division -> Taurus
        4: 3,   # Fourth division -> Gemini
        5: 4,   # Fifth division -> Cancer
        6: 5,   # Sixth division -> Leo
        7: 6,   # Seventh division -> Virgo
    },
    # Libra (odd sign)
    7: {
        1: 7,   # First division -> Libra
        2: 8,   # Second division -> Scorpio
        3: 9,   # Third division -> Sagittarius
        4: 10,  # Fourth division -> Capricorn
        5: 11,  # Fifth division -> Aquarius
        6: 12,  # Sixth division -> Pisces
        7: 1,   # Seventh division -> Aries
    },
    # Scorpio (even sign)
    8: {
        1: 2,   # First division -> Taurus
        2: 3,   # Second division -> Gemini
        3: 4,   # Third division -> Cancer
        4: 5,   # Fourth division -> Leo
        5: 6,   # Fifth division -> Virgo
        6: 7,   # Sixth division -> Libra
        7: 8,   # Seventh division -> Scorpio
    },
    # Sagittarius (odd sign)
    9: {
        1: 9,   # First division -> Sagittarius
        2: 10,  # Second division -> Capricorn
        3: 11,  # Third division -> Aquarius
        4: 12,  # Fourth division -> Pisces
        5: 1,   # Fifth division -> Aries
        6: 2,   # Sixth division -> Taurus
        7: 3,   # Seventh division -> Gemini
    },
    # Capricorn (even sign)
    10: {
        1: 4,   # First division -> Cancer
        2: 5,   # Second division -> Leo
        3: 6,   # Third division -> Virgo
        4: 7,   # Fourth division -> Libra
        5: 8,   # Fifth division -> Scorpio
        6: 9,   # Sixth division -> Sagittarius
        7: 10,  # Seventh division -> Capricorn
    },
    # Aquarius (odd sign)
    11: {
        1: 11,  # First division -> Aquarius
        2: 12,  # Second division -> Pisces
        3: 1,   # Third division -> Aries
        4: 2,   # Fourth division -> Taurus
        5: 3,   # Fifth division -> Gemini
        6: 4,   # Sixth division -> Cancer
        7: 5,   # Seventh division -> Leo
    },
    # Pisces (even sign)
    12: {
        1: 6,   # First division -> Virgo
        2: 7,   # Second division -> Libra
        3: 8,   # Third division -> Scorpio
        4: 9,   # Fourth division -> Sagittarius
        5: 10,  # Fifth division -> Capricorn
        6: 11,  # Sixth division -> Aquarius
        7: 12,  # Seventh division -> Pisces
    },
} 