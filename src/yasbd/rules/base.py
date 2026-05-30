import re  # For simpler patterns

import regex as re2


def _build_abbr_pattern(options: set[str]) -> str:
    """Build a safe escaped regex alternation pattern.

    Returns a never-match pattern if no valid options exist.
    Ref: https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything?
    """
    cleaned = [
        re2.escape(opt.strip())
        for opt in sorted(options, key=len, reverse=True)
        if opt.strip()
    ]

    return "|".join(cleaned) if cleaned else r"(?!)"


# fmt: off
class Rules:
    TERMINATORS = {"。", "．", ".", "！", "!", "？", "?", "‼", "⁉", "⁈"}

    TITLE_ABBRVS = {
        # Standard Professional (Universal Latin roots)
        "dr", "drs", "prof", "hon", "rev", "supt", "insp",

        # Global Social (Overlap across English/Spanish/Portuguese/French)
        "mr", "mrs", "ms", "st",

        # Military (NATO/International Standardized Ranks)
        "adm", "brig", "capt", "cmdr", "col", "cpl", "gen", "lt", "maj", "sgt", "pvt",

        # Political/Administrative (Common in Western bureaucracy)
        "gov", "rep", "sen", "pres"
    }

    GEOPOLITICAL_ABBRVS = {
        # North Atlantic / Western Europe
        "u.s", "u.s.a", "u.k", "e.u",
        "ｕ．ｓ", "ｕ．ｓ．ａ", "ｕ．ｋ", "ｅ．ｕ",

        # Multilateral / Intergovernmental
        "u.n", "u.s.s.r",
        "ｕ．ｎ", "ｕ．ｓ．ｓ．ｒ",

        # Asia / Middle East
        "u.a.e", "p.r.c", "r.o.k",
        "ｕ．ａ．ｅ", "ｐ．ｒ．ｃ", "ｒ．ｏ．ｋ",
    }

    REFERENCE_ABBRVS = {
        # Publishing / Documents
        "et al", "app", "apps", "cf", "ext", "fig", "figs", "l", "ll",
        "n", "nn", "p", "pp", "pag", "pt", "pts", "ref", "refs", "tab",
        "tbl", "tbls", "v", "vol", "vols",

        # Section / Structure
        "ann", "art", "arts", "cap", "cl", "cls", "col", "cols", "para",
        "paras", "sec", "sect", "secs", "subsec",

        # Legal / Numbering
        "no", "nos", "n°", "reg", "regs",

        # Scientific / Math / Technical
        "approx", "eq", "eqn", "eqs", "est", "ex", "exs",

        # Academic
        "univ", "s",
    }

    DATE_ABBRVS = {
        # Months
        "jan", "feb", "mar", "apr", "jun", "jul", "sep",
        "sept", "oct", "nov", "dec", "déc",

        # Day
        "mon", "tue", "wed", "thu", "fri", "sat", "sun",
        "lun", "mar", "dom",
    }

    MID_SENTENCE_ABBRVS = {
        # Business entity bridges
        "assoc", "mfg",

        # Bridge/connectors
        "cf", "eg", "e.g", "ie", "i.e", "vs", "v", "viz", "ibid", "ca", "sc",

        # Street & directional anchors
        "mt", "dist",

        # General
        "approx", "est", "intl", "misc",
    }

    STREET_ABBRVS = {
        "ave", "blvd", "blv", "ct", "ln", "pl", "rd", "sq", "st", "wy", "way"
    }

    NAMES_WITH_EXCLAMATION = {
        # Tech, Corporate Entities, & Major Consumer Brands
        "Yahoo", "Yum", "Chips Ahoy", "Kahoot", "JOOP", "Walla",
        "I Can't Believe It's Not Butter", "Pop",

        # Gaming, Media, Animation, & Entertainment
        "Mamma Mia", "Jeopardy", "Oklahoma", "Oliver", "Shindig",
        "Hailey's On It", "Airplane", "Osu", "Ha", "VSPO",

        # Geopolitical Quirks / Municipalities
        "Westward Ho", "Saint-Louis-du-Ha", "Baie-des-Ha",

        # Public Figures, Politics, & Manufacturing Brands
        "Jeb", "Éxito", "Hey Man", "Basta", "Elliot S"
    }

    COMMON_ORG_NOUNS = set()
    COMMON_SENT_STARTERS = set()
    QUOTATIVE_PARTICLES = set()
    CASE_MARKERS = set()
    REPORTING_WORDS = set()

    # https://regex101.com/r/tI9Cmg/2
    VERTICAL_LIST_START_FINDER = re2.compile(r"(?<=^\s*(?:[\p{L}\p{N}]\.){1,3})(?=\s)")

    # https://regex101.com/r/JYdWZw/4
    QUOTE_AND_PAREN_FINDER = re2.compile(
        r"""
        (?:\p{Pi}|»|(?<=[\s:])(['""])).+?(?:\p{Pf}|«|\1)|  # Quoted text
        \p{Ps}.+?\p{Pe}  # Parenthesized text
        """,
        re2.X,
    )

    # https://regex101.com/r/0P9f2V/1
    TOC_LEADER_FINDER = re.compile(r"[^\W_][\s\.]{4,}\d")

    # https://regex101.com/r/ZOZlLb/2/substitution
    NEWLINE_INSIDE_SENTENCE_FINDER = re2.compile(r"(?<=[,:;)\w\s])\n(?=([a-z(]))")

    _REGEX_CACHED = False
    # fmt: on
    def __init__(self):
        """Initialize rule instance with lazy-compiled regex patterns.

        Patterns are compiled once per class and cached via ``_REGEX_CACHED``.
        Subclasses can override data constants (abbreviation sets, terminators, etc.)
        and the classmethod ``_compile_regex_dynamically`` will pick them up.
        """
        if not type(self).__dict__.get("_REGEX_CACHED", False):
            self._compile_regex_dynamically()
            type(self)._REGEX_CACHED = True

    @classmethod
    def _compile_regex_dynamically(cls):
        """Compile language-specific regex patterns."""
        terminators_pattern = "".join(cls.TERMINATORS)
        dots_pattern = r"[.．]"
        title_abbrvs_pattern = _build_abbr_pattern(cls.TITLE_ABBRVS)
        geopolitical_abbrvs_pattern = _build_abbr_pattern(cls.GEOPOLITICAL_ABBRVS)
        common_starters_pattern = _build_abbr_pattern(cls.COMMON_SENT_STARTERS)

        # https://regex101.com/r/qBSyU5/12
        # Handle flattened lists due to messy OCR.
        cls.HORIZONTAL_LIST_FINDER = re.compile(
            rf"""
            (?:   #  Must preceded by
                ^\s*|     # A string start
                [:{terminators_pattern}]\s+  # A terminator or double colon + space
            )
            (?:[•◦]\s+)?   # Optional bullet point (e.g., • 9.)
            (?:
                [-*+]|      #  Markdown style list
                (?:\d{{1,2}}[.)]{{1,2}}|[a-zA-Z]\))  #  Numbered and alphabetical list (e.g, a\), 34.\), 1.)
            )
            (?=\s)  # Must followed by a space
            """,
            re.X,
        )

        # https://regex101.com/r/VMzYsx/9
        cls.NAIVE_BOUNDARY_FINDER = re2.compile(
            rf"""
            # Split if left token is a unicase letter (Always)
            (?<=\p{{Lo}}\s*[{terminators_pattern}])|

            # Split after any terminators followed by a a newline,
            # common sentence starter, Space+Upper or unicase letter
            (?<=[{terminators_pattern}])
            (?=
                \s*\n|
                \s+(?:[^\p{{Ll}}]|
                \s+(?<!\.\.)(?i:{common_starters_pattern})\b)|
                \s*\p{{Lo}}
            )|

            # Split at transition between Latin letters separate by alien
            (?<=[\p{{LU}}\p{{Ll}}][​。！？।])(?=[\p{{Lu}}])|

            # Cluster of terminators (e.g hello!!! r u ok?)
            (?<=[{terminators_pattern.replace('.', '')}]{{2,}})(?=\s)
            """,
            re2.X,
        )

        # fmt: off
        # Faster than one big regex
        # https://regex101.com/r/svyCoU/18
        cls.MID_SENTENCE_FINDER_LST = [
            # https://regex101.com/r/cPh8sD/2
            # Three-dot ellipsis mid-thought (e.g., "... she didn't")
            # Only four dots (.... or . . . .) should be a sentence boundary.
            re.compile(r"(?<!\.)(?:\s?\.){3}"),

            # Title abbrv or initialisms (e.g., Dr. Paul)
            re.compile(rf"\b(?i:{title_abbrvs_pattern}){dots_pattern}"),

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            re.compile(rf"""
                \b(?i:{geopolitical_abbrvs_pattern}){dots_pattern}
                (?=
                    \s*(?:{_build_abbr_pattern(cls.CASE_MARKERS)})|
                    \s+(?:{_build_abbr_pattern(cls.COMMON_ORG_NOUNS)})
                )
                """, re.X
            ),

            # Abbrv that NEVER ends a sentence
            re.compile(
               rf"\b(?i:{_build_abbr_pattern(cls.MID_SENTENCE_ABBRVS)}){dots_pattern}"
            ),

            # References abbrv followed by a number, a letter or opened paren (e.g., to p. 55, app. A)
            re2.compile(rf"""
                \b(?i:{_build_abbr_pattern(cls.REFERENCE_ABBRVS)}){dots_pattern}
                (?=\s+(?:\(|\p{{Lu}}\b|\p{{N}}|[IVXLCDM]+))
                """, re2.X
            ),

            # Date abbrv followed by a number
            re2.compile(
                rf"\b(?i:{_build_abbr_pattern(cls.DATE_ABBRVS)}){dots_pattern}(?=\s+\p{{N}})"
            ),

            # Streets/Initialism/Acronyms/Exclamations words (e.g., Yahoo!, A.B. Holding, Ave. Central)
            # excluding geopolitical ones not followed by a common starters
            re2.compile(rf"""
                (?:\p{{Lu}}\.)(?<!(?i:{geopolitical_abbrvs_pattern}))
                (?!\s+(?:{common_starters_pattern})\b)
                """, re2.X
            ),
            re.compile(rf"""
                (?:
                    \b(?i:{_build_abbr_pattern(cls.STREET_ABBRVS)}){dots_pattern}|
                    (?i:{_build_abbr_pattern(cls.NAMES_WITH_EXCLAMATION)})[! ！‼]
                )
                (?!\s+(?:{common_starters_pattern})\b)
               """, re.X
            ),
        ]
        # fmt: on

        # https://regex101.com/r/EGkRU8/6
        cls.QUOTE_AND_PAREN_END_FINDER = re2.compile(
            rf"""
            (?<=
                [{terminators_pattern}]   # A terminator
                (?:'\s|["”]|\s*[»\p{{Pf}}\p{{Pe}}])     # Closing quotes/parens
            )
            (?!  # NOT followed by any continuation markers, punctuation, or space+lowercase
                \s*\p{{Po}}|
                {_build_abbr_pattern(cls.QUOTATIVE_PARTICLES | cls.REPORTING_WORDS)}|
                \s+[\p{{Ll}}]
            )
            """,
            re2.X,
        )

        # https://regex101.com/r/ffqwjh/2
        cls.CONTIGUOUS_TERMINATORS_FINDER = re.compile(rf"(?:\s*+[{terminators_pattern}]){{2,}}")

    def _remove_quote_and_paren_spans(
        self,
        main_boundaries: set[int],
        text: str,
        preserve_quote_and_paren: bool,
    ) -> None:
        """Remove boundaries inside quoted/parenthesised spans."""
        if preserve_quote_and_paren:
            # Ignore first pos to preserve splits before opening quote/paren,
            # especially for non-whitespace languages
            main_boundaries.difference_update(
                pos
                for m in self.QUOTE_AND_PAREN_FINDER.finditer(text)
                for pos in range(m.start() + 1, m.end())
            )

            main_boundaries.update(
                m.end() for m in self.QUOTE_AND_PAREN_END_FINDER.finditer(text)
            )

    def _remove_toc_spans(
        self, main_boundaries: set[int], text: str
    ) -> None:
        """Remove boundaries inside TOC leader runs."""
        if "..." in text:
            for m in self.TOC_LEADER_FINDER.finditer(text):
                main_boundaries.difference_update(range(*m.span()))

    def _adjust_list_boundaries(self, main_boundaries: set[int], text: str) -> None:
        """Remove and re-align boundaries around list markers."""
        horiz_matches = list(self.HORIZONTAL_LIST_FINDER.finditer(text))
        if len(horiz_matches) >= 2:
            main_boundaries.difference_update(m.end() for m in horiz_matches)
            # Shift boundaries the pointer back (1.\)| => |1.\), a. | => |a. ) to correctly
            # terminate the preceding sentence before flattened horizontal list.
            main_boundaries.update(m.start() + 1 for m in horiz_matches if m.start())

        main_boundaries.difference_update(
            m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(text)
        )

    def apply(
        self,
        text: str,
        preserve_quote_and_paren: bool,
    ) -> list[int]:
        """Detect sentence boundaries in *text*.

        Two-pass algorithm:
        1. Collect boundary candidates from punctuation positions.
        2. Remove false alarms (mid-sentence abbreviations, ellipsis,
           quote/paren spans, list markers).

        Args:
            text: A string to find sentence boundaries in.
            preserve_quote_and_paren: If ``True``, suppress boundaries
               inside quote and parenthesis spans.

        Returns:
            Sorted list of character offsets at which sentences end.
        """
        text = self.NEWLINE_INSIDE_SENTENCE_FINDER.sub(" ", text)
        main_boundaries = {
            m.end() for m in self.NAIVE_BOUNDARY_FINDER.finditer(text)
        }

        # -- Remove false alarms --
        main_boundaries.difference_update(
            m.end() for pat in self.MID_SENTENCE_FINDER_LST
            for m in pat.finditer(text)
        )
        self._remove_quote_and_paren_spans(
            main_boundaries, text, preserve_quote_and_paren
        )
        self._remove_toc_spans(main_boundaries, text)
        self._adjust_list_boundaries(main_boundaries, text)

        # Remove contiguous term pos except last one (e.g., Hello! !!   !! )
        main_boundaries.difference_update(
            *(
                range(m.start(), m.end() - 1)
                for m in self.CONTIGUOUS_TERMINATORS_FINDER.finditer(text)
            )
        )

        main_boundaries.update({0, len(text)})
        return sorted(main_boundaries)
