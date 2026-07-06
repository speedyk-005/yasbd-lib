from yasbd.rules.base import Rules


# fmt: off
class SwRules(Rules):

    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "b", "n", "bw", "bi", "dkt", "mwl", "mt",
        "mh", "nd", "mhn", "eng", "mj", "kam",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "T.Z", "D.R.C", "U.A.E",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "uk", "sur", "jal", "har", "mf", "t.m", "n.k",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "mf", "m.n", "k.v", "n.k", "k.m", "ya", "taz",
    }

    SECTION_MARKERS = {
        "sura", "sehemu", "kifungu", "mwisho",
        "mlango", "Sura", "Sehemu", "Kiambatisho",
        "Hitimisho", "Utangulizi", "Dibaji",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        "mac", "mei", "ago", "des",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Mimi", "Sisi", "Wewe", "Ninyi", "Yeye", "Wao",
        "Huyu", "Hawa", "Huu", "Hii", "Hiki", "Hivi", "Hili", "Haya",
        "Yule", "Wale", "Ule", "Ile", "Kile", "Vile", "Lile", "Yale",

        # Question Particles
        "Nani", "Nini", "Lini", "Wapi", "Kwanini", "Mbona", "Vipi",

        # Logical Conjunctions & Transitions
        "Kwa", "Kwa sababu", "Lakini", "Ingawa", "Kisha",
        "Halafu", "Basi", "Isipokuwa", "Aidha", "Zaidi",
        "Kwamba", "Hata", "Tena", "Ila", "Bali",
    }

# fmt: on
