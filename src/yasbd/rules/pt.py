from yasbd.rules.base import Rules


# fmt: off
class PtRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "sr", "sra", "srª", "sras", "srta", "d", "dr", "dra", "drª", "drs", "dras",
        "prof", "profa", "profª", "arq", "eng", "enga", "engª", "adv", "lic", "bel",
        "gen", "cel", "cap", "ten", "subten", "cmdte", "cmdt", "me", "ma", "reit",

        # Religious / Formal Honours
        "pe", "dom", "rev", "ir", "irmaos", "exmo", "exma", "exmª",

        # Noble / Royal / Formal Pronouns
        "s.m", "s.m.s", "s.a.r", "s.a.s", "s.s", "s.a", "s.e", "v.e", "v.ex.a",
        "s.ex.a", "v.exª", "s.exª", "v.s.a", "v.sª",
    }

    REFERENCE_ABBRVS = (Rules.REFERENCE_ABBRVS - {"no", "nos", "para"}) | {
        "pág", "pag", "págs", "pags", "núm", "num", "nro", "dir", "t", "tel", "trad",
        "incl", "cia", "vol", "ed", "puj",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Artigo", "Anexo", "Capítulo", "Secção", "Seção", "Subsecção", "Subseção",
        "Unidade", "Módulo", "Divisão",
    }

    INLINE_ONLY_ABBRVS = (Rules.INLINE_ONLY_ABBRVS - {"ave"}) | {
        # Business entity bridges
        "assoc",

        # Bridge / connectors / text notes
        "ex", "p.ex", "vid", "vd", "of",

        # Addresses / Urban transport markers
        "r", "av", "al", "vía", "transv", "bc", "ch", "estr", "pl",
        "pç", "pça", "br", "rs", "sp", "qd", "lt", "urb", "ap", "apt",
        "apto", "bl", "cj", "ed", "edif", "sl", "jd", "m.g",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "E.U.A", "U.E", "P.T", "F.A", "R.H",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months (Portuguese specific updates)
        "fev", "abr", "mai", "ago", "set", "out", "dez",

        # Days (Portuguese specific updates)
        "seg", "ter", "qua", "qui", "sex", "sáb", "sab",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "O", "A", "Os", "As", "Um", "Uma", "Uns", "Unas",

        # Pronouns
        "Eu", "Nós", "Tu", "Você", "Vocês", "Ele", "Ela", "Eles", "Elas",
        "Este", "Esta", "Estes", "Estas", "Esse", "Essa", "Esses", "Essas",
        "Aquele", "Aquela", "Aqueles", "Aquelas", "Isto", "Isso", "Aquilo",
        "Lá", "Ali", "Aqui",

        # Question words
        "Quem", "O que", "Que", "Onde", "Aonde", "Quando", "Por que", "Como",
        "Qual", "Quais", "Cujo", "Cuja",

        # Adverbs
        "Contudo", "Todavia", "Entretanto", "Porém", "Além disso", "Portanto",
        "Assim", "Consequentemente", "Enquanto",
        "Depois", "Então", "Atualmente", "Finalmente", "Inicialmente",
        "Posteriormente", "Seguinte", "Último",
        "Primeiramente", "Primeiro", "Segundo", "Terceiro",
        "Por último", "Antigamente", "Previamente", "Imediatamente",

        # Other common starters
        "Faz", "Fez", "Milhões",
    }

# fmt: on
