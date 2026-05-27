from yasbd.rules.base import Rules


# Don't remove the fmt guards as they keep compact set formatting
# fmt: off
class LangRules(Rules):
    """Template for adding new language rule modules.

    Copy this file and rename it to ``<lang>.py`` (e.g.
    ``fr.py``), rename the class to ``<Lang>Rules`` (e.g.
    ``FrRules``) and override only the sets your language needs
    (please, not all of them).
    """

    # Extra sentence terminators used by the language.
    TERMINATORS = Rules.TERMINATORS | {...}

    # Honorifics and professional abbreviations that should not split sentences.
    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {...}

    # Country and regional abbreviations written with periods (U.S., E.U., etc.).
    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {...}

    # Citation and reference abbreviations commonly used mid-text.
    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {...}

    # Street and address abbreviations (Ave., Blvd., Rd., etc.).
    STREET_ABBRVS = Rules.STREET_ABBRVS | {...}

    # Common inline abbreviations that should not end a sentence.
    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {...}

    # Names or titles containing "!" that should not trigger sentence breaks.
    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {...}

    # Month, weekday, and calendar abbreviations.
    DATE_ABBRVS = Rules.DATE_ABBRVS | {...}

    # Common nouns appearing inside organization or institution names.
    COMMON_ORG_NOUNS = {...}

    # Frequently occurring sentence starters used as weak boundary hints.
    COMMON_SENT_STARTERS = {...}

    # -- Mostly useful for unicase or weakly-cased languages --

    # Quotative particles used after speech, thoughts, or labels.
    QUOTATIVE_PARTICLES = {...}

    # Postpositional case markers that tightly bind an abbreviation to the clause
    # (Japanese の, Chinese 的, etc.).
    CASE_MARKERS = {...}

    # Verbs commonly used for dialogue attribution or reported speech.
    REPORTING_WORDS = {...}

# fmt: on
