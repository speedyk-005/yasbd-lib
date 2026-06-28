from yasbd.rules.base import Rules
from yasbd.rules.de import DeRules


# fmt: off
class SvRules(DeRules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social
        "doc", "h", "hr", "fr", "frk",

        # Academic and Professional
        "mag", "fil", "tekn", "med", "civ",
        "dipl", "ekon", "jur", "teol",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "s", "sid", "anm", "ang", "bil", "kap", "forts",
        "förf", "avd", "uppl", "utg", "red",  "hft",
        "sammanst",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitel", "Avsnitt", "Bilaga", "Inledning", "Sammanfattning",
        "Slutsats", "Bakgrund", "Metod", "Resultat", "Diskussion",
        "Paragraf", "Tabell", "Figur",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "bl.a", "dvs", "d.v.s", "jf", "jvf", "pga", "ifm", "ca",
        "t.ex", "m.m", "m.fl", "o.l", "osv", "o.s.v", "m.a.o",
        "fr.o.m", "t.o.m", "p.g.a", "inkl", "ekskl", "evt",
        "hhv", "kl",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "mån", "tis", "ons",
        "tors", "fre", "lör", "sön",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Det", "En", "Ett", "Den",

        # Pronouns
        "Jag", "Du", "Han", "Hon", "Vi", "Ni", "De", "Man",
        "Detta", "Denna", "Det här", "Det där",

        # Question words
        "Vem", "Vad", "Var", "När", "Hur", "Varför",
        "Vilken", "Vilket",

        # Adverbs and Connectors
        "Men", "Och", "Eller", "Ty", "Så", "Då",
        "Därför", "Ändå", "Emellertid", "Dessutom",
        "Därmed", "Vidare", "Slutligen", "Först",
        "Sedan", "Därefter", "Tidigare", "Senare",
        "Idag", "Igår", "Imorgon", "Nu", "Ytterligare",
        "Annars", "Nämligen", "Faktiskt", "Självklart",
    }

    STREET_ABBRVS = {"str", "st", "pl", "g", "v"}
    INLINE_ONLY_ABBRVS |= STREET_ABBRVS

    DATE_WORDS = {
        # Swedish months
        "januari", "februari", "mars", "april", "maj", "juni",
        "juli", "augusti", "september", "oktober", "november", "december",

        # Swedish days
        "måndag", "tisdag", "onsdag", "torsdag", "fredag",
        "lördag", "söndag",
     }

# fmt: on
