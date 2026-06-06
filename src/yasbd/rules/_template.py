from yasbd.rules.base import Rules


# Don't remove the fmt guards as they keep compact set formatting
# fmt: off
class LangRules(Rules):
    """Template for adding new language rule modules.

    Copy this file and rename it to ``<lang>.py`` (e.g.
    ``fr.py``), rename the class to ``<Lang>Rules`` (e.g.
    ``FrRules``) and override only the sets your language needs,
    (please, not all of them). Then remove the others.
    """

    # Extra sentence terminators used by the language.
    TERMINATORS = Rules.TERMINATORS | {...}

    # Honorifics and professional abbreviations that should not split sentences.
    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {...}

    # Country and regional abbreviations written with periods (U.S., E.U., etc.).
    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {...}

    # Citation and reference abbreviations commonly used mid-text.
    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {...}

    # Structural headings (e.g., Section, Chapter, etc.).
    # Not too useful for CJKV languages style
    HEADING_TOKENS = Rules.HEADING_TOKENS | {...}

    # Common inline abbreviations that should not end a sentence (e.g., Blvd., etc.).
    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {...}

    # Names or titles containing "!" that should not trigger sentence breaks.
    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {...}

    # Month, weekday, and calendar abbreviations.
    DATE_ABBRVS = Rules.DATE_ABBRVS | {...}

    # Frequently occurring sentence starters used as weak boundary hints.
    # Not too useful for languages without spaces
    COMMON_SENT_STARTERS = {...}

    # -- Mostly useful for unicase or weakly-cased languages --

    # Quotative particles used after speech, thoughts, or labels.
    QUOTATIVE_PARTICLES = {...}

    # Verbs commonly used for dialogue attribution or reported speech.
    REPORTING_WORDS = {...}

    def _post_process_boundaries(
        self, main_boundaries: set[int], text: str
    ) -> None:
        """Hook for language-specific boundary filtering that the regex
        passes cannot catch. Override and mutate ``main_boundaries``.
        """
        pass
# fmt: on
