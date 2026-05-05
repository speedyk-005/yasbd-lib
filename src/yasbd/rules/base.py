"""Multilingual sentence boundary detection rule."""

from collections.abc import Iterator

import regex as re


class Rule:
    """Base rule for sentence boundary detection.
    
    Provides abbreviation sets and split patterns to handle common cases where
    periods should NOT indicate sentence boundaries (e.g., "Mr.", "Dr.", "Inc.").
    
    Attributes:
        ALPHABET: Single letter initials (A-Z).
        PUNCTUATIONS: Sentence-ending punctuation marks.
        TITLE_ABBRVS: Honorifics and titles (Dr., Mr., etc.).
        OTHER_ABBRVS: Other abbreviations (Inc., Co., etc.).
    """
    
    ALPHABET = {
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    }

    PUNCTUATIONS = {
        "。", "．", ".", "！", "!", "?", "？"
    }

    TITLE_ABBRVS = {
        "adj", "adm", "adv", "assn", "asst", "bart", "bldg", "brig", "bros", "capt", "cmdr",
        "col", "comdr", "con", "cpl", "dr", "dr.phil", "dr.philos", "drs", "ens", "gen",
        "gov", "hon", "hr", "hosp", "jr", "insp", "lt", "maj", "messrs", "mlle", "mme", "mr",
        "mrs", "ms", "msgr", "op", "ord", "pfc", "ph", "prof", "pvt", "rep", "reps", "res",
        "rev", "rt", "sen", "sens", "sfc", "sgt", "sr", "st", "supt", "surg",
    }

    OTHER_ABBRVS = {
        # Roman numerals
        "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ", "Ⅼ", "Ⅽ", "Ⅾ", "Ⅿ",
        "ⅰ", "ⅱ", "ⅲ", "ⅳ", "ⅴ", "ⅵ", "ⅶ", "ⅷ", "ⅸ", "ⅹ", "ⅺ", "ⅻ", "ⅼ", "ⅽ", "ⅾ", "ⅿ",

        # Org/Business
        "approx", "asst", "assoc", "bros", "bldg", "co", "corp", "dept", "est", "inc",
        "ltd", "mfsg", "misc", "univ",

        # Units (measurement)
        "cm", "ft", "in", "kg", "km", "lb", "mi", "mm", "mph", "oz", "qt", "sq", "vol", "wt",

        # Time/date
        "a.m", "ac", "ad", "bc", "dc", "fy", "hr", "min", "msec", "ms", "p.m",
        "sec", "wk", "yr",

        # Location
        "apt", "bld", "blvd", "dept", "fl", "lat", "long", "mt", "mtn", "ne", "nw",
        "rd", "rm", "se", "ste", "st", "sw",

        # Academic/scientific
        "cf", "ed", "eg", "e.g", "fig", "i.e", "ph.d", "phd", "pp", "ref",
        "res", "sec", "viz", "vs", "etc", "approx", "avg",

        # US states/regions
        "ariz", "ark", "calif", "colo", "conn", "dak", "del", "fla", "ga", "ia", "ida",
        "ill", "ind", "kan", "kans", "ken", "ky", "la", "mass", "md", "mich", "minn",
        "mont", "n.c", "n.j", "n.y", "neb", "nebr", "nev", "nh", "okla", "ont", "ore",
        "pa", "penn", "penna", "ri", "sask", "tenn", "tex", "ut", "va", "vt", "wash",
        "wis", "wisc", "wyo", "yuk",

        # Other
        "acct", "admin", "al", "ala", "alta", "alt", "amt", "ans", "arc", "atty", "cert",
        "cl", "cont", "cres", "ct", "curr", "det", "dist", "div", "esq", "exec", "exp",
        "expy", "fed", "fwy", "info", "insp", "man", "may", "med", "mfg", "mlle",
        "mme", "msgr", "mssrs", "nr", "ord", "pd", "pkg", "pde", "pl", "qty", "que", "rs",
        "tce", "u.s", "usafa", "ver", "univ",
    }

    def __init__(self):
        _all_abbrvs = self.TITLE_ABBRVS | self.OTHER_ABBRVS | self.ALPHABET
        all_abbrvs_pattern = r"\.|".join(_all_abbrvs) + r"\."
        other_abbrvs_pattern = r"\.|".join(self.OTHER_ABBRVS) + r"\."

        self.double_abbrvs_split_regex = re.compile(rf"({all_abbrvs_pattern})\s+(?={all_abbrvs_pattern})", re.I)
        self.not_a_name_split_regex = re.compile(
            rf"(?<=(?i:{other_abbrvs_pattern}))\s+(?=[\p{{Lu}}\p{{Lo}}\p{{Lt}}])",
        )

        self.abbr_safe_split_regex = re.compile(rf"""
            (?<!\b(?:     # If not preceded by 
                {all_abbrvs_pattern}|\d\.
                # |[IVXLCDM]+\.   # Skip decimal numbers and standard Latin-Roman numerals
            ))
            (?<=[{"".join(self.PUNCTUATIONS)}])  # Split after punctuation
            (?=\s+[\p{{Lu}}\p{{Lo}}\p{{Lt}}]|\s*\n|$)  # followed by letter (upper or catch-all) or end
            """,
            re.I | re.X,
        )

    def apply(self, text: str) -> Iterator[str]:
        """Split text into sentences.
        
        Args:
            text: Input text to split into sentences.
            
        Yields:
            Individual sentences.
        """
        # Pre-processing (edge cases):
        #  - double_abbrvs_split_pattern: Handles "A. B." where both are abbrvs
        #  - not_a_name_split_pattern: Handles "Inc. The" where next is uppercase
        #    but the abbr isnt a title
        text = self.double_abbrvs_split_regex.sub(
            # Skip initials
            lambda m: "\n" if len(m.group(0)) == 2  else m.group(0), text.strip()
        )
        text = self.not_a_name_split_regex.sub("\n", text)
 
        # Main split: split based on punctuation then on newlines
        for sent in self.abbr_safe_split_regex.split(text):
            stripped_sent = sent.strip() 
            if stripped_sent:
                yield from stripped_sent.splitlines()
