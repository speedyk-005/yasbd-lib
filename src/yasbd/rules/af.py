from yasbd.rules.nl import NlRules


# fmt: off
class AfRules(NlRules):

    TITLE_ABBRVS = NlRules.TITLE_ABBRVS | {
        "adv", "ds", "at", "mej", "me",
    }

    DOTTED_GEOPOL_ABBRVS = NlRules.DOTTED_GEOPOL_ABBRVS | {
        "V.S.A", "R.S.A", "S.A"
    }

    REFERENCE_ABBRVS = NlRules.REFERENCE_ABBRVS | {
        # Bibliographical, Document, and Page References
        "bl", "a.w", "bg", "samest", "uitg", "byl", "red", "hers",

        # Unique Afrikaans legal and cross-referencing markers
        "kol", "vg", "verg", "hfst"
    }

    SECTION_MARKERS = NlRules.SECTION_MARKERS | {
        "Hoofstuk", "Bylae", "Opsomming", "Gevolgtrekking"
    }

    INLINE_ONLY_ABBRVS = NlRules.INLINE_ONLY_ABBRVS | {
        "d.w.s", "o.a", "m.a.w", "m.m.v", "i.v.m", "n.v.t",
        "v.C", "n.C", "v.m", "n.m",
    }

    DATE_ABBRVS = NlRules.DATE_ABBRVS | {
        # 'dec' becomes 'des' for Desember;
        # 'vry' ensures safe Vrydag tracking
        "des", "vry"
    }

    COMMON_SENT_STARTERS = NlRules.COMMON_SENT_STARTERS | {
        # Unique Afrikaans Articles & Pronouns
        "Die", "'n", "Ek", "Ons", "Jy", "Sy", "Hulle", "Hierdie", "Daardie",
        "Dié", "Sulke", "Mens",

        # Unique Afrikaans Question/Connector Anchors
        "Watter", "Boonop", "Gevolglik", "Inteendeel", "Daarbenewens", "Daarteenoor",

        # Sequence/Time Variations
        "Eerstens", "Tweedens", "Gister", "Môre", "Dikwels",
    }

    DATE_WORDS = {
        # Months
        "januarie", "februarie", "maart", "april", "mei", "junie",
        "julie", "augustus", "september", "oktober", "november", "desember",

        # Days
        "maandag", "dinsdag", "woensdag", "donderdag", "vrydag",
        "saterdag", "sondag",
     }

# fmt: on
