from yasbd.rules.base import Rules


# fmt: off
class PlRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic, Medical, and Administrative Titles
        "inż", "lek", "dyr", "hab", "doc",

        # Ecclesiastical and Religious Honorifics
        "ks", "bp", "abp", "św", "kard", "o", "dh",

        # Military and Security Ranks
        "kpt", "płk", "mjr", "sierż", "chor", "ppłk",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "R.P", "P.N.E",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "art", "ust", "par", "ptk", "dz", "poz", "sygn",
        "t", "cz", "rozdz", "wyd", "rys", "tab", "zob",
        "por", "ok", "nr", "nast", "itp", "m.in", "itd",
        "godz", "str", "lp", "tłum",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "np", "tzw", "tj", "tzn", "ww", "b.z", "pt", "jw", "sp",
        "spol", "os", "ul", "al", "pl", "skw", "bulw", "boul",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Rozdział", "Część", "Ustęp", "Paragraf", "Artykuł", "Punkt", "Sekcja",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "sty", "stycz", "lut", "mar", "kwi", "kwiec", "cze", "czerw",
        "lip", "sie", "sierp", "wrz", "wrzes", "paź", "paźdz", "lis",
        "listop", "gru",

        # Days
        "pn", "pon", "wt", "śr", "czw", "pt", "piąt", "sob", "nd", "niedz",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Ja", "Ty", "On", "Ona", "Ono", "My", "Wy",
        "Oni", "One", "Ten", "Ta", "To", "Ci", "Te",

        # Temporal adverbs
        "Potem", "Następnie", "Wtedy", "Nagle", "Teraz",
        "Już", "Później", "Wcześniej", "Następnego",

        # Discourse / transition
        "Jednak", "Zatem", "Więc", "Dlatego", "Mimo",
        "Ponadto", "Dodatkowo", "Poza", "Tymczasem",
        "Wreszcie", "Wobec", "Otóż", "Przykładowo",
        "Z kolei",

        # Coordinating starters
        "Ale", "Lecz", "Natomiast", "Tak", "Nie",

        # Question words
        "Kto", "Co", "Kiedy", "Gdzie", "Dlaczego",
        "Jak", "Ile", "Który", "Która", "Które", "Czyj",
        "Skąd", "Dokąd", "Czemu",
    }

# fmt: on
