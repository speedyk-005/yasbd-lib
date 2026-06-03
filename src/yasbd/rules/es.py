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

    STREET_ABBRVS = set()

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {
        "ej", "p.ej", "vid", "cll", "cra", "diag", "transv", "mz", "mza", "lt",
        "urb", "asent", "dpto", "prov", "mnpio", "conj", "edif", "ofic", "km",
        "av", "avd", "c", "pso", "ctra", "pl", "blvr",
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {
        "ee.uu", "ff.aa", "rr.hh", "cc.aa", "ee", "uu", "ff", "rr", "hh", "aa",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "ene", "abr", "may", "ago", "dic", "lun" , "mar" ,"mié", "miér",
        "jue", "vie", "sáb", "dom",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "El", "La", "Los", "Las", "Un", "Una", "Unos", "Unas",

        # Pronouns
        "Yo", "Tú", "Él", "Ella", "Usted", "Nosotros", "Vosotros", "Ellos",
        "Ellas", "Aquel", "Aquél", "Aquella", "Aquello", "Aquellas",
        "Aquellos", "Este", "Esta", "Estos", "Estas", "Ese", "Esa", "Esos",
        "Esas", "Aquí", "Allí", "Quien", "Quienes", "Cual", "Cuales", "Cuanto",

        # Adverbs & Transitions (crucial for Ud. heuristic robustness)
        "Pero", "Entonces", "Así que", "Asi que", "Sin embargo", "Luego", "Además", "Aunque",
        "Afortunadamente", "Desafortunadamente", "Lamentablemente", "Felizmente", "Tristemente",
        "Sinceramente", "Atentamente", "Posiblemente", "Probablemente", "Seguramente",
        "Evidentemente", "Obviamente", "Claramente", "Efectivamente", "Realmente",
        "Verdaderamente", "Francamente", "Principalmente", "Generalmente", "Normalmente",
        "Especialmente", "Particularmente", "Finalmente", "Inicialmente", "Anteriormente",
        "Posteriormente", "Últimamente", "Recientemente", "Actualmente", "Brevemente",
        "Curiosamente", "Increíblemente", "Sorprendentemente", "Casualmente", "Aparentemente",
        "Supuestamente", "Teóricamente", "Básicamente", "Fundamentalmente", "Técnicamente",
        "Prácticamente", "Literalmente", "Exactamente", "Precisamente", "Inmediatamente",
        "Rápidamente", "Lentamente", "Súbitamente", "Repentinamente", "Inesperadamente",
        "Constantemente", "Frecuentemente", "Ocasionalmente", "Raramente", "Apenas",
        "Bastante", "Demasiado", "Mucho", "Poco", "Muy", "Tan", "Tanto", "Más", "Menos",
        "Mejor", "Peor", "Igual", "Diferente", "Aparte", "Incluso", "También", "Tampoco",
        "Sino", "Solo", "Solamente", "Únicamente", "Exclusivamente", "Inclusive", "Salvo",
        "Excepto", "Mientras", "Entretanto", "Ahora", "Después", "Antes", "Temprano", "Tarde",
        "Pronto", "Aún", "Todavía", "Ya", "Nunca", "Jamás", "Siempre", "Ayer", "Hoy", "Mañana",
        "Anoche", "Anteayer", "Quizás", "Quizas", "Quizá", "Tal vez", "Ojalá", "Casi",

        # Prepositions & Interrogatives
        "¿", "¡", "Por", "Para", "Como", "Cuando", "Donde", "A", "Ante", "Bajo", "Cabe",
        "Con", "Contra", "De", "Desde", "Durante", "En", "Entre", "Hacia", "Hasta",
        "Mediante", "Según", "Sin", "So", "Sobre", "Tras", "Vía", "Versus",
        "Qué", "Quién", "Cuál", "Cuánto", "Cómo", "Cuándo", "Dónde", "Porqué", "Porque",

        # Verbs and auxiliaries
        "Es", "Son", "Era", "Eran", "Fue", "Fueron", "Hay", "Tiene", "Tienen", "Está", "Están",
        "Había", "Habían", "Hubo", "Hubieron", "Estaba", "Estaban", "Estuvo", "Estuvieron", "Estuviera", "Estuvieran",

    }
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix Spanish ellipsis behavior."""
        # 1. Let the base class build the default rules first
        super()._compile_regex_dynamically()

        import regex as re2

        # 2. Heurística para Ud./Uds./Vd./Vds.
        # No cortar si la siguiente palabra NO es un starter común (asumimos nombre propio).
        # Esto soluciona la ambigüedad "Ud. Marco" vs "Ud. Mañana".
        pronoun_abbrvs_pattern = _build_abbr_pattern({"ud", "uds", "vd", "vds"})
        common_starters_pattern = _build_abbr_pattern(cls.COMMON_SENT_STARTERS)
        dots_pattern = r"[.．]"

        cls.MID_SENTENCE_FINDER_LST.append(
            re2.compile(rf"""
                \b(?i:{pronoun_abbrvs_pattern}){dots_pattern}
                (?!\s+(?:{common_starters_pattern})\b)
            """, re2.X)
        )

# fmt: on
