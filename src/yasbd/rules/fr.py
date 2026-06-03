from yasbd.rules.base import Rules


# fmt: off
class FrRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "m", "a.c.n", "a.m", "ch.-l", "e.v", "me", "mm", "r.p",

        # Noble / Royal / Religious
        "ll.aa", "ll.aa.ii", "ll.aa.rr", "ll.aa.ss", "ll.ee", "ll.mm",
        "ll.mm.ii.rr", "nn.ss", "ll", "aa", "ii", "rr", "ss", "ee", "mm",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Publishing / Documents
        "ann", "chap", "coll", "dict", "fasc", "ill", "impr", "introd",
        "ms", "pl", "pref", "suppl", "suiv", "t", "trad",
    }

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {
        # Bridge/connectors
        "c.-à-d", "c-à-d", "c-a-d", "p.ex", "n.b", "p.s", "éts", "sté", "ste",

        # Streets
        "av", "boul", "bd", "ch", "imp", "faub", "fg", "carr", "Pén"
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "janv", "fevr", "févr", "fév", "avr", "juill", "juil", "sept",
        "oct","nov", "déc",

        # Days
        "mer", "jeu", "ven", "sam", "dim",
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Le", "La", "Les", "L'",

        # Pronouns
        "Je", "Tu", "Il", "Elle", "On", "Nous", "Vous", "Ils", "Elles",
        "Ce", "Cet", "Cette", "Ces",

        # Adverbs
        "Mais", "Donc", "Alors", "Cependant", "Toutefois", "Néanmoins",
        "Ainsi", "Puis", "Ensuite", "Voici", "Voilà",

        # Question words
        "Qui", "Que", "Qu'", "Quand", "Où", "Pourquoi", "Comment", "Combien",
        "Quel", "Quelle", "Quels", "Quelles",

        # Other common starters
        "Est-ce", "Millions",
    }

# fmt: on
