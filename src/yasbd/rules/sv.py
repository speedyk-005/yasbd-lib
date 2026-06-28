from yasbd.rules.base import Rules
from yasbd.rules.de import DeRules


# fmt: off
class SvRules(DeRules):

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Swedish honorifics
        "hr", "h", "fru", "fr", "frk",

        # Academic and Professional
        "dr", "prof", "mag", "fil", "tekn", "med", "docent",
        "civil", "civ", "dipl", "ekon", "jur", "teol", "filosofie",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical and Document References
        "s", "anm", "ang", "bil", "fig", "kap", "tab", "avd",
        "uppl", "omg", "utg", "red", "sammanst", "hft", "förf",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitel", "Avsnitt", "Bilaga", "Inledning", "Sammanfattning",
        "Slutsats", "Bakgrund", "Metod", "Resultat", "Diskussion",
        "Paragraf", "Tabell", "Figur",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Common Swedish inline abbreviations
        "bl.a", "dvs", "m.m", "t.ex", "ev", "ca", "e.Kr", "f.Kr",
        "m.a.o", "m.fl", "s.a.s", "s.k", "o.s.v", "osv",
        "fr.o.m", "t.o.m", "inkl", "exkl", "jfr", "jämf",

        # Correspondence
        "ang", "ref", "p.m", "bif",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Swedish months
        "jan", "febr", "feb", "mars", "april", "maj", "juni", "juli",
        "aug", "sept", "sep", "okt", "nov", "dec",

        # Swedish days
        "mån", "tis", "ons", "tors", "fre", "lör", "sön",
    }

    COMMON_SENT_STARTERS = {
        # Common Swedish sentence starters
        "Det", "En", "Ett", "Den",
        "Jag", "Du", "Han", "Hon", "Vi", "Ni", "De", "Man",
        "Detta", "Denna", "Det här", "Det där",
        "Vem", "Vad", "Var", "När", "Hur", "Varför", "Vilken", "Vilket",
        "Men", "Och", "Eller", "Ty", "Så", "Då",
        "Därför", "Ändå", "Emellertid", "Dessutom", "Därmed", "Vidare",
        "Slutligen", "Först", "Sedan", "Därefter", "Tidigare", "Senare",
        "Idag", "Igår", "Imorgon", "Nu",
        "Ytterligare", "Annars", "Nämligen", "Faktiskt", "Självklart",
    }

    DATE_WORDS = {
        # Swedish months
        "januari", "februari", "mars", "april", "maj", "juni",
        "juli", "augusti", "september", "oktober", "november", "december",

        # Swedish days
        "måndag", "tisdag", "onsdag", "torsdag", "fredag",
        "lördag", "söndag",
     }

# fmt: on
