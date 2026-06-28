from yasbd.rules.base import Rules
from yasbd.rules.sv import SvRules


# fmt: off
class DaRules(SvRules):


    # Specific academic/professional extensions
    TITLE_ABBRVS = SvRules.TITLE_ABBRVS | {
        "cand", "lic", "scient", "polit", "odont",
    }

    REFERENCE_ABBRVS = SvRules.REFERENCE_ABBRVS | {
        "forf", "anm", "afd", "sp"
    }

    SECTION_MARKERS = SvRules.SECTION_MARKERS | {
        "Afsnit", "Bilag", "Indledning", "Resumé",
        "Konklusion", "Metode", "Tabel", "Stk",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "febr", "maj", "man", "tir", "ons", "tor",
        "fre", "lør", "søn",
    }

    INLINE_ONLY_ABBRVS = SvRules.INLINE_ONLY_ABBRVS | {
        "f.eks", "vedr",
    }

    COMMON_SENT_STARTERS = SvRules.COMMON_SENT_STARTERS | {
        # Connectors (sentence-initial discourse markers)
        "Dog", "Alligevel", "Samtidig",
        "Endvidere", "Imidlertid", "Faktisk",

        # Interrogatives (Lexical split)
        "Hvad", "Hvem", "Hvor", "Hvornår", "Hvordan",
        "Hvorfor", "Hvilken", "Hvilket", "Hvilke",

        # Others
         "Et", "Ydermere", "Dermed", "Ellers",
    }

    DATE_WORDS = {
        # Danish months
        "januar", "februar", "marts", "april", "maj", "juni",
        "juli", "august", "september", "oktober", "november", "december",

        # Danish days
        "mandag", "tirsdag", "onsdag", "torsdag", "fredag",
        "lørdag", "søndag",
     }

# fmt: on
