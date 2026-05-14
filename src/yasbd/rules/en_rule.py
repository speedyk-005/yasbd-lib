from yasbd.rules.base import Rule


class EnRule(Rule):
    """English-specific rule extending Rule.
    
    Adds English-specific abbreviations:
    - Months (jan, feb, mar, etc.)
    - Misc (btw, cal, hwy, etc.)
    """
    ISO_CODE = "en"
    MID_SENTENCE_ABBRVS = Rule.MID_SENTENCE_ABBRVS | {"ing", "wy"}
    REFERENCE_ABBRVS = Rule.REFERENCE_ABBRVS | {"nos", "hway", "hwy",}

    COMMON_STARTERS = {
        "A", "An", "Being", "Did", "For", "He", "How", "However", "I", "In", "It",
        "Millions", "More", "She", "That", "The", "Their", "These", "They", "This",
        "Those", "We", "What", "When", "Where", "Who", "Why", "You",
    }
    COMMON_ORG_NOUNS = {"Army", "Government", "Federation", "Senate", "Council", "Commission", "Parliament"}


if __name__ == "__main__":
    rule = EnRule()
    text = """
        The system requirements for the project are simple: 1. Python 3.12 environment. 2. At least 8GB of RAM. 3. Access to the PUA character set for Sinta markers. Please ensure these are met before initialization.

        To install Sinta, follow these steps:
        1. They Clone the repository from the internal server.
        2. Initialize the virtual environment using the provided script.
        3. Run the $O(n)$ test suite to verify performance.
        Deployment will follow successful testing.

        The project (which had been delayed for months. ) was finally complete.
    """
    sentences = rule.apply(text, True)
    for s in sentences:
        print(repr(s))
