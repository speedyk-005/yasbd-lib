import re

from yasbd.rules.base import Rules, _build_abbr_pattern


# fmt: off
class NlRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic and Professional Titles
        "dr", "drs", "prof", "mr", "ir", "ing", "lic", "bc",

        # Bachelor / Master Degrees
        "ba", "ma", "bsc", "msc",

        # Social Honorifics and Clergy
        "dhr", "mevr", "mw", "ds",

        # Military Ranks
        "gen", "lt-gen", "maj-gen", "briga", "kol", "lt-kol", "maj",
        "kapt", "lt", "elnt", "tlnt", "serg", "korp",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "A.U", "E.G", "V.S", "N.V", "B.V", "V.K",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical, Page, and Document References
        "art", "afb", "hfdst", "blz", "nr",  "par", "reg",
        "bijl", "ca", "cf", "ed", "vert", "id",

        # Legal, Corporate, and Formal Citation Markers
        "b.w", "stb", "gem", "coll", "hr", "c.q", "ov", "vp",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Afdeling", "Artikel", "Lid", "Paragraaf", "Bijlage",
        "Hoofdstuk", "Deel", "Inleiding", "Voorwoord",
        "Samenvatting", "Conclusie", "Register",
    }

    # Multi-part lowercase spaced/dotted abbreviations like "e. g." or "i. e."
    # are caught dynamically later by the cls.MID_SENTENCE_FINDER_LST regex rule.
    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
       # Bridge / Logical connectors
       "ebd", "dwz", "bijv", "evtl", "incl", "excl", "zgn", "ca",

        # Business/Commercial
        "tel", "fax", "attn",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "jan", "feb", "mrt", "apr", "jun", "jul",
        "aug", "sep", "okt", "nov", "dec",

        # Days
        "ma", "di", "wo", "do", "vr", "za", "zo",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "Nu", "Doe mee", "Tikkie", "Vergeet je tandenborstel niet"
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "De", "Het", "Een",

        # Pronouns
        "Ik", "We", "Wij", "Je", "Jij", "U", "Jullie", "Hij", "Zij", "Ze",
        "Men", "Die", "Deze", "Dit", "Dat", "Gene", "Er",

        # Question words
        "Wie", "Wat", "Waar", "Wanneer", "Waarom", "Hoe", "Welke", "Welk",
        "Wiens", "Wier",

        # Adverbs and Connectors
        "Echter", "Bovendien", "Desondanks", "Daarom", "Daardoor", "Dus",
        "Desalniettemin", "Niettemin", "Intussen", "Inmiddels", "Tevens",
        "Verder", "Tenslotte", "Uiteindelijk", "Vervolgens", "Voorlopig",
        "Overigens", "Trouwens", "Anderzijds", "Enerzijds", "Immers",
        "Namelijk", "Kortom", "Aldus", "Zodoende", "Bijgevolg", "Daarnaast",
        "Daarentegen", "Toch", "Hoewel", "Ondertussen",

        # Time / Sequence Anchors
        "Later", "Vroeger", "Daarna", "Vandaag", "Gisteren", "Morgen",
        "Eerst", "Toen", "Nu", "Soms", "Vaak", "Altijd", "Nooit",

        # Common Noun Starters
        "Mensen", "Miljoen",
    }

    STREET_ABBRVS = {
        "str", "st", "ln", "pl", "rd", "wgh", "plts", "hbf", "geb"
    }
    INLINE_ONLY_ABBRVS |= STREET_ABBRVS

    DATE_WORDS = {
        # Months
        "januari", "februari", "maart", "april", "mei", "juni",
        "juli", "augustus", "september", "oktober", "november", "december",

        # Days
        "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag",
        "zaterdag", "zondag",
     }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis, ord num and time"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
            # Consecutive dots "..." or "...." still create sentence boundaries.
            re.compile(r"(?<!\.)\.(?:\s\.){2}"),

            # Ordinal numbers
            # https://learngerman.dw.com/en/ordinal-numbers/l-57731450/gr-60885529
            re.compile(r"\s\d{1,3}\."),

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
