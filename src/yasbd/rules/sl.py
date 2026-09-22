from yasbd.rules.base import Rules


# fmt: off
class SlRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "doc", "mag", "univ", "izr", "akad", "dipl",

        # Social
        "g", "ga", "gdč",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout & Citations
        "str", "pogl", "čl", "odst", "sl", "tab", "prim",
        "gl", "št", "zv", "izd", "op", "pril",

        # Legal Reference Identifiers
        "tč", "al", "zak", "ur.l",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "npr", "tj", "itd", "ipd", "oz", "t.i", "cca",
        "pribl", "sod",

        # Address Identifiers
        "ul", "trg", "c", "št.h",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Poglavje", "Člen", "Odstavek", "Del",
        "Oddelek", "Priloga", "Točka",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "jan", "feb", "mar", "apr", "maj", "jun",
        "jul", "avg", "sep", "okt", "nov", "dec",

        # Days
        "pon", "tor", "sre", "čet", "pet", "sob", "ned",
    }

# fmt: on
