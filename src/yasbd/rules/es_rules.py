from yasbd.rules.base import Rules


# fmt: off
class EsRules(Rules):
    ISO_CODE = "es"

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "sr", "sra", "srta", "d", "dña", "dra", "lic", "gral",
        "pdte", "ing", "profa",

        # Noble / Royal
        "s.m", "ss.mm", "s.a.r", "ss.aa.rr", "s.a.s", "s.s", "s.a",
        "ss.aa", "s.e", "v.e", "s.à.s.r", "aa", "mm", "rr", "ss",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "cra", "pág", "núm", "t", "tel", "trad",
    }

    STREET_ABBRVS = Rules.STREET_ABBRVS | {
        "av", "avd", "c", "pso", "ctra", "pl", "blvr",
    }

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {"ej", "p.ej", "vid"}

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "ene", "abr", "ago", "dic", "mié", "jue", "vie", "sáb",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas",

        # Pronouns
        "Yo", "Tú", "Él", "Ella", "Usted", "Nosotros", "Vosotros", "Ellos",
        "Ellas", "aquel", "aquél", "aquella", "aquello", "aquellas",
        "aquellos", "Este", "Esta", "Estos", "Estas", "Ese", "Esa", "Esos",
        "Esas", "Aquí", "Allí",

        # Adverbs
        "Pero", "Entonces", "Así que", "Asi que", "Sin embargo", "Luego",
        "Mientras", "Además", "Aunque",

        # Other common starters
        "¿", "¡" "Millones", "Ya",
    }

# fmt: on
