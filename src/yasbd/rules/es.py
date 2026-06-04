import regex as re2

from yasbd.rules.base import Rules, _build_abbr_pattern


# fmt: off
class EsRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "sr", "sra", "srta", "d", "dña", "dra", "lic", "gral",
        "pdte", "profe", "profa", "arq", "abg", "cnel", "cap", "cmdte", "mag", "lcdo",
        "hno", "hnos", "pbro", "tte", "subtte",

        # Noble / Royal
        "s.m", "ss.mm", "s.a.r", "ss.aa.rr", "s.a.s", "s.s", "s.a",
        "ss.aa", "s.e", "v.e", "s.à.s.r", "aa", "mm", "rr", "ss",
    }

    REFERENCE_ABBRVS = (Rules.REFERENCE_ABBRVS - {"no", "nos", "para"}) | {
        "pág", "núm", "nro", "dir", "t", "tel", "trad", "asoc", "aprox",
        "cf", "incl", "cía", "s",
    }

    HEADING_TOKENS = Rules.HEADING_TOKENS | {
    "Artículo", "Anexo", "Capítulo", "Sección", "Subsección", "Unidad",
    "Módulo", "División",
    }

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS - {"ave"} | {
        "ej", "p.ej", "vid", "cll", "cra", "diag", "transv", "mz", "mza", "lt",
        "urb", "asent", "dpto", "prov", "mnpio", "conj", "edif", "ofic", "km",
        "av", "avd", "c", "pso", "ctra", "pl", "blvr",
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {
        "EE.UU", "FF.AA", "RR.HH", "CC.AA", "EE", "UU", "FF", "RR", "HH", "AA",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "ene", "abr", "may", "ago", "dic", "lun" , "mar" ,"mié", "miér",
        "jue", "vie", "sáb", "dom",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas",

        # Pronouns
        "Yo", "Tú", "Él", "Ella", "Usted", "Nosotros", "Vosotros",
        "Ellos", "Ellas", "Este", "Esta", "Estos", "Estas",
        "Ese", "Esa", "Esos", "Esas",
        "Aquel", "Aquella", "Aquellos", "Aquellas", "Aquí", "Allí",
        "Quien", "Quienes", "Cual", "Cuales", "Cuanto",

        # Inverted punctuation (always start a new sentence in Spanish)
        "¿", "¡",

        # Adverbs & Transitions
        "Pero", "Entonces", "Así que", "Sin embargo", "Luego", "Además",
        "Aunque", "Tampoco", "También", "Incluso", "Solo", "Solamente",
        "Más", "Menos", "Mejor", "Peor", "Mientras", "Ahora", "Después",
        "Antes", "Temprano", "Tarde", "Pronto", "Siempre", "Nunca", "Jamás",
        "Ya", "Aún", "Todavía", "Ayer", "Hoy", "Mañana", "Anoche",
        "Quizás", "Quizá", "Tal vez", "Ojalá", "Casi",
        "Finalmente", "Generalmente", "Normalmente", "Realmente",
        "Seguramente", "Probablemente", "Lamentablemente", "Afortunadamente",

        # Prepositions & Interrogatives
        "Por", "Para", "Como", "Cuando", "Donde", "De", "Desde", "Durante",
        "En", "Entre", "Hacia", "Hasta", "Mediante", "Según", "Sin", "Con",
        "Sobre", "Tras", "Qué", "Quién", "Cuál", "Cuánto", "Cómo", "Cuándo",
        "Dónde", "Porqué", "Porque",

        # Verbs / auxiliaries
        "Es", "Son", "Era", "Eran", "Fue", "Fueron", "Hay", "Tiene",
        "Tienen", "Está", "Están", "Había", "Hubo", "Estaba", "Estuvo",
    }
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix pronouns abbrvs behavior."""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()


        # Ud./Uds./Vd./Vds. heuristic
        # Don't split if the next word is NOT a common starter (assumes it's a proper name).
        # Resolves the ambiguity "Ud. Marco" vs "Ud. Mañana".
        pronoun_abbrvs_pattern = _build_abbr_pattern({"ud", "uds", "vd", "vds"})

        cls.MID_SENTENCE_FINDER_LST.append(
            re2.compile(rf"""
                \b(?i:{pronoun_abbrvs_pattern})\.
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
            """, re2.X)
        )

# fmt: on
