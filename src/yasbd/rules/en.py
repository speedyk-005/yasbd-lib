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
    STREET_ABBRVS = Rules.STREET_ABBRVS | {
        "bldg", "expy", "hway", "hwy", "pkwy", "isl",
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

    ORG_PROPER_NOUNS = {
        # Military institutions
        "Army", "Navy", "Air Force", "Pentagon",

        # Political / legislative institutions
        "Congress", "Senate", "House of Representatives", "Supreme Court",
        "Cabinet", "Parliament", "Commons",
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            re.compile(rf"""
                \b(?i:{cls.GEOPOLITICAL_ABBRVS_PATTERN}){cls.DOTS_PATTERN}
                (?=\s+(?:{_build_abbr_pattern(cls.ORG_PROPER_NOUNS)}))
                """, re.X
            ),
        )

# fmt: on
