from yasbd.rules.base import Rules

# fmt: off
class HyRules(Rules):
    """Sentence boundary detection rules for the Armenian language."""

    # Armenian sentence boundaries use the Armenian full stop (։),
    # exclamation mark (՜), and the Armenian colon/verjaket (:).
    TERMINATORS = {
        "։",
        "՜",
        ":",
    }

    TITLE_ABBRVS = set()
    DOTTED_GEOPOL_ABBRVS = set()
    REFERENCE_ABBRVS = set()
    SECTION_MARKERS = set()
    INLINE_ONLY_ABBRVS = set()
    NAMES_WITH_EXCLAMATION = set()
    DATE_ABBRVS = set()

    COMMON_SENT_STARTERS = {
        # Personal pronouns
        "Ես",
        "Դու",
        "Նա",
        "Մենք",
        "Դուք",
        "Նրանք",

        # Demonstrative pronouns
        "Սա",
        "Դա",
        "Սրանք",
        "Դրանք",

        # Question words
        "Ով",
        "Որտեղ",
        "Ինչ",
        "Ինչու",
        "Ինչպես",
        "Որը",
        "Երբ",
        "Քանի",
    }

    REPORTING_WORDS = {
        "ասաց",
        "հարցրեց",
        "պատասխանեց",
        "ավելացրեց",
        "բացատրեց",
        "նշեց",
        "հայտնեց",
        "պատմեց",
        "խնդրեց",
        "առաջարկեց",
        "շշնջաց",
        "գոռաց",
        "զգուշացրեց",
        "հրամայեց",
        "ծիծաղեց",
    }

# fmt: on
