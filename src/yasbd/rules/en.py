import re

from yasbd.rules.base import Rules, _build_abbr_pattern


# fmt: off
class EnRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "cong", "cpls", "ens", "sgts", "revs", "v.p", "del", "dep", "cllr",
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {
        "calif", "dc", "wash", "bc", "ont"
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Publishing / Documents
        "ch", "chs", "ed", "eds", "fn", "fns",

        # Legal / Numbering
        "r", "rr", "suppl", "supl",

        # Addresses
        "appt",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "The", "A", "An",

        # Pronouns
        "I", "We", "You", "He", "She", "It", "They", "This", "That",
        "These", "Those", "There",

        # Question words
        "Who", "What", "Where", "When", "Why", "How", "Which", "Whose", "Whom",

        # Adverbs
        "However", "Moreover", "Nevertheless", "Therefore", "Consequently",
        "Meanwhile", "Besides", "Furthermore", "Otherwise",

        # Other common starters
        "Do", "Did", "Millions",
    }

    STREET_ABBRVS = {
        "ave", "blvd", "blv", "ct", "ln", "pl", "rd", "sq", "st", "wy",
        "rte", "rt", "jct", "riv", "pen", "bldg", "expy", "hway", "hwy",
        "pkwy", "isl",
    }
    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | STREET_ABBRVS

    ORG_PROPER_NOUNS = {
        # Military institutions
        "Army", "Navy", "Air Force", "Pentagon",

        # Political / legislative institutions
        "Congress", "Senate", "House of Representatives", "Supreme Court",
        "Cabinet", "Parliament", "Commons",
    }

    DATE_WORDS = {
        # Months
        "january", "february", "march", "april", "june", "july",
        "august", "september", "october", "november", "december",
        # "May" is intentionally omitted because it is also a common modal verb.

        # Days
        "monday", "tuesday", "wednesday", "thursday", "friday",
        "saturday", "sunday",
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
            # Consecutive dots "..." or "...." still create sentence boundaries.
            re.compile(r"(?<!\.)\.(?:\s\.){2}"),

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            re.compile(rf"""
                \b(?i:{cls.GEOPOLITICAL_ABBRVS_PATTERN})\.
                (?=\s+(?:{_build_abbr_pattern(cls.ORG_PROPER_NOUNS)}))
                """, re.X
            ),

            # Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
            re.compile(rf"""
                (?:(?<=\d)|\b)(?i:[ap]\.m\.)
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
