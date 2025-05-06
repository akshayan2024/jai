"""
Constants related to yogas (planetary combinations) in Vedic astrology.
"""

from typing import Dict, List, Tuple, Any

# Yoga categories
YOGA_CATEGORIES = {
    "dhana_yoga": "Wealth yogas",
    "raja_yoga": "Power and authority yogas",
    "pancha_mahapurusha_yoga": "Five great person yogas",
    "nabhasa_yoga": "Sky yogas",
    "chandra_yoga": "Moon-based yogas",
    "arishta_yoga": "Malefic/difficulty yogas",
    "misc_yoga": "Miscellaneous yogas"
}

# Dictionary of yogas with descriptions and categories
YOGA_DESCRIPTIONS = {
    # --- Dhana Yogas (Wealth) ---
    "lakshmi_yoga": {
        "name": "Lakshmi Yoga",
        "description": "Formed when Venus is in own sign or exalted, and 9th lord is in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "dhana_yoga",
        "effect": "Brings wealth, prosperity, and material comforts."
    },
    "dhana_yoga": {
        "name": "Dhana Yoga",
        "description": "Formed when the lord of the 2nd house (house of wealth) is in a kendra or trikona (1st, 4th, 5th, 7th, 9th, or 10th house) and strong.",
        "category": "dhana_yoga",
        "effect": "Brings financial prosperity and wealth."
    },
    
    # --- Raja Yogas (Authority and Power) ---
    "gaja_kesari_yoga": {
        "name": "Gaja Kesari Yoga",
        "description": "Formed when Jupiter is in a kendra (1st, 4th, 7th, or 10th house) from the Moon.",
        "category": "raja_yoga",
        "effect": "Gives wisdom, leadership qualities, and success in endeavors."
    },
    "budha_aditya_yoga": {
        "name": "Budha-Aditya Yoga",
        "description": "Formed when Mercury and Sun are in the same house (except when Mercury is combusted).",
        "category": "raja_yoga",
        "effect": "Gives intelligence, wisdom, and political or administrative success."
    },
    "chandra_mangala_yoga": {
        "name": "Chandra-Mangala Yoga",
        "description": "Formed when Moon and Mars are in the same house or aspecting each other.",
        "category": "raja_yoga",
        "effect": "Gives courage, prosperity, and leadership."
    },
    
    # --- Pancha Mahapurusha Yogas (Five Great Person) ---
    "ruchaka_yoga": {
        "name": "Ruchaka Yoga",
        "description": "Formed when Mars is in its own sign or exalted and in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "pancha_mahapurusha_yoga",
        "effect": "Gives physical strength, leadership, and combative abilities."
    },
    "bhadra_yoga": {
        "name": "Bhadra Yoga",
        "description": "Formed when Mercury is in its own sign or exalted and in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "pancha_mahapurusha_yoga",
        "effect": "Gives intelligence, communication skills, and business acumen."
    },
    "hamsa_yoga": {
        "name": "Hamsa Yoga",
        "description": "Formed when Jupiter is in its own sign or exalted and in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "pancha_mahapurusha_yoga",
        "effect": "Gives wisdom, spirituality, and success in education."
    },
    "malavya_yoga": {
        "name": "Malavya Yoga",
        "description": "Formed when Venus is in its own sign or exalted and in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "pancha_mahapurusha_yoga",
        "effect": "Gives beauty, artistic talent, and sensual pleasures."
    },
    "sasa_yoga": {
        "name": "Sasa Yoga",
        "description": "Formed when Saturn is in its own sign or exalted and in a kendra (1st, 4th, 7th, or 10th house).",
        "category": "pancha_mahapurusha_yoga",
        "effect": "Gives discipline, longevity, and success through persistent effort."
    },
    
    # --- Nabhasa Yogas (Sky) ---
    "rajju_yoga": {
        "name": "Rajju Yoga",
        "description": "Formed when all planets are in signs of one element (fire, earth, air, or water).",
        "category": "nabhasa_yoga",
        "effect": "Gives stable career and methodical approach."
    },
    "musala_yoga": {
        "name": "Musala Yoga",
        "description": "Formed when all planets are in movable (cardinal) signs.",
        "category": "nabhasa_yoga",
        "effect": "Gives active, enterprising, and pioneering nature."
    },
    "nala_yoga": {
        "name": "Nala Yoga",
        "description": "Formed when all planets are in fixed signs.",
        "category": "nabhasa_yoga",
        "effect": "Gives determination, stability, and strong character."
    },
    "sarpa_yoga": {
        "name": "Sarpa Yoga (Snake Yoga)",
        "description": "Formed when all planets are in odd signs (1, 3, 5, 7, 9, 11).",
        "category": "nabhasa_yoga",
        "effect": "Gives sneaky and potentially manipulative tendencies."
    },
    
    # --- Chandra Yogas (Moon) ---
    "adhi_yoga": {
        "name": "Adhi Yoga",
        "description": "Formed when Mercury, Venus, and Jupiter are in 6th, 7th, and 8th houses from the Moon.",
        "category": "chandra_yoga",
        "effect": "Gives prosperity, good health, and positive mindset."
    },
    "sunapha_yoga": {
        "name": "Sunapha Yoga",
        "description": "Formed when a planet (other than the Sun) is in the 2nd house from the Moon.",
        "category": "chandra_yoga",
        "effect": "Gives financial prosperity and good social status."
    },
    "anapha_yoga": {
        "name": "Anapha Yoga",
        "description": "Formed when a planet (other than the Sun) is in the 12th house from the Moon.",
        "category": "chandra_yoga",
        "effect": "Gives success through one's own efforts and travels."
    },
    
    # --- Arishta Yogas (Malefic) ---
    "kemadruma_yoga": {
        "name": "Kemadruma Yoga",
        "description": "Formed when there are no planets in the 2nd and 12th houses from the Moon.",
        "category": "arishta_yoga",
        "effect": "May cause financial hardships and lack of support."
    },
    "shakata_yoga": {
        "name": "Shakata Yoga",
        "description": "Formed when Moon is in the 6th, 8th, or 12th house from Jupiter.",
        "category": "arishta_yoga",
        "effect": "May cause issues with luck, finances, and education."
    },
    
    # --- Miscellaneous Yogas ---
    "neecha_bhanga_raja_yoga": {
        "name": "Neecha Bhanga Raja Yoga",
        "description": "Formed when a planet in debilitation is aspected by its exaltation lord, or when the lord of the sign where a planet is debilitated is in a kendra from the Ascendant or Moon.",
        "category": "misc_yoga",
        "effect": "Cancels the negative effects of a debilitated planet and turns them into positive results."
    },
    "parivartana_yoga": {
        "name": "Parivartana Yoga (Mutual Exchange)",
        "description": "Formed when two planets exchange signs - each occupying the sign ruled by the other.",
        "category": "misc_yoga",
        "effect": "Creates a powerful connection that enhances the significations of both planets and houses."
    }
}

def get_yoga_description(yoga_name: str) -> Dict[str, Any]:
    """
    Get the description, category, and effects of a yoga.
    
    Args:
        yoga_name (str): Name of the yoga
        
    Returns:
        Dict[str, Any]: Yoga details
    """
    return YOGA_DESCRIPTIONS.get(yoga_name.lower(), {
        "name": yoga_name,
        "description": "No description available",
        "category": "unknown",
        "effect": "Unknown effect"
    })

def get_yogas_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """
    Get all yogas in a specific category.
    
    Args:
        category (str): Yoga category
        
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of yogas in the category
    """
    return {
        yoga_key: yoga_info
        for yoga_key, yoga_info in YOGA_DESCRIPTIONS.items()
        if yoga_info["category"] == category.lower()
    } 