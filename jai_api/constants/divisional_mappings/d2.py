"""
D2 chart (Hora) mapping.
This mapping divides each sign into two equal parts (of 15° each).
In D2, odd signs first half maps to Leo and second half to Cancer.
For even signs, first half maps to Cancer and second half to Leo.
"""

D2_MAPPING = {
    # Aries (odd sign)
    1: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Taurus (even sign)
    2: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
    # Gemini (odd sign)
    3: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Cancer (even sign)
    4: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
    # Leo (odd sign)
    5: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Virgo (even sign)
    6: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
    # Libra (odd sign)
    7: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Scorpio (even sign)
    8: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
    # Sagittarius (odd sign)
    9: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Capricorn (even sign)
    10: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
    # Aquarius (odd sign)
    11: {
        1: 5,  # First half -> Leo
        2: 4,  # Second half -> Cancer
    },
    # Pisces (even sign)
    12: {
        1: 4,  # First half -> Cancer
        2: 5,  # Second half -> Leo
    },
} 