from yasbd.rules.base import Rules


# fmt: off
class EnRules(Rules):
    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Honorific
        "messrs", "mlle", "mme", "mmes", "mssrs",

        # Military (Additional)
        "comdr", "cpls", "ens", "sgts",

        # Academic / Professional / Medical
        "asst", "det", "surg",

        # Clerical / Religious
        "fr", "msgr", "revs",

        # Executive
        "v.p",
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {"calif", "dc", "wash", "bc", "ont"}
    STREET_ABBRVS = Rules.STREET_ABBRVS | {"expy", "hway", "hwy", "pkwy", "rt"}
    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Publishing / Documents
        "ch", "chs", "ed", "eds", "fn", "fns",

        # Legal / Numbering
        "r", "rr", "suppl", "supl",

        # Addresses
        "appt",
    }

    COMMON_ORG_NOUNS = Rules.COMMON_ORG_NOUNS | {
        # Government / Political
        "Government", "Parliament", "Senate", "Congress", "Assembly",
        "Ministry", "Department", "Bureau", "Agency", "Commission", "Board",
        "Council", "Committee", "Authority", "Administration",

        # Education / Research
        "University", "College", "Institute", "School", "Academy",

        # Corporate / Business
        "Corporation", "Company", "Association", "Foundation", "Trust",

        # Military / Legal
        "Army", "Navy", "Airforce", "Police", "Force", "Court",

        # Media / Cultural
        "Museum", "Gallery", "Theater", "Theatre", "Network",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "The", "A", "An",

        # Pronouns
        "I", "We", "You", "He", "She", "It", "They", "This", "That",
        "These", "Those", "There",

        # Question words
        "Who", "What", "Where", "When", "Why", "How", "Which", "Whose", "Whom",

        # Adverbs
        "However", "Moreover", "Nevertheless", "Therefore", "Consequently",
        "Meanwhile", "Besides", "Furthermore", "Otherwise",

        # Other common starters
        "Do", "Did", "Millions",

        # Slangs
        # "Wanna", "Gonna", "Trynna",
    }
# fmt: on


if __name__ == "__main__":  # pragma: no cover
    rule = EnRules()
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
