from yasbd.rules.base import Rules


# fmt: off
class ItRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "sig", "sig.ra", "sig.na", "sigg", "dott",
        "dott.ssa", "dott.sa", "dott.re", "dott.ri", "prof.ssa",
        "prof.sa", "avv", "arch", "geom", "rag",
        "not", "comm", "cav", "on", "dep", "spett",

        # Military ranks (Italian-specific)
        "amm", "cap", "ten", "serg",

        # Academic
        "ch.mo", "chiar.mo", "magn", "rett",

        # Noble / Royal / Religious
        "s", "ss", "s.s", "p", "mons", "card",
        "s.e", "s.a", "s.a.r", "s.a.s", "s.e.r",
        "v.e", "s.m", "ll.mm", "ll.ee", "ss.mm",
        "b.ne", "f.lli", "vesc", "arciv",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "cap", "capit", "par", "parag", "sez", "fasc", "trad",
        "rif", "cit", "op.cit", "artt", "n.s", "s.l", "s.d", "s.n.t",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Capitolo", "Articolo", "Sezione", "Paragrafo",
        "Parte", "Appendice", "Prefazione",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "es", "p.es", "ecc", "c.d", "c.d.d",
        "v", "vv", "ss", "segg",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "S.P.A", "S.R.L", "S.N.C", "S.A.P.A", "S.S", "S.P", "S.R",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "CheBanca", "Zeus",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "gen", "febbr", "apr", "mag", "giu",
        "lug", "ago", "sett", "ott", "dic",

        # Days
        "mart", "mer", "giov", "ven", "sab",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Il", "Lo", "La", "L'", "Gli", "I", "Le",
        "Un", "Uno", "Una",

        # Pronouns
        "Io", "Tu", "Lui", "Lei", "Egli", "Ella", "Esso", "Essa",
        "Noi", "Voi", "Loro", "Essi", "Esse",
        "Questo", "Questa", "Questi", "Queste",
        "Quello", "Quella", "Quei", "Quelle",

        # Adverbs & Transitions
        "Ma", "Però", "Tuttavia", "Quindi", "Dunque",
        "Sempre", "Mai", "Ancora", "Già", "Appena", "Ormai",
        "Inoltre", "Neanche", "Nemmeno", "Neppure", "Così",
        "Piuttosto", "Quasi", "Almeno", "Davvero", "Certamente",
        "Sicuramente", "Probabilmente", "Forse", "Magari", "Chissà",

        # Question words
        "Chi", "Che", "Cosa", "Quando", "Dove", "Come", "Perché",
        "Quanto", "Quale", "Quali", "Quanti", "Quante",
    }

# fmt: on
