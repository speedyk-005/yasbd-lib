from yasbd.rules.base import Rules


# fmt: off
class HuRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "dr", "prof", "docs", "okl", "mérn",

        # Social & Genealogical
        "id", "ifj", "özv", "néhai",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout & Citations
        "o", "old", "fej", "bek", "ld", "vö", "uo", "im",
        "köt", "kiad", "sz", "jegyz", "ábra", "táb", "mell",

        # List Terminators
        "stb", "s.a.t",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "pl", "kb", "ill", "ti", "ún", "ált", "tkp", "vsz",

        # Address Identifiers
        "u", "krt", "tér", "hrsz",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "Kr.e", "Kr.u", "i.e", "i.sz",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Fejezet", "Szakasz", "Bekezdés", "Melléklet",
        "Rész", "Cikk", "Pont",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "jan", "febr", "márc", "ápr", "máj", "jún",
        "júl", "aug", "szept", "okt", "nov", "dec",
    }

# fmt: on
