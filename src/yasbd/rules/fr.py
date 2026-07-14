from yasbd.rules.base import Rules


# fmt: off
class FrRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social / Professional
        "m", "a.c.n", "a.m", "ch.-l", "e.v", "me", "mm", "r.p",

        # Noble / Royal / Religious
        "ll.aa", "ll.aa.ii", "ll.aa.rr", "ll.aa.ss", "ll.ee", "ll.mm",
        "ll.mm.ii.rr", "nn.ss", "ll", "aa", "ii", "rr", "ss", "ee",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Publishing / Documents
        "ann", "chap", "coll", "dict", "fasc", "ill", "impr", "introd",
        "ms", "pl", "pref", "suppl", "suiv", "t", "trad",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Annexe", "Chapitre", "Sous-section", "Unité", "Préface",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
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
        "Ce", "Ces", "Cet", "Cette", "Elle", "Elles", "Il",
        "Ils", "Je", "Nous", "On", "Tu", "Vous",

        # Adverbs
        "Actuellement", "Ainsi", "Alors", "Auparavant",
        "Cependant", "Dernier", "Deuxièmement", "Donc",
        "Dorénavant", "Désormais", "Enfin", "Ensuite",
        "Finalement", "Initialement", "Mais", "Néanmoins",
        "Par la suite", "Plus tard", "Premièrement", "Puis",
        "Suivant", "Toutefois", "Troisièmement", "Voici",
        "Voilà",

        # Question words
        "Combien", "Comment", "Où", "Pourquoi", "Qu'", "Quand",
        "Que", "Quel", "Quelle", "Quelles", "Quels", "Qui",

        # Other common starters
        "Est-ce", "Millions",
    }

# fmt: on
