import io
import re  # For simpler pattern
from collections.abc import Iterator

import regex as re2


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
        "ac", "chap", "cf", "ed", "fig", "p", "pp", "ref", "res", "sec", "v", "ver", "viz",
        "ext",
    }

    MID_SENTENCE_ABBRVS = {
        # Business entity bridges
        "assoc", "mfg",

        # Bridge/connectors
        "cf", "eg", "e.g", "ie", "i.e", "vs", "v", "viz", "ibid", "ca", "sc",

        # Street & directional anchors
        "mt", "dist",
    }

    EXCLAMATION_NAMES = {
        "Ha", "Yahoo", "Yum", "Chips Ahoy", "Kahoot", "JOOP", "Joomla", "Starz",
        "Jeopardy", "Airplane", "Oklahoma", "Mamma Mia", "Oliver", "Shindig",
        "Westward Ho", "Saint-Louis-du-Ha! Ha", "Jeb", "Elliot S", "Air France Hop",
        "Basta", "¡Éxito", "Pepitos", "OSN Yahala", "Shugo Chara", "Adopt Me", "Bingo",
        "E", "Hailey's On It", "Hey Boo", "Hey Man! Let's Eat", "Microsoft Plus", "Off",
        "Osu", "PBS Kids Go", "Pop", "Red Bip", "RedeTV", "This Can't Be Yogurt",
        "Transfer It", "VSPO", "Walla", "WWE Smackdown",
    }

    COMMON_STARTERS = {"The"}
    COMMON_ORG_NOUNS = {"Commission", "Federation"}
    QUOTATIVE_PARTICLES = {"と", "って", "라고"}
    REPORTING_WORDS = {"说", "道", "问", "他", "她"}

    # https://regex101.com/r/tI9Cmg/2
    VERTICAL_LIST_START_FINDER = re2.compile(r"(?<=^\s*(?:[\p{L}\p{N}]\.){1,3})(?=\s)")

    # https://regex101.com/r/JYdWZw/1
    QUOTE_AND_PAREN_FINDER = re2.compile(r"""
        (?:\p{Pi}|»|(['"”])).+?(?:\p{Pf}|«|\1)|  # Quoted text
        \p{Ps}.+?\p{Pe}  # Parenthesized text
        """, re2.X
    )

    # https://regex101.com/r/wILgbJ/1
    ELLIPSIS_FINDER = re.compile(r"[！!?？]?(?:\s*\.){3,4}")

    # https://regex101.com/r/0P9f2V/1
    TOC_LEADER_FINDER = re.compile(r"[^\W_][\s\.]{4,}\d")
    
    def __init__(self):
        _title_abbrvs_pattern = "|".join(self.TITLE_ABBRVS)
        _terminators_pattern = "".join(self.TERMINATORS)

        # https://regex101.com/r/qBSyU5/10
        # Handle flattened lists due to messy OCR.
        self.horizontal_list_finder = re2.compile(rf""" 
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
            """, re2.X
        )

        # https://regex101.com/r/VMzYsx/4
        self.naive_boundary_detector = re2.compile(rf"""
            # Split if left token is a unicase letter (Always)
            (?<=\p{{Lo}}[{_terminators_pattern}])|

            # Split after any terminators followed by Space+Upper or unicase letter
            (?<=[{_terminators_pattern}])(?=\s+[^\p{{Ll}}]|\s*\p{{Lo}})
            """, re2.X
        )

        # https://regex101.com/r/svyCoU/3
        self.mid_sentence_finder = re2.compile(rf"""
            # Title abbrv or initialisms is NOT followed by a common ender (e.g., Dr. Paul)
            (?<=\b(?i:{_title_abbrvs_pattern})\.)(?!\s+(?:{"|".join(self.COMMON_STARTERS)}))|

            # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
            (?<=\b(?i:{"|".join(self.GEOPOLITICAL_ABBRVS)})\.)(?=\s+(?:{"|".join(self.COMMON_ORG_NOUNS)}))|

            # Abbrv that NEVER ends a sentence
            (?<=\b(?i:{"|".join(self.MID_SENTENCE_ABBRVS)})\.)|

            # References abbrv followed by a number (e.g., to p. 55)
            (?<=\b(?i:{"|".join(self.REFERENCE_ABBRVS)})\.)(?=\s+\p{{N}})|

            # Exclamations words (e.g., Yahoo!)
            (?<=\b(?:{"|".join(self.EXCLAMATION_NAMES)})!)|

            # Collapsed middle name (e.g, Jonas E. Smith)
            (?<=\s\b(?:\p{{Lu}})\.)(?=\s)
            """, re2.X
        )
        
        # https://regex101.com/r/EGkRU8/4
        self.quote_and_paren_end_finder = re2.compile(rf"""
            (?<=[{_terminators_pattern}]\s*   # A terminator followed by additional space
            ["”«\p{{Pf}}])     # Closing quotes
            (?!  # NOT followed by any continuation markers or space+lowercase letter or end
                {"|".join(self.QUOTATIVE_PARTICLES)}|{"|".join(self.REPORTING_WORDS)}|
                \s+[\p{{Ll}}]|$
            )
            """, re2.X
        )

    def apply(
        self,
        line_iter: io.IOBase | Iterator,
        preserve_quote_and_paren: bool,
    ) -> Iterator[tuple]:
        for line in line_iter:
            main_boundaries = set()
            if line.strip():
                main_boundaries.update(m.end() for m in self.naive_boundary_detector.finditer(line))
                quote_and_paren_boundaries = {m.end() for m in self.quote_and_paren_end_finder.finditer(line)}
                main_boundaries.update(quote_and_paren_boundaries)

                # -- Remove false alarms --

                if preserve_quote_and_paren:
                    protected_spans = set()
                    for m in self.QUOTE_AND_PAREN_FINDER.finditer(line):
                        inner_range = set(range(*m.span()))
                        protected_spans.update(inner_range - quote_and_paren_boundaries)
                    main_boundaries.difference_update(protected_spans)
                main_boundaries.difference_update(m.end() for m in self.mid_sentence_finder.finditer(line))

                # Shields ellipsis and dot leaders
                for m in self.ELLIPSIS_FINDER.finditer(line):
                    main_boundaries.difference_update(range(*m.span()))
                for m in self.TOC_LEADER_FINDER.finditer(line):
                    main_boundaries.difference_update(range(*m.span()))

                # Prevents list-marker fragmentation by removing markers
                horiz_list_boundaries = {m.end() for m in self.horizontal_list_finder.finditer(line)}
                horiz_list_boundaries = (  # Reduce false alarm
                    horiz_list_boundaries if len(horiz_list_boundaries) >= 2 else set()
                )
                main_boundaries.difference_update(horiz_list_boundaries)
                main_boundaries.difference_update(
                    m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(line)
                )

                # Shift boundaries the pointer back (1.\)| => |1.\), a. | => |a. ) to correctly terminate 
                # the preceding sentence before flattened horizontal list.
                main_boundaries.update(
                    m.start() + 1 for m in self.horizontal_list_finder.finditer(line) if m.start()
                )

                # Add the start and end so we can handle empty boundaries
                main_boundaries.update({0, len(line)})
                main_boundaries_lst = sorted(main_boundaries)
                yield from (
                    (line[start:end], (start, end))
                    for start, end in zip(main_boundaries_lst, main_boundaries_lst[1:])
                )
