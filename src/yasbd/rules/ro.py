from yasbd.rules.base import Rules


# fmt: off
class RoRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Standard Professional / Academic
        "arh", "av", "conf", "lect", "asist", "acad",
        "cerc", "dir", "drd", "prep",

        # Social & Religious Address
        "sf", "cuv", "părinte",

        # Traditional Given Name Initials (Highly critical)
        "Al", "Dem", "Fr", "Gh", "Gr", "Șt",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "R.S.R", "R.P.R", "S.U.A", "U.E", "M.B",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical & Academic Citations
        "vezi", "apud", "id", "trad", "coord", "colab",
        "urm", "ș.a", "obs", "șamd",

        # Legal & Structural Cross-References
        "alin", "lit", "pct", "secț",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Capitolul", "Secțiunea", "Articolul", "Alineatul", "Tabelul",
        "Figura", "Anexa", "Nota", "Introducere", "Concluzii",
    }

    # Administrative, Geographic, & Address Elements
    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "str", "bd", "bld", "os", "al", "p-ța", "intr", "jud", "loc",
        "com", "sat", "sc", "et", "ap",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "ian", "iun", "iul", "mar", "mie", "joi", "vin",
        "sâm", "dum",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Eu", "Tu", "El", "Ea", "Noi", "Voi", "Ei", "Ele",
        "Acest", "Această", "Acestea", "Aceștia",
        "Cine", "Ce", "Care", "Nimeni", "Cineva",

        # Question words
        "Unde", "Cum", "Când", "De ce",

        # Common Transitions / Adverbs
        "Deși", "Deoarece", "Pentru că", "Fiindcă",
        "Dacă", "Prin urmare", "Deci", "În plus",
        "Mai mult", "Totuși", "De pildă", "De exemplu",
        "În primul rând", "În concluzie", "Astfel",
        "Astăzi", "Ieri",
    }

# fmt: on
