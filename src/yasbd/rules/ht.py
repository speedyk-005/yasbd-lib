from yasbd.rules.base import Rules


# fmt: off
class HtRules(Rules):


    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {"sek"} - {"ex", "exs", "tab"}
    DATE_ABBRVS = Rules.DATE_ABBRVS | {"okt", "fev", "des"}

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Chapit", "Pati", "Seksyon", "Atik", "Inite", "Modil", "Divizyon"
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Mwen", "Nou", "Ou", "Li", "Yo", "Sa", "Sila",

        # Question words
        "Ki kote", "Ki lè", "Kibo", "Kibò", "Kijan", "Kikote",
        "Kile", "Kilè", "Kimoun", "Kisa", "Kiyes", "Kiyès",
        "Koman", "Kouman", "Kòman", "Pou kiyes", "Pou kiyès",
        "Poukisa", "Poukiyes", "Poukiyès",

        # Adverbs
        "Anplis", "Antretan", "Anvan", "Apre", "Denye", "Donk",
        "Epitou", "Finalman", "Kidonk", "Kounye a", "Lè", "Men",
        "Okòmansman", "Otreman", "Pa konsekan", "Pakonsekan",
        "Pandan se tan", "Pandansetan", "Pita", "Poutan",
        "Premye", "Sepandan", "Sinon",

        # Other common starters
        "Yon", "Eske", "Èske",
    }

# fmt: on
