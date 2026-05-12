import io
from collections.abc import Iterator

import regex as re


class Rule:
    ISO_CODE = "xx"
    TERMINATORS = {
        "。", "．", ".", "！", "!", "?", "？"
    }

    TITLE_ABBRVS = {
        # Standard Professional (Universal Latin roots)
        "dr", "drs", "prof", "sr", "jr", "hon", "rev", "supt", "insp",

        # Global Social (Overlap across English/Spanish/Portuguese/French)
        "mr", "mrs", "ms", "sr", "st",

        # Military (NATO/International Standardized Ranks)
        "adm", "brig", "capt", "cmdr", "col", "cpl", "gen", "lt", "maj", "sgt", "pvt",
    
        # Political/Administrative (Common in Western bureaucracy)
        "gov", "rep", "sen", "pres"
    }

    GEOPOLITICAL_ABBRVS = {
        "us", "u.s", "uk", "u.k", "eu", "e.u", "usa", "u.s.a", "un", "u.n", "ussr",
    }

    REFERENCE_ABBRVS = {
        "ac", "chap", "cf", "ed", "fig", "p", "pp", "ref", "res", "sec", "ver", "viz", 
    }

    MID_SENTENCE_ABBRVS = {
        # Business entity bridges
        "assoc", "mfg",

        # Bridge/connectors
        "cf", "eg", "e.g", "ie", "i.e", "vs", "v", "viz", "ibid", "ca", "sc",

        # Street & directional anchors
        "mt", "dist",
    }

    COMMON_STARTERS = {}
    COMMON_ORG_NOUNS = {}

    # https://regex101.com/r/tI9Cmg/2
    VERTICAL_LIST_START_FINDER = re.compile(r"(?<=^\s*(?:[\p{L}\p{N}]\.){1,3})(?=\s)")
    
    def __init__(self):
        _title_abbrvs_pattern = "|".join(self.TITLE_ABBRVS)
        _terminators_pattern = "".join(self.TERMINATORS)

        # https://regex101.com/r/qBSyU5/10
        # Handle flattened lists due to messy OCR.
        self.horizontal_list_finder = re.compile(rf""" 
            (?:   #  Must preceded by
                ^\s*|     # A string start
                [:{_terminators_pattern}]\s+  # A terminator or double colon + space
            ) 
            (?:[•◦]\s+)?   # Optional bullet point (e.g., • 9.)
            (?:
                [-*+]|      #  Markdown style list
                (?:\d{{1,2}}|[^\W_\d])[.)]{{1,2}}  #  Numbered and alphabetical list (e.g, a\), 34.\), 1.)
            )
            (?=\s)  # Must followed by a space
            """, re.X
        )

        # https://regex101.com/r/VMzYsx/4
        self.naive_boundary_detector = re.compile(rf"""
            # Split if left token is a unicase letter (Always)
            (?<=\p{{Lo}}[{_terminators_pattern}])|

            # Split after any terminators followed by Space+Upper or unicase letter
            (?<=[{_terminators_pattern}]+)(?=\s+[^\p{{Ll}}]|\s*\p{{Lo}})
            """, re.X
        )

        # https://regex101.com/r/svyCoU/1
        self.mid_sentence_finder = re.compile(rf"""
            # Title abbrv or initialisms is NOT followed by a common ender (e.g., Dr. Paul)
            (?<=\b(?i:{_title_abbrvs_pattern})\.)(?!\s+(?:{"|".join(self.COMMON_STARTERS)}))|

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            (?<=\b(?i:{"|".join(self.GEOPOLITICAL_ABBRVS)})\.)(?=\s+(:{"|".join(self.COMMON_ORG_NOUNS)}))|

            # Abbrv that NEVER ends a sentence
            (?<=\b(?i:{"|".join(self.MID_SENTENCE_ABBRVS)})\.)|

            # References abbrv followed by a number (e.g., to p. 55)
            (?<=\b(?i:{"|".join(self.REFERENCE_ABBRVS)})\.)(?=\s+\p{{N}})|

            # Collapsed middle name (e.g, Jonas E. Smith)
            (?<=\s\b(?:\p{{Lu}})\.)(?=\s)
            """, re.X
        )

    def apply(
        self,
        input: str | io.IOBase,
        preserve_quote_and_paren: bool,
    ) -> Iterator[tuple]:
        line_iter = io.StringIO(input) if isinstance(input, str) else input
        for line in line_iter:
            main_boundaries = {0, len(line)}
            if line:
                main_boundaries.update({m.end() for m in self.naive_boundary_detector.finditer(line)})

                # Remove false alarms
                main_boundaries.difference_update({m.end() for m in self.mid_sentence_finder.finditer(line)})

                # Prevents list-marker fragmentation by removing markers
                horiz_list_boundaries = {m.end() for m in self.horizontal_list_finder.finditer(line)}
                horiz_list_boundaries = (  # Reduce false alarm
                    horiz_list_boundaries if len(horiz_list_boundaries) >= 2 else set()
                )
                vert_list_boundaries = {m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(line)}
                main_boundaries.difference_update(horiz_list_boundaries | vert_list_boundaries)

                # Shift boundaries 3 chars back (1.\)| => |1.\), a. | => |a. ) to correctly terminate 
                # the preceding sentence before 'In-line' horizontal list transitions.
                main_boundaries.update(
                    {m.start() + 1 for m in self.horizontal_list_finder.finditer(line) if m.start()}
                )

                main_boundaries_lst = sorted(list(main_boundaries))
                yield from (
                    (line[start:end], (start, end))
                    for start, end in zip(main_boundaries_lst, main_boundaries_lst[1:])
                )
