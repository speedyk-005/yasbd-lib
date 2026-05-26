from yasbd.rules.base import Rules


# Don't remove the fmt guards as they keep compact set formatting
# fmt: off
class LangRules(Rules):
    """Template for adding new language rule modules.

    Copy this file and rename it to ``<lang>_rules.py`` (e.g.
    ``fr_rules.py``), rename the class to ``<Lang>Rules`` (e.g.
    ``FrRules``), set ``ISO_CODE`` to the two-letter language code,
    and override only the sets your language needs (please, not all of them).
    """

    ISO_CODE = "xx"

    # Sentence-ending punctuation specific to your language
    TERMINATORS = Rules.TERMINATORS | {...}

    # Honorifics & professional titles (Mr., Dr., Prof., etc.)
    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {...}

    # Country/region abbreviations (U.S., U.K., E.U., etc.)
    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {...}

    # Bibliographic / citation abbreviations (cf., fig., p., etc.)
    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {...}

    # Street/road suffixes (Ave., Blvd., Rd., etc.)
    STREET_ABBRVS = Rules.STREET_ABBRVS | {...}

    # Abbreviations that safely appear mid-sentence (vs., e.g., i.e., etc.)
    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {...}

    # Brands / titles containing "!" that should not trigger a split
    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {...}

    # Days abbreviations (Jan. Mon., etc..)
    DATE_ABBRVS = Rules.DATE_ABBRVS | {...}

    # Nouns that appear inside organisational names
    COMMON_ORG_NOUNS = {...}

    # Words that commonly start sentences (The, A, This, etc.)
    COMMON_SENT_STARTERS = {...}

    # -- Mostly for unicase languages --

    # Quotative particles (Japanese と, Korean 라고, etc.)
    QUOTATIVE_PARTICLES = {...}

    # Possessive markers that link nouns together (Japanese の, etc.)
    POSSESSIVE_PARTICLES = {...}

    # Reporting verbs for dialogue (Chinese 说/道/问, etc.)
    REPORTING_WORDS = {...}

# fmt: on
