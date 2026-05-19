import re  # For simpler patterns
from collections.abc import Generator, Iterator

import regex as re2
from typeguard import typechecked


def _build_abbr_pattern(options: set[str]) -> str:
    """Build regex pattern from a set while escaping special chars."""
    return "|".join(re2.escape(opt) for opt in sorted(options, key=len))


# fmt: off
class Rules:
    ISO_CODE = "xx"
    TERMINATORS = {"。", "．", ".", "！", "!", "?", "？"}

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

        # Multilateral / Intergovernmental
        "u.n", "u.s.s.r",

        # Asia / Middle East
        "u.a.e", "p.r.c", "r.o.k",
    }

    REFERENCE_ABBRVS = {
        # Publishing / Documents
        "ac", "app", "cf", "chap", "ed", "ext", "fig", "p", "pp", "ref", "res",
        "v", "ver", "viz", "vol", "vols",

        # Section & Paragraph
        "art", "sec",

        # Legal / Numcro
        "no", "suppl", "supl",

        # Scientific / Math
        "eq", "eqn",
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

    COMMON_ORG_NOUNS = {"Army", "Authority", "Commission", "Trust"}
    COMMON_SENT_STARTERS = {"The"}
    QUOTATIVE_PARTICLES = {"と", "って", "라고"}
    REPORTING_WORDS = {"说", "道", "问", "他", "她"}

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

    # fmt: on
    def __init__(self):
        """Compile language-specific regex patterns.

        Patterns that depend on abbreviation sets or terminators are built here
        rather than at class level so subclasses can override the data constants.
        """
        terminators_pattern = "".join(self.TERMINATORS)
        title_abbrvs_pattern = _build_abbr_pattern(self.TITLE_ABBRVS)
        common_starters_pattern = _build_abbr_pattern(self.COMMON_SENT_STARTERS)

        # https://regex101.com/r/qBSyU5/10
        # Handle flattened lists due to messy OCR.
        self.horizontal_list_finder = re.compile(
            rf"""
            (?:   #  Must preceded by
                ^\s*|     # A string start
                [:{terminators_pattern}]\s+  # A terminator or double colon + space
            )
            (?:[•◦]\s+)?   # Optional bullet point (e.g., • 9.)
            (?:
                [-*+]|      #  Markdown style list
                (?:\d{{1,2}}|[^\W_\d])[.)]{{1,2}}  #  Numbered and alphabetical list (e.g, a\), 34.\), 1.)
            )
            (?=\s)  # Must followed by a space
            """,
            re.X,
        )

        # https://regex101.com/r/VMzYsx/5
        self.naive_boundary_finder = re2.compile(
            rf"""
            # Split if left token is a unicase letter (Always)
            (?<=\p{{Lo}}[{terminators_pattern}])|

            # Split after any terminators followed by a common sentence starter,
            # Space+Upper or unicase letter
            (?<=[{terminators_pattern}])
            (?=
                \s+(?:[^\p{{Ll}}]|(?i:{common_starters_pattern})\b)|
                \s*\p{{Lo}}
            )|
            
            # Cluster of terminators (e.g hello!!! r u ok?)
            (?<=[{terminators_pattern.replace('.', '')}]{{2,}})(?=\s)
            """,
            re2.X,
        )

        # https://regex101.com/r/svyCoU/6
        self.mid_sentence_finder = re2.compile(
            rf"""
            # Title abbrv or initialisms (e.g., Dr. Paul)
            (?<=\b(?i:{title_abbrvs_pattern})\.)|

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            (?<=\b(?i:{_build_abbr_pattern(self.GEOPOLITICAL_ABBRVS)})\.)
            (?=\s+(?:{_build_abbr_pattern(self.COMMON_ORG_NOUNS)}))|

            # Abbrv that NEVER ends a sentence
            (?<=\b(?i:{_build_abbr_pattern(self.MID_SENTENCE_ABBRVS)})\.)|

            # References abbrv followed by a number (e.g., to p. 55)
            (?<=\b(?i:{_build_abbr_pattern(self.REFERENCE_ABBRVS)})\.)(?=\s+\p{{N}})|

            # Acronyms/Exclamations words (e.g., Yahoo!, A.B. Holding)
            (?<=\.\p{{Lu}}\.|\b(?i:{_build_abbr_pattern(self.NAMES_WITH_EXCLAMATION)})!)
            (?!\s+(?:{common_starters_pattern})\b)|

            # Collapsed middle name (e.g, Jonas E. Smith)
            (?<=\s\b(?:\p{{Lu}})\.)(?=\s)
            """,
            re2.X,
        )

        # https://regex101.com/r/EGkRU8/7
        self.quote_and_paren_end_finder = re2.compile(
            rf"""
            (?<=
                [{terminators_pattern}]   # A terminator
                (?:'\s|["”]|\s*[»\p{{Pf}}\p{{Pe}}])     # Closing quotes/parens
            )
            (?!  # NOT followed by any continuation markers, punctuation, or space+lowercase
                \s*\p{{po}}|
                {"|".join(self.QUOTATIVE_PARTICLES | self.REPORTING_WORDS)}|
                \s+[\p{{Ll}}]|$
            )
            """,
            re2.X,
        )

        # https://regex101.com/r/ffqwjh/2
        self.contiguous_terminators_finder = re.compile(rf"(?:\s*+[{terminators_pattern}]){{2,}}")

    def _remove_quote_and_paren_spans(
        self,
        main_boundaries: set[int],
        line: str,
        preserve_quote_and_paren: bool,
    ) -> None:
        """Remove boundaries inside quoted/parenthesised spans."""
        if preserve_quote_and_paren:
            protected_spans = set()
            for m in self.QUOTE_AND_PAREN_FINDER.finditer(line):
                inner_range = set(range(*m.span()))
                protected_spans.update(inner_range)
            main_boundaries.difference_update(protected_spans)

        main_boundaries.update(
            m.end() for m in self.quote_and_paren_end_finder.finditer(line)
        )

    def _remove_toc_spans(
        self, main_boundaries: set[int], line: str
    ) -> None:
        """Remove boundaries inside TOC leader runs."""
        if "..." in line:
            for m in self.TOC_LEADER_FINDER.finditer(line):
                main_boundaries.difference_update(range(*m.span()))

    def _adjust_list_boundaries(self, main_boundaries: set[int], line: str) -> None:
        """Remove and re-align boundaries around list markers."""
        horiz_matches = list(self.horizontal_list_finder.finditer(line))
        if len(horiz_matches) >= 2:
            main_boundaries.difference_update(m.end() for m in horiz_matches)
            # Shift boundaries the pointer back (1.\)| => |1.\), a. | => |a. ) to correctly
            # terminate the preceding sentence before flattened horizontal list.
            main_boundaries.update(m.start() + 1 for m in horiz_matches if m.start())

        main_boundaries.difference_update(
            m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(line)
        )

    @typechecked
    def apply(
        self,
        line_iter: Iterator[str],
        preserve_quote_and_paren: bool,
        relative: bool = False,
    ) -> Generator[tuple[int, int], None, None]:
        """Detect sentence boundaries for each line.

        Two-pass algorithm:
        1. Collect boundary candidates from punctuation positions.
        2. Remove false alarms (mid-sentence abbreviations, ellipsis,
           quote/paren spans, list markers).

        Args:
            line_iter: Source of text lines (string stream or iterator).
            preserve_quote_and_paren: If ``True``, suppress boundaries
               inside quote and parenthesis spans.
            relative: If ``False`` (default), yield offsets relative to
                the full text. If ``True``, offsets are per-line.

        Yields:
            ``(start_offset, end_offset)`` per sentence.
        """
        offset = 0
        for line in line_iter:
            if not line.strip():
                n = len(line)
                yield (offset, offset + n) if not relative else (0, n)
                if not relative:
                    offset += n
                continue

            main_boundaries = set()
            main_boundaries.update(
                m.end() for m in self.naive_boundary_finder.finditer(line)
            )

            # -- Remove false alarms --
            main_boundaries.difference_update(
                m.end() for m in self.mid_sentence_finder.finditer(line)
            )
            self._remove_quote_and_paren_spans(
                main_boundaries, line, preserve_quote_and_paren
            )
            self._remove_toc_spans(main_boundaries, line)
            self._adjust_list_boundaries(main_boundaries, line)

            # Remove contiguous term except last one (e.g., Hello! !!   !! )
            main_boundaries.difference_update(
                *(
                    range(m.start(), m.end() - 1)
                    for m in self.contiguous_terminators_finder.finditer(line)
                )
            )

            main_boundaries.update({0, len(line)})
            main_boundaries_lst = sorted(main_boundaries)
            for i in range(len(main_boundaries) - 1):
                start = main_boundaries_lst[i]
                end = main_boundaries_lst[i + 1]
                yield (offset + start, offset + end) if not relative else (start, end)

            if not relative:
                offset += len(line)
