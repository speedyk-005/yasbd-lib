from yasbd.rules.base import Rules


# Don't remove the fmt guards as they keep compact set formatting
# fmt: off
class LangRules(Rules):
    """Template for adding new language rule modules.

    Copy this file and rename it to ``<lang>.py`` (e.g.
    ``fr.py``), rename the class to ``<Lang>Rules`` (e.g.
    ``FrRules``) and override only the sets your language needs,
    (please, not all of them). Then remove the others.

    Important:
        The class name must end with ``"Rules"``.
        The language code is derived by removing the suffix
        and lowercasing: ``FrRules`` => ``"fr"``.
        Use the ISO 639-1 two-letter code whenever
        a standard code exists. This is the value you pass to
        ``BoundaryDetector(lang="...")``.
    """

    # Extra sentence terminators used by the language.
    TERMINATORS = Rules.TERMINATORS | {...}

    # Honorifics and professional abbreviations that should not split sentences.
    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {...}

    # Country and regional abbreviations written with periods (U.S., E.U., etc.).
    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {...}

    # Citation and reference abbreviations commonly used mid-text.
    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {...}

    # Structural headings (e.g., Section, Chapter, etc.).
    # Not too useful for CJK languages style
    SECTION_MARKERS = Rules.SECTION_MARKERS | {...}

    # Common inline abbreviations that should not end a sentence (e.g., Blvd., etc.).
    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {...}

    # Names or titles containing "!" that should not trigger sentence breaks.
    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {...}

    # Month, weekday, and calendar abbreviations.
    DATE_ABBRVS = Rules.DATE_ABBRVS | {...}

    # Frequently occurring sentence starters used as weak boundary hints.
    # Not too useful for languages without spaces
    COMMON_SENT_STARTERS = {...}

    # -- Mostly useful for unicase or weakly-cased languages --

    # Quotative particles used after speech, thoughts, or labels.
    POST_QUOTATIVE_PARTICLES = {...}

    # Verbs commonly used for dialogue attribution or reported speech.
    REPORTING_WORDS = {...}

    # fmt: on
    def _post_process_boundaries(
        self, main_boundaries: set[int], text: str
    ) -> None:
        """Hook for language-specific boundary filtering that the regex
        passes cannot catch. Override and mutate ``main_boundaries``.
        """
        pass
