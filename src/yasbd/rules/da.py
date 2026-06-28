from yasbd.rules.base import Rules
from yasbd.rules.sv import SvRules


# fmt: off
class DaRules(SvRules):

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Danish honorifics
        "hr", "fru", "fr", "frk",

        # Academic and Professional
        "dr", "prof", "cand", "lic", "mag", "ph.d", "jur",
        "med", "teol", "fil", "scient", "polit", "pharm", "odont",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical and Document References
        "s", "fig", "tab", "kap", "bil", "anm", "red", "forf",
        "udg", "bd", "hft", "sp", "afd", "till", "p",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitel", "Afsnit", "Bilag", "Indledning", "Resumé",
        "Konklusion", "Metode", "Resultat", "Diskussion",
        "Paragraf", "Tabel", "Figur", "Stk",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Common Danish inline abbreviations
        "bl.a", "dvs", "d.v.s", "jf", "pga", "ifm", "ca",
        "f.eks", "m.m", "m.fl", "o.l", "osv", "o.s.v",
        "evt", "henh", "hhv", "inkl", "ekskl", "jvf",

        # Correspondence
        "ref", "p.m", "bif", "vedr",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Danish months
        "jan", "febr", "feb", "mar", "apr", "maj", "jun", "jul",
        "aug", "sept", "sep", "okt", "nov", "dec",

        # Danish days
        "man", "tir", "ons", "tor", "fre", "lør", "søn",
    }

    COMMON_SENT_STARTERS = {
        # Common Danish sentence starters
        "Det", "En", "Et", "Den",
        "Jeg", "Du", "Han", "Hun", "Vi", "I", "De", "Man",
        "Denne", "Dette", "Den her", "Det her",
        "Hvem", "Hvad", "Hvor", "Hvornår", "Hvordan", "Hvorfor",
        "Hvilken", "Hvilket", "Hvilke",
        "Men", "Og", "Eller", "For", "Så", "Da",
        "Derfor", "Alligevel", "Imidlertid", "Desuden", "Dermed",
        "Ydermere", "Endelig", "Først", "Siden", "Derefter", "Senere",
        "I dag", "I går", "I morgen", "Nu",
        "Yderligere", "Ellers", "Nemlig", "Faktisk", "Selvfølgelig",
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
