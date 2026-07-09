from yasbd.rules.base import Rules


# fmt: off
class CsRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional Titles
        "bc", "bca", "ing", "arch", "doc",

        # Rigorózní & Professional Doctorates
        "judr", "mudr", "mvdr", "phdr", "rndr", "thdr", "paeddr", "ak",

        # Military, Administrative, and Corporate
        "p", "pí", "fa", "plk", "mjr", "kpt", "por", "npor",

        # Ecclesiastical and Religious Honorifics
        "o", "br", "sr", "th", "sv",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "Č.R", "Č.S.R", "P.N.E", "N.E",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout, Citations & Document Hierarchy
        "odst", "par", "čl", "č", "čj", "s", "str",
        "vyd", "sv", "t", "kap", "obr", "graf",
        "zob", "porov", "pozn", "písm", "roč",
        "hod",

        # Legal Reference Identifiers
        "zák", "nař", "usn", "vyhl", "pol", "pov", "pod",

        # List Terminators
        "apod", "a pod", "a j", "aj", "atp",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Discourse & Syntactic Coordinators
        "např", "tj", "tzn", "tzv", "resp", "cca",
        "zejm", "př", "popř", "příp", "r", "ev",
        "č.p", "č.ev",

        # Urban & Address Identifiers
        "ul", "tř", "nám", "nábř",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitola", "Část", "Sekce", "Odstavec", "Bod",
        "Hlava", "Oddíl", "Článek", "Paragraf", "Písmeno",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "led", "ún", "únor", "bře", "břez", "dub", "kvě", "čvn", "červ",
        "čvc", "čec", "srp", "zář", "říj", "lis", "list", "pro", "pros",

        # Days
        "po", "út", "st", "čt", "pá", "so", "ne",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Já", "Ty", "On", "Ona", "Ono", "My",
        "Vy", "Oni", "Ony", "One", "Ten",
        "Ta", "To", "Ti", "Tento", "Tato",
        "Toto", "Tito", "Tyto", "Onen", "Onače",

        # Discourse, Transition & Logic Modifiers
        "Proto", "Přesto", "Navíc", "Mezitím",
        "Naopak", "Totiž", "Zkrátka","Především",
        "Však", "Avšak", "Tedy", "Protože",
        "Kromě", "Ovšem", "Například",
        "Jinak", "Tudíž", "Takže",

        # Coordinating Starters & Particles
        "Ale", "Nicméně", "Jenže", "Nebo", "Ani",
        "Vždyť", "Přece", "Ano", "Ne", "Prosím",
        "Děkuji", "Promiňte",

        # Question Words / Relative Modifiers
        "Kdo", "Co", "Kdy", "Kde", "Proč",
        "Jak", "Kolik", "Který", "Která", "Které",
        "Čí", "Odkud", "Kam", "Čím",
    }

# fmt: on
