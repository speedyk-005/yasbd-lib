import re

from yasbd.rules.base import Rules
from yasbd.utils.trie import build_optimized_pattern


# fmt: off
class EnRules(Rules):


    TITLE_ABBRVS = (Rules.TITLE_ABBRVS - {"min"}) | {
        "cong", "cpls", "ens", "sgts", "revs", "v.p", "del", "dep", "cllr",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
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

    SECTION_MARKERS = Rules.SECTION_MARKERS | {"Chapter", "Appendix",}

    COMMON_SENT_STARTERS = {
        # Articles
        "The", "A", "An",

        # Pronouns
        "He", "I", "It", "She", "That", "There", "These",
        "They", "This", "Those", "We", "You",

        # Question words
        "How", "What", "When", "Where", "Which", "Who", "Whom",
        "Whose", "Why",

        # Adverbs
        "Afterwards", "Besides", "Consequently", "Currently",
        "Finally", "First", "Formerly", "Furthermore",
        "However", "Initially", "Last", "Lastly", "Later",
        "Meanwhile", "Moreover", "Nevertheless", "Next",
        "Otherwise", "Second", "Subsequently", "Then",
        "Therefore", "Third",

        # Other common starters
        "Do", "Did", "Millions",
    }

    STREET_ABBRVS = {
        "ave", "bldg", "blv", "blvd", "ct", "expy", "hway",
        "hwy", "isl", "jct", "ln", "pen", "pkwy", "pl", "rd",
        "riv", "rt", "rte", "sq", "st", "wy",
    }
    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | STREET_ABBRVS

    ORG_PROPER_NOUNS = {
        # Military institutions
        "Army", "Navy", "Air Force", "Pentagon",

        # Political / legislative institutions
        "Cabinet", "Commons", "Congress",
        "House of Representatives", "Parliament", "Senate",
        "Supreme Court",
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
        """Override base regex compilation to handle ellipsis, geopolit and time"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
            # Consecutive dots "..." or "...." still create sentence boundaries.
            re.compile(r"(?<!\.)\.(?:\s\.){2}"),

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            re.compile(rf"""
                \b(?i:{cls.DOTTED_GEOPOL_ABBRVS_PATTERN})\.
                (?=\s+(?:{build_optimized_pattern(cls.ORG_PROPER_NOUNS)}))
                """, re.X
            ),

            # Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
            re.compile(rf"""
                (?:(?<=\d)|\b)(?i:[ap]\.m\.)
                (?=
                    \s+(?i:{build_optimized_pattern(cls.DATE_ABBRVS | cls.DATE_WORDS)})
                    (?:\.|\s|$)
                )
            """, re.X),
        ])

        # Street abbrv followed by a common starters
        cls.ENDING_STREET_ABBRVS_FINDER = re.compile(rf"""
            (?:\b(?i:{build_optimized_pattern(cls.STREET_ABBRVS)})\.)
            (?=\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
           """, re.X
        )

    # fmt: on
    def post_process_boundaries(
        self, sentence_boundaries: set[int], text: str
    ) -> None:
        sentence_boundaries.update(
            m.end() for m in self.ENDING_STREET_ABBRVS_FINDER.finditer(text)
        )
