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

    # https://regex101.com/r/tI9Cmg/1
    VERTICAL_LIST_START_FINDER = re.compile(r"(?<=^\s*(?:[\p{L}\p{N}]\.){1,3})(?=\s)")
    
    def __init__(self):
        _title_abbrvs_pattern = "|".join(self.TITLE_ABBRVS)
        _common_starters_pattern = "|".join(self.COMMON_STARTERS)
        _terminators_pattern = "".join(self.TERMINATORS)

        # https://regex101.com/r/qBSyU5/3
        # Handle inline lists/citations: NLTK favors grammar; PySBD favors list-structure
        # Yasbd takes the middle ground: Considers "1." a list start unless followed by common starter
        self.horizontal_list_finder = re.compile(rf"""
            (?<=[^\w\n]\s+\d\.)     # A number between 0-9 followed by dot + whitespace
            (?!\s+\b(?:{_common_starters_pattern})\b)  # But not followed by a common starters
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
            # A title abbrv or initialisms is NOT followed by a common starter (e.g., Dr. Paul)
            (?<=\b(?i:{_title_abbrvs_pattern})\.)(?!\s+(?:{_common_starters_pattern}))|

            # A geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            (?<=\b(?i:{"|".join(self.GEOPOLITICAL_ABBRVS)})\.)(?=\s+(:{"|".join(self.COMMON_ORG_NOUNS)}))|

            # An abbrv that never ends a sentence
            (?<=\b(?i:{"|".join(self.MID_SENTENCE_ABBRVS)})\.)
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
                main_boundaries.update({m.start() for m in self.naive_boundary_detector.finditer(line)})

                # Remove false alarms
                main_boundaries.difference_update({m.start() for m in self.mid_sentence_finder.finditer(line)})

                # Prevents list-marker fragmentation by removing markers from the 
                # candidate set and shifting boundaries 2 chars back (1.| => |1.) to correctly 
                # terminate the preceding sentence before 'In-line' horizontal list transitions.
                horiz_list_boundaries = {m.start() for m in self.horizontal_list_finder.finditer(line)}
                vert_list_boundaries = {m.start() for m in self.VERTICAL_LIST_START_FINDER.finditer(line)}
                main_boundaries.difference_update(horiz_list_boundaries | vert_list_boundaries)
                main_boundaries.update(
                    {pos - 2 for pos in horiz_list_boundaries - vert_list_boundaries}
                )

                main_boundaries_lst = sorted(list(main_boundaries))
                yield from [
                    (line[start:end], (start, end))
                    for start, end in zip(main_boundaries_lst, main_boundaries_lst[1:])
                ]
