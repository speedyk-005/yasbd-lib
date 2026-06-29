from yasbd.rules.base import Rules


# fmt: off
class SkRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "p", "P", "pani", "sl", "doc",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "S.R", "E.Ú", "O.S.N",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "s", "č", "zv", "vyd", "roč", "čís", "ods", "písm",
        "par", "obr", "obv", "odd", "pok", "pozn",
        "str", "st", "kol", "zn",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Kapitola", "Časť", "Oddiel", "Príloha",
        "Hlava", "Diel", "Odsek",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "napr", "tzv", "t.j", "príp", "resp", "tzn",
        "viď", "cca",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "máj", "jún", "júl",

        # Days
        "ne", "po", "ut", "st", "št", "pi", "so",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Ja", "Ty", "On", "Ona", "Ono",
        "My", "Vy", "Oni", "Ten", "Tá", "To",
        "Tento", "Táto", "Toto", "Tí", "Tie",

        # Adverbs
        "Potom", "Následne", "Medzitým",
        "Najprv", "Nakoniec", "Napokon",
        "Vtedy", "Zrazu", "Znovu", "Dnes",
        "Včera", "Zajtra", "Teraz", "Už", "Ešte",
        "Neskôr",

        # Discourse / transition starters (sentence-level only)
        "Avšak", "Preto", "Teda", "Čiže",
        "Z toho vyplýva", "To znamená",

        # Coordinating sentence starters
        # (only true sentence-initial usage)
        "A", "Ale", "No", "Tak",

        # Question words
        "Kto", "Čo", "Kedy", "Kde", "Prečo", "Ako",
        "Koľko", "Ktorý", "Ktorá", "Ktoré", "Kým", "Či"
    }

# fmt: on
