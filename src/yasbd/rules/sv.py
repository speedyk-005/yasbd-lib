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
        "sammanst", "m.fl", "o.l", "osv", "o.s.v", "kl",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitel", "Avsnitt", "Bilaga", "Inledning", "Sammanfattning",
        "Slutsats", "Bakgrund", "Metod", "Resultat", "Diskussion",
        "Paragraf", "Tabell", "Figur",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "bl.a", "dvs", "d.v.s", "jf", "jvf", "pga", "ifm", "ca",
        "t.ex", "m.a.o", "fr.o.m", "t.o.m", "p.g.a", "inkl",
        "ekskl", "evt", "hhv",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "mån", "tis", "ons", "tors", "fre", "lör", "sön",
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
        "april", "augusti", "december", "februari", "januari",
        "juli", "juni", "maj", "mars", "november", "oktober",
        "september",

        # Swedish days
        "måndag", "tisdag", "onsdag", "torsdag", "fredag",
        "lördag", "söndag",
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Remove the German ordinal guard inherited from DeRules."""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST = [
            pattern
            for pattern in cls.MID_SENTENCE_FINDER_LST
            if pattern.pattern != r"\s\d{1,3}\."
        ]

# fmt: on
