from yasbd.rules.base import Rules


# fmt: off
class HtRules(Rules):
    ISO_CODE = "ht"


    # HT always uses full words (e.g., lame ameriken), never dot-abbreviated forms
    GEOPOLITICAL_ABBRVS = set()
    COMMON_ORG_NOUNS = set()

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {"sek"} - {"ex", "exs", "tab"}
    DATE_ABBRVS = Rules.DATE_ABBRVS | {"okt",}

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Mwen", "Nou", "Ou", "Li", "Yo", "Sa", "Sila",

        # Question words
        "Kiyes", "Kiyès", "Kimoun", "Kisa", "Kikote", "Ki kote", "Kibo",
        "Kibò", "Kile", "Kilè", "Ki lè", "Poukisa", "Kijan", "Koman",
        "Kòman", "Kouman", "Poukiyes", "Poukiyès", "Pou kiyes", "Pou kiyès",

        # Adverbs
        "Poutan", "Sepandan", "Anplis", "Epitou", "Men", "Sinon", "Otreman",
        "Kidonk", "Donk", "Antretan", "Pakonsekan", "Pa konsekan",
        "Pandan se tan", "Pandansetan",

        # Other common starters
        "Yon", "Eske", "Èske",
    }

# fmt: on
