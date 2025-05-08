# Vedic Astrological Glossary

This glossary provides definitions of Vedic astrological terms used throughout the JAI API codebase. This resource is intended to help developers understand the domain-specific terminology.

## Core Concepts

### Ayanamsa
The angular difference between the Tropical zodiac (based on the equinoxes) and the Sidereal zodiac (based on fixed stars). This correction is applied to planetary positions to account for the precession of the equinoxes. Common systems include Lahiri, Raman, and Krishnamurti.

### Graha
Sanskrit term for "planet" or celestial body. In Vedic astrology, there are 9 main grahas: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu.

### House (Bhava)
One of 12 divisions of the chart representing different areas of life. In the Whole Sign system, each house corresponds to one complete zodiac sign.

### Julian Day
A continuous count of days since January 1, 4713 BCE. Used for astronomical calculations to simplify date arithmetic.

### Nakshatra
Lunar mansion or asterism. There are 27 nakshatras, each spanning 13°20' of the zodiac, and each ruled by a specific planet.

### Pada
Quarter or division of a nakshatra. Each nakshatra has 4 padas, each spanning 3°20'.

### Rashi
Sanskrit term for zodiac sign. There are 12 rashis in the zodiac, each spanning 30 degrees.

### Retrograde (Vakri)
Apparent backward motion of a planet as viewed from Earth. In Vedic astrology, retrograde planets have modified significations.

### Varga (Divisional Chart)
A specialized chart derived from the birth chart by dividing each sign into a specific number of parts. Common vargas include D1 (birth chart), D9 (navamsa), and D12 (dvadashamsa).

## Planets (Grahas)

### Sun (Surya)
Represents the soul, father, authority, and government. Rules the sign Leo.

### Moon (Chandra)
Represents the mind, mother, emotions, and public life. Rules the sign Cancer.

### Mars (Mangala)
Represents energy, courage, siblings, and property. Rules Aries and Scorpio.

### Mercury (Budha)
Represents intelligence, communication, and business. Rules Gemini and Virgo.

### Jupiter (Guru)
Represents wisdom, knowledge, children, and fortune. Rules Sagittarius and Pisces.

### Venus (Shukra)
Represents love, marriage, luxury, and vehicles. Rules Taurus and Libra.

### Saturn (Shani)
Represents discipline, limitations, service, and longevity. Rules Capricorn and Aquarius.

### Rahu (North Node)
The ascending lunar node. Represents obsession, foreign influences, and amplification.

### Ketu (South Node)
The descending lunar node. Represents isolation, spirituality, and loss. Always 180° opposite from Rahu.

## Divisional Charts (Vargas)

### D1 (Rashi Chart)
The birth chart, showing the basic personality and life circumstances.

### D2 (Hora Chart)
Indicates wealth and prosperity.

### D3 (Drekkana Chart)
Indicates siblings and courage.

### D4 (Chaturthamsha Chart)
Indicates property and fixed assets.

### D7 (Saptamsha Chart)
Indicates children and progeny.

### D9 (Navamsa Chart)
The most important divisional chart, indicating marriage, dharma, and deeper karmic patterns.

### D10 (Dashamsha Chart)
Indicates career and professional life.

### D12 (Dvadashamsha Chart)
Indicates parents and ancestry.

### D16 (Shodashamsha Chart)
Indicates vehicles and comforts.

### D20 (Vimshamsha Chart)
Indicates spiritual growth and religious inclinations.

### D24 (Chaturvimshamsha Chart)
Indicates education and learning.

### D27 (Nakshatramsha Chart)
Indicates overall strength and vitality.

### D30 (Trimshamsha Chart)
Indicates misfortunes and challenges.

### D60 (Shashtiamsha Chart)
The most detailed divisional chart, indicating overall life circumstances.

## Dasha System

### Vimshottari Dasha
The most commonly used dasha (planetary period) system in Vedic astrology. It has a 120-year cycle divided among the 9 planets based on the Moon's nakshatra at birth.

### Mahadasha
A major planetary period governed by one of the 9 planets, ranging from 6 to 20 years in length.

### Antardasha
A sub-period within a mahadasha, which is governed by another planet.

### Pratyantar Dasha
A sub-sub-period within an antardasha.

## Special Combinations

### Yoga
A planetary combination or configuration that produces specific effects. There are hundreds of different yogas in Vedic astrology.

### Conjunction
When two or more planets are in the same sign. In Vedic astrology, aspects are by sign rather than by exact degree.

### Aspect (Drishti)
The influence of a planet on another planet or house. In Vedic astrology, all planets aspect the 7th sign from their position, and Mars, Jupiter, and Saturn have additional special aspects.

## Strength Calculations

### Shadbala
Six-fold strength measurement of planets, including positional, directional, and temporal factors.

### Digbala
Directional strength of a planet based on its placement in the chart.

### Vargottama
A planet in the same sign in both the birth chart (D1) and the navamsa chart (D9), giving it extra strength.

## Technical Terms

### 1-based Indexing
In the JAI API, signs, houses, nakshatras, and planets are indexed starting from 1, not 0, to align with traditional astrological notation.

### Whole Sign House System
A house system where each house corresponds to exactly one zodiac sign, with the 1st house being the sign of the ascendant.

### Sign Lordship
Each planet rules (is the lord of) one or two zodiac signs. The lord of a house is the planet that rules the sign occupying that house. 