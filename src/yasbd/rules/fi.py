from yasbd.rules.base import Rules


# fmt: off
class FiRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "dos", "toht", "tri", "fil", "maist", "ins", "dipl.ins",
        "kand", "yliopp",

        # Social
        "hra", "rva", "nti",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout & Citations
        "s", "ss", "kpl", "kuv", "taul", "liite", "ks",
        "vrt", "huom", "nro", "n:o", "mom", "kohta",

        # Legal Reference Identifiers
        "pykälä", "ao", "em", "ml",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "esim", "mm", "jne", "ym", "yms", "tms", "ts", "ns",
        "n", "mrd", "milj",

        # Temporal
        "klo", "eaa", "jaa",

        # Address Identifiers
        "os", "pl", "as",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Luku", "Osa", "Kohta", "Liite", "Pykälä", "Momentti",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "tammik", "helmik", "maalisk", "huhtik", "toukok", "kesäk",
        "heinäk", "elok", "syysk", "lokak", "marrask", "jouluk",

        # Days
        "ma", "ti", "ke", "to", "pe", "la", "su",
    }

# fmt: on
