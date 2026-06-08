import re

from yasbd.rules.base import Rules, _build_abbr_pattern


# fmt: off
class DeRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "dr.h.c", "di", "dipl", "dipl.-Ing", "mag", "ba", "ma", "bsc", "msc",
        "h", "hr", "hnr", "hll", "frl", "min", "pfr", "ass", "​projektass",
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {
        "D.H", "E.V", "G.M.B.H", "I.G", "A.D", "K.U.K"
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical and Document References
        "abb", "anm", "bd", "bzw", "cap", "ed", "hrsg", "kap", "nr",
        "s", "sp", "std", "u.a", "u.ä", "vgl", "z.t", "f", "ff", "o.ä",
        "gl", "a.a.o", "s.o", "s.u", "s.a"

        # Legal and Formal References
        "abs", "art", "az", "lit", "m.w.n", "rspr",
    }

    HEADING_TOKENS = Rules.HEADING_TOKENS | {
        "Abschnitt", "Anhang", "Artikel", "Band", "Beispiel",
        "Einleitung", "Exposé", "Kapitel", "Paragraf", "Präambel",
        "Schlusswort", "Seite", "Teil", "Vorwort", "Zusammenfassung",
    }

    # Multi-part abbreviations with spaces (like "d. h.", "z. B.", "i. d. R.")
    # are removed from this literal set. They are caught dynamically later
    # in the pipeline by the cls.MID_SENTENCE_FINDER_LST regex rule.
    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {
       # Bridge / Logical connectors
       "bzw", "evtl", "ggf", "ggfs", "inkl", "lt", "sog",
       "zzgl", "bspw", "insb", "ca", "bsp",

        # Business/Commercial
        "fa", "tel", "fax",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "mär", "mai", "okt", "dez",

        # Days
        "mo", "di", "mi", "do", "fr", "sa", "so",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "Mach mit", "Jetzt neu"
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Der", "Die", "Das", "Ein", "Eine",

        # Pronouns
        "Ich", "Wir", "Du", "Ihr", "Er", "Sie", "Es", "Man",
        "Dieser", "Diese", "Dieses", "Jener", "Jene", "Jenes",

        # Question words
        "Wer", "Was", "Wo", "Wann", "Warum", "Wie", "Welcher", "Welche", "Welches",
        "Wessen", "Wem", "Wen",

        # Adverbs and Connectors
        "Allerdings", "Zudem", "Dennoch", "Deshalb", "Folglich", "Darum",
        "Mittlerweile", "Außerdem", "Darüberhinaus", "Ansonsten", "Jedoch",
        "Ebenso", "Somit", "Dann", "Denn",

        # Other starters
        "Tun", "Tat", "Millionen", "Gestern", "Heute", "Morgen",
    }

    STREET_ABBRVS = {
        "str", "gasse", "pl", "allee", "weg", "hbf", "platz",
        "ring", "ufer", "chaussee", "damm", "brücke", "geb"
    }
    MID_SENTENCE_ABBRVS |= STREET_ABBRVS

    DATE_WORDS = {
        # Months
        "januar", "februar", "märz", "april", "mai", "juni",
        "juli", "august", "september", "oktober", "november", "dezember",

        # Days
        "montag", "dienstag", "mittwoch", "donnerstag", "freitag",
        "samstag", "sonntag",
     }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis, ord num and time"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
            # Consecutive dots "..." or "...." still create sentence boundaries.
            re.compile(r"(?<!\.)\.(?:\s\.){2}"),

            # Ordinal numbers
            # https://learngerman.dw.com/en/ordinal-numbers/l-57731450/gr-60885529
            re.compile(r"\s\d+\."),

            # Multi-part abbreviations with spaces (like "d. h.", "z. B.", "i. d. R.")
            re.compile(r"\b[a-zA-Z]\.(?!\s+\w{2,})"),

            # Number/Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
            re.compile(rf"""
                (?:\d\.|(?:(?<=\d)|\b)(?i:[ap]\.m\.))
                (?=
                    \s+(?i:{_build_abbr_pattern(cls.DATE_ABBRVS | cls.DATE_WORDS)})
                    (?:\.|\s|$)
                )
            """, re.X),
        ])

        # Street abbrv followed by a common starters
        cls.ENDING_STREET_ABBRVS_FINDER = re.compile(rf"""
            (?:\b(?i:{_build_abbr_pattern(cls.STREET_ABBRVS)})\.)
            (?=\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
           """, re.X
        )

    def _post_process_boundaries(
        self, main_boundaries: set[int], text: str
    ) -> None:
        main_boundaries.update(
            m.end() for m in self.ENDING_STREET_ABBRVS_FINDER.finditer(text)
        )
# fmt: on
