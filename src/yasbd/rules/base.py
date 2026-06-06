import re  # For simpler patterns

import regex as re2
from retrie.trie import Trie


def _build_abbr_pattern(options: set[str]) -> str:
    """Build an optimised and escaped regex alternation pattern.

    Returns a never-match pattern if no valid options exist.
    Ref: https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything?
    """
    if not options:
        return r"(?!)"

    trie = Trie()
    return trie.add(*options).pattern()


class Rules:
    TERMINATORS = {"。", "．", ".", "！", "!", "？", "?", "‼", "⁉", "⁈"}

    TITLE_ABBRVS = {
        # Standard Professional (Universal Latin roots)
        "dr", "dir", "drs", "prof", "hon", "ing", "rev", "supt", "insp", "spec",

        # Global Social
        "mr", "mrs", "ms", "mme", "messrs", "mlle", "mmes", "mssrs",
        "mmes", "mssrs", "st", "fr", "br"

        # Military (NATO/International Standardized Ranks)
        "adm", "brig", "capt", "cmdr",  "comdr", "commr",  "col", "cpl", "gen", "lt",
        "maj", "sgt", "pvt",

        # Political/Administrative (Common in Western bureaucracy)
        "gov", "rep", "sen", "pres", "sec", "min", "mgr", "asst", "det", "surg",
        "msgr", "amb",
    }

    GEOPOLITICAL_ABBRVS = {
        # North Atlantic / Western Europe
        "U.S", "U.S.A", "U.K", "E.U",

        # Multilateral / Intergovernmental
        "U.N", "U.S.S.R",

        # Asia / Middle East
        "U.A.E", "P.R.C", "R.O.K",
    }

    REFERENCE_ABBRVS = {
        # Publishing / Documents / Manuscripts
        "app", "apps", "cf", "cod", "diag", "ext", "fig", "figs",
        "fol", "illus", "l", "ll", "ms", "mss", "p", "pp", "pag",
        "pt", "pts", "ref", "refs", "tab", "tbl", "tbls", "v", "vol",
        "vols",

        # Section / Structure
        "ann", "art", "arts", "cap", "cl", "cls", "col",
        "cols", "para", "paras", "quaest", "sec", "sect",
        "secs", "subsec",

        # Legal / Numbering / Cross References
        "a.c", "a.d", "a.u.c", "b.c", "lc", "n", "nn",
        "no", "nos", "n°", "n.º", "qv", "reg", "regs",

        # Scientific / Technical
        "approx", "deg", "diam", "eq", "eqn", "eqs",
        "est", "ex", "exs", "lat", "long", "max", "min",

        # Commerce / Measurements
        "alt", "fam", "ord", "qty", "std", "wt",

        # Academic
        "et al", "s", "univ",
    }

    HEADING_TOKENS = {
        "Part", "Parte", "Section", "Subsection", "Article",
        "Module", "Division", "Usage", "Unit", "Volume",
        "Preface",  "Introduction",
    }

    DATE_ABBRVS = {
        # Months
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
        "sept", "oct", "nov", "dec", "déc",

        # Day
        "mon", "tue", "wed", "thu", "thurs", "thur", "fri",
        "sat", "sun", "lun", "mar", "dom",
    }

    MID_SENTENCE_ABBRVS = {
        # Business entity bridges
        "assoc", "mfg",

        # Bridge/connectors
        "cf", "eg", "e.g", "ie", "i.e", "i.q", "i.c", "a.k.a", "vs", "v", "viz",
        "ibid", "ca", "sc",

        # Notes & postscript markers
        "n.b", "p.s", "p.p.s", "sci", "scill", "s.vloc",

        # Others
        "approx", "est", "intl", "misc", "mt", "dist",

        # Streets
        "ave", "blvd", "blv", "ct", "ln", "pl", "rd", "sq", "st", "wy",
        "rte", "rt", "jct", "riv", "pen",
    }

    NAMES_WITH_EXCLAMATION = {
        # Tech, Corporate Entities, & Major Consumer Brands
        "Yahoo", "Yum", "Chips Ahoy", "Kahoot", "JOOP", "Walla",
        "I Can't Believe It's Not Butter", "Pop", "FreshDirect", "Boost",

        # Gaming, Media, Animation, & Entertainment
        "Mamma Mia", "Jeopardy", "Oklahoma", "Oliver", "Shindig",
        "Hailey's On It", "Airplane", "Osu", "VSPO", "bam", "go", "wham",

       # Geopolitical Quirks / Municipalities
        "Westward Ho", "Saint-Louis-du-Ha", "Baie-des-Ha", "Ha"

        # Public Figures, Politics, & Manufacturing Brands
        "Jeb", "Éxito", "Hey Man", "Basta", "Elliot S",
    }

    COMMON_SENT_STARTERS = set()
    QUOTATIVE_PARTICLES = set()
    CASE_MARKERS = set()
    REPORTING_WORDS = set()

    # https://regex101.com/r/tI9Cmg/2
    VERTICAL_LIST_START_FINDER = re2.compile(r"(?<=^\s*(?:[\p{L}\p{N}]\.){1,3})(?=\s)")

    # https://regex101.com/r/JYdWZw/5
    QUOTE_AND_PAREN_FINDER = re2.compile(
        r"""
        (?:\p{Pi}|»|(?:^|(?<=[\s:]))(['""])).+?(?:\p{Pf}|«|\1)|  # Quoted text (quotation marks)
        —.+?[,.!?]\s*—|          # Quoted text (dashes)
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
        cls.TERMINATORS_PATTERN = "".join(cls.TERMINATORS)
        cls.DOTS_PATTERN = r"[.．]"
        cls.TITLE_ABBRVS_PATTERN = _build_abbr_pattern(cls.TITLE_ABBRVS)
        cls.GEOPOLITICAL_ABBRVS_PATTERN = _build_abbr_pattern(cls.GEOPOLITICAL_ABBRVS)
        cls.COMMON_STARTERS_PATTERN = _build_abbr_pattern(cls.COMMON_SENT_STARTERS)

        # https://regex101.com/r/qBSyU5/15
        # Handle flattened lists due to messy OCR.
        cls.HORIZONTAL_LIST_FINDER = re2.compile(
            r"""
            # Must preceded by string or word boundary
            (?:^|(?<![A-Z]\w+)\s+)
            (?:[•◦]\s+)?   # Optional bullet point (e.g., • 9.)
            (?:
                [-*+]|      #  Markdown style list
                (?:\d{1,2}|[a-eA-E])[.)]{1,2}  #  Numbered and alphabetical list (e.g, a\), 34.\), 1.)
            )
            (?=\s)  # Must followed by a space
            """,
            re2.X,
        )

        # https://regex101.com/r/VMzYsx/10
        cls.NAIVE_BOUNDARY_FINDER = re2.compile(
            rf"""
            (?:
                # Split if left token is a unicase letter (Always)
                (?<=\p{{Lo}}\s*[{cls.TERMINATORS_PATTERN}])|

                # Split after any terminators followed by a a newline,
                # common sentence starter, Space+Upper or unicase letter
                (?<=[{cls.TERMINATORS_PATTERN}])
                (?=
                    \s*[\n\p{{Lo}}]|
                    \s+(?:[^\p{{Ll}}]|
                    \s+(?<!\.\.)(?i:{cls.COMMON_STARTERS_PATTERN})\b)
               )|

                # Split at transition between Latin letters separate by alien
                (?<=[\p{{LU}}\p{{Ll}}][​。！？।])(?=[\p{{Lu}}])
            )

            # Not followed by another terminators (clusters)
            (?!(\s*+[{cls.TERMINATORS_PATTERN}])+)
            """, re2.X,
        )

        # fmt: off
        # Faster than one big regex
        # https://regex101.com/r/svyCoU/21
        cls.MID_SENTENCE_FINDER_LST = [
            # Title abbrv or initialisms (e.g., Dr. Paul)
            re.compile(rf"\b(?i:{cls.TITLE_ABBRVS_PATTERN}){cls.DOTS_PATTERN}"),

            # Abbrv that NEVER ends a sentence
            re.compile(
               rf"\b(?i:{_build_abbr_pattern(cls.MID_SENTENCE_ABBRVS)}){cls.DOTS_PATTERN}"
            ),

            # References abbrv followed by a number, a letter or opened paren/bracket (e.g., to p. 55, app. A, et al. [2004])
            re2.compile(rf"""
                \b(?i:{_build_abbr_pattern(cls.REFERENCE_ABBRVS)}){cls.DOTS_PATTERN}
                (?=\s+(?:\(|\[|\p{{Lu}}\b|\p{{N}}|[IVXLCDM]+))
                """, re2.X
            ),

            # Date abbrv followed by a number
            re2.compile(
                rf"\b(?i:{_build_abbr_pattern(cls.DATE_ABBRVS)}){cls.DOTS_PATTERN}(?=\s+\p{{N}})"
            ),

            # A dot followed by an superscript indicator (e.g. n.º, ​1.º)
            re.compile(r"\.(?=[ºª])"),

            # Initialism/Acronyms/Exclamations words (e.g., Yahoo!, A.B. Holding, Ave. Central)
            # excluding geopolitical ones not followed by a common starters
            re2.compile(rf"""
                (?:(?<={cls.DOTS_PATTERN}|[\p{{Lu}}\s])
                \p{{Lu}}|\b\p{{Lo}})\.
                (?<!(?i:{cls.GEOPOLITICAL_ABBRVS_PATTERN}|p\.m|a\.m){cls.DOTS_PATTERN})
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
                """, re2.X
            ),
            re.compile(rf"""
                (?:(?i:{_build_abbr_pattern(cls.NAMES_WITH_EXCLAMATION)})[! ！‼])
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
               """, re.X
            ),

            # structural headings (e.g., "Section 1. The Beginning.")
            re.compile(rf"""
                \b(?:{_build_abbr_pattern(cls.HEADING_TOKENS)})\s+
                (?:[\dIVXLCDM]+{cls.DOTS_PATTERN}){{1,3}}
                """, re.X
            )
        ]

        # https://regex101.com/r/EGkRU8/6
        cls.QUOTE_AND_PAREN_END_FINDER = re2.compile(
            rf"""
            (?<=
                [{cls.TERMINATORS_PATTERN}]   # A terminator
                (?:'\s|["”]|\s*[»\p{{Pf}}\p{{Pe}}])     # Closing quotes/parens
            )
            (?!  # NOT followed by any continuation markers, punctuation, or space+lowercase
                \s*[\p{{Po}}\p{{Ll}}\p{{Pe}}]|
                {_build_abbr_pattern(cls.QUOTATIVE_PARTICLES | cls.REPORTING_WORDS)}
            )
            """,
            re2.X,
        )

    # fmt: on
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
            # Shift boundaries back (1.\)| => |1.\), a. | => |a. ) to correctly
            # terminate the preceding sentence before flattened horizontal list.
            main_boundaries.update(m.start() + 1 for m in horiz_matches if m.start())

        main_boundaries.difference_update(
            m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(text)
        )

    def _post_process_boundaries(
        self, main_boundaries: set[int], text: str
    ) -> None:
        """Hook for language-specific boundary filtering.

        Override in subclasses to remove false-positive boundaries that
        the regex passes cannot catch. Mutate ``main_boundaries`` in
        place; do not touch any other engine state.
        """

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
        self._post_process_boundaries(main_boundaries, text)

        main_boundaries.update({0, len(text)})
        return sorted(main_boundaries)
