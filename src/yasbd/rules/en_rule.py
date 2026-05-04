"""English language sentence boundary detection rule."""

from yasbd.rules.base import Rule


class EnRule(Rule):
    """English-specific rule extending Rule.
    
    Adds English-specific abbreviations:
    - Months (jan, feb, mar, etc.)
    - Misc (btw, cal, hwy, etc.)
    """
    
    OTHER_ABBRVS = Rule.OTHER_ABBRVS | {
        # Months
        "apr", "aug", "dec", "feb", "jan", "jul", "jun", "mar", "nov", "oct", "sep", "sept",

        # Misc
        "btw", "cal", "ext", "hway", "hwy", "id", "ing", "me", "mex", "miss", "nos", "plz", "v", "wy",
    }


if __name__ == "__main__":
    rule = EnRule()
    text = """
        Mr. Smith is a Dr. he told me that works at Inc. The meeting is at 5 p.m. Is he there?
        Say hello to dr. smith. Yes, he is. The patient was seen by Sam Smith, M.D. Jr. at the clinic.
    """
    sentences = rule.apply(text)
    for s in sentences:
        print(s)
