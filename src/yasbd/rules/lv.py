from yasbd.rules.base import Rules


# fmt: off
class LvRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "asoc", "doc", "mg", "bc", "inž", "habil",

        # Social
        "k-gs", "kdze",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout & Citations
        "lpp", "nod", "att", "tab", "piel", "sēj", "izd",
        "sk", "skat", "salīdz", "ats", "nr",

        # Legal Reference Identifiers
        "pkt", "apakšp", "lik", "not", "MK",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "piem", "t.i", "t.sk", "u.c", "u.tml", "utt", "resp", "apm",

        # Temporal & Quantitative
        "gs", "g", "tūkst", "milj",

        # Address Identifiers
        "iela", "bulv", "pag", "nov",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Nodaļa", "Sadaļa", "Pants", "Punkts", "Daļa",
        "Pielikums", "Priekšvārds",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "janv", "febr", "apr", "jūn", "jūl", "aug",
        "sept", "okt", "nov", "dec",
    }

# fmt: on
