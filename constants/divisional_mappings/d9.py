"""
D9 chart (Navamsa) mapping.
This mapping is based on classical Vedic astrology texts.
"""

D9_MAPPING = {
    # Aries
    1: {
        1: 1,  # Aries → Aries
        2: 2,  # Aries → Taurus
        3: 3,  # Aries → Gemini
        4: 4,  # Aries → Cancer
        5: 5,  # Aries → Leo
        6: 6,  # Aries → Virgo
        7: 7,  # Aries → Libra
        8: 8,  # Aries → Scorpio
        9: 9,  # Aries → Sagittarius
    },
    # Taurus
    2: {
        1: 10,  # Taurus → Capricorn
        2: 11,  # Taurus → Aquarius
        3: 12,  # Taurus → Pisces
        4: 1,   # Taurus → Aries
        5: 2,   # Taurus → Taurus
        6: 3,   # Taurus → Gemini
        7: 4,   # Taurus → Cancer
        8: 5,   # Taurus → Leo
        9: 6,   # Taurus → Virgo
    },
    # Gemini
    3: {
        1: 7,   # Gemini → Libra
        2: 8,   # Gemini → Scorpio
        3: 9,   # Gemini → Sagittarius
        4: 10,  # Gemini → Capricorn
        5: 11,  # Gemini → Aquarius
        6: 12,  # Gemini → Pisces
        7: 1,   # Gemini → Aries
        8: 2,   # Gemini → Taurus
        9: 3,   # Gemini → Gemini
    },
    # Cancer
    4: {
        1: 4,   # Cancer → Cancer
        2: 5,   # Cancer → Leo
        3: 6,   # Cancer → Virgo
        4: 7,   # Cancer → Libra
        5: 8,   # Cancer → Scorpio
        6: 9,   # Cancer → Sagittarius
        7: 10,  # Cancer → Capricorn
        8: 11,  # Cancer → Aquarius
        9: 12,  # Cancer → Pisces
    },
    # Leo
    5: {
        1: 1,   # Leo → Aries
        2: 2,   # Leo → Taurus
        3: 3,   # Leo → Gemini
        4: 4,   # Leo → Cancer
        5: 5,   # Leo → Leo
        6: 6,   # Leo → Virgo
        7: 7,   # Leo → Libra
        8: 8,   # Leo → Scorpio
        9: 9,   # Leo → Sagittarius
    },
    # Virgo
    6: {
        1: 10,  # Virgo → Capricorn
        2: 11,  # Virgo → Aquarius
        3: 12,  # Virgo → Pisces
        4: 1,   # Virgo → Aries
        5: 2,   # Virgo → Taurus
        6: 3,   # Virgo → Gemini
        7: 4,   # Virgo → Cancer
        8: 5,   # Virgo → Leo
        9: 6,   # Virgo → Virgo
    },
    # Libra
    7: {
        1: 7,   # Libra → Libra
        2: 8,   # Libra → Scorpio
        3: 9,   # Libra → Sagittarius
        4: 10,  # Libra → Capricorn
        5: 11,  # Libra → Aquarius
        6: 12,  # Libra → Pisces
        7: 1,   # Libra → Aries
        8: 2,   # Libra → Taurus
        9: 3,   # Libra → Gemini
    },
    # Scorpio
    8: {
        1: 4,   # Scorpio → Cancer
        2: 5,   # Scorpio → Leo
        3: 6,   # Scorpio → Virgo
        4: 7,   # Scorpio → Libra
        5: 8,   # Scorpio → Scorpio
        6: 9,   # Scorpio → Sagittarius
        7: 10,  # Scorpio → Capricorn
        8: 11,  # Scorpio → Aquarius
        9: 12,  # Scorpio → Pisces
    },
    # Sagittarius
    9: {
        1: 1,   # Sagittarius → Aries
        2: 2,   # Sagittarius → Taurus
        3: 3,   # Sagittarius → Gemini
        4: 4,   # Sagittarius → Cancer
        5: 5,   # Sagittarius → Leo
        6: 6,   # Sagittarius → Virgo
        7: 7,   # Sagittarius → Libra
        8: 8,   # Sagittarius → Scorpio
        9: 9,   # Sagittarius → Sagittarius
    },
    # Capricorn
    10: {
        1: 10,  # Capricorn → Capricorn
        2: 11,  # Capricorn → Aquarius
        3: 12,  # Capricorn → Pisces
        4: 1,   # Capricorn → Aries
        5: 2,   # Capricorn → Taurus
        6: 3,   # Capricorn → Gemini
        7: 4,   # Capricorn → Cancer
        8: 5,   # Capricorn → Leo
        9: 6,   # Capricorn → Virgo
    },
    # Aquarius
    11: {
        1: 7,   # Aquarius → Libra
        2: 8,   # Aquarius → Scorpio
        3: 9,   # Aquarius → Sagittarius
        4: 10,  # Aquarius → Capricorn
        5: 11,  # Aquarius → Aquarius
        6: 12,  # Aquarius → Pisces
        7: 1,   # Aquarius → Aries
        8: 2,   # Aquarius → Taurus
        9: 3,   # Aquarius → Gemini
    },
    # Pisces
    12: {
        1: 4,   # Pisces → Cancer
        2: 5,   # Pisces → Leo
        3: 6,   # Pisces → Virgo
        4: 7,   # Pisces → Libra
        5: 8,   # Pisces → Scorpio
        6: 9,   # Pisces → Sagittarius
        7: 10,  # Pisces → Capricorn
        8: 11,  # Pisces → Aquarius
        9: 12,  # Pisces → Pisces
    },
} 