"""
Dictionary file containing coding schemes for survey variables.
This makes it easier to recode variables consistently across different scripts.
"""

# Gender coding
GENDER_DICT = {
    0: 'Female',
    1: 'Male', 
    2: 'Divers', 
    3: 'Prefer not to say/Don\'t know'
}

# Education coding
EDUCATION_DICT = {
    0: 'Noch in der Schule',
    1: 'Schule beendet ohne Abschluss',
    2: 'Volks- oder Hauptschulabschluss',
    3: 'Realschulabschluss/Mittlere Reife/Polytechnische Oberschule',
    4: 'Abgeschlossene Lehre',
    5: 'Fachhochschulreife',
    6: 'Abitur/Hochschulreife',
    7: 'Hochschulabschluss: Bachelor',
    8: 'Hochschulabschluss: Master/Magister/Diplom/Staatsexamen',
    9: 'Hochschulabschluss: Promotion/Habilitation',
    10: 'Keine Angabe/weiß nicht'
}

# Location (German states) coding
LOCATION_DICT = {
    0: 'Baden-Württemberg',
    1: 'Bayern',
    2: 'Berlin',
    3: 'Brandenburg',
    4: 'Bremen',
    5: 'Hamburg',
    6: 'Hessen',
    7: 'Mecklenburg-Vorpommern',
    8: 'Niedersachsen',
    9: 'Nordrhein-Westfalen',
    10: 'Rheinland-Pfalz',
    11: 'Saarland',
    12: 'Sachsen',
    13: 'Sachsen-Anhalt',
    14: 'Schleswig-Holstein',
    15: 'Thüringen',
    16: 'Ich lebe nicht in Deutschland'
}

# Party voting coding (for both first and second votes)
PARTY_DICT = {
    0: 'SPD',
    1: 'CDU/CSU',
    2: 'Bündnis 90/Die Grünen',
    3: 'FDP',
    4: 'AfD',
    5: 'Die Linke',
    6: 'BSW',
    7: 'Andere Partei',
    8: 'Ungültig',
    9: 'Keine Angabe',
    10: 'Nicht wahlberechtigt',
    11: 'Nicht wählen'
}
