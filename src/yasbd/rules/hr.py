from yasbd.rules.base import Rules


# fmt: off
class HrRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "doc", "mr", "inž", "akad", "izv",

        # Social
        "gosp", "gđa", "gdin", "gđica",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout & Citations
        "str", "pogl", "čl", "st", "sl", "tab", "usp",
        "vidi", "isto", "sv", "izd", "god", "br", "bilj",

        # Legal Reference Identifiers
        "toč", "podst", "zak", "prav", "NN",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "npr", "tj", "itd", "tzv", "odn", "sl", "i sl",
        "uklj", "cca", "otpr",

        # Address Identifiers
        "ul", "trg", "obala", "kbr",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Poglavlje", "Članak", "Stavak", "Dio",
        "Odjeljak", "Prilog", "Točka",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "sij", "velj", "ožu", "tra", "svi", "lip",
        "srp", "kol", "ruj", "lis", "stu", "pro",

        # Days
        "pon", "uto", "sri", "čet", "pet", "sub", "ned",
    }

# fmt: on
