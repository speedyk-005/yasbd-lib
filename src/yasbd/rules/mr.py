from yasbd.rules.hi import HiRules


# fmt: off
class MrRules(HiRules):


    TITLE_ABBRVS = (HiRules.TITLE_ABBRVS - {"ले"}) | {
        "सौ",
    }

    DOTTED_GEOPOL_ABBRVS = HiRules.DOTTED_GEOPOL_ABBRVS | {
        "म.रा", "भा.रा",
    }

    REFERENCE_ABBRVS = HiRules.REFERENCE_ABBRVS | {
        "मुखपृ", "संद", "पान", "अध्य", "आदेश",
    }

    INLINE_ONLY_ABBRVS = HiRules.INLINE_ONLY_ABBRVS | {
        "बनाम", "जि",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "आपण", "आम्ही", "तिने", "ती", "तुम्ही", "तू", "ते",
        "तो", "त्या", "त्यांनी", "त्यानं", "त्याने", "मी", "या",
        "हा", "हि", "ही", "हे",

        # Question words
        "कशी", "कसा", "कसे", "का", "काय", "किती", "कुठे",
        "केव्हा", "कोण",

        # Adverbs & logical connectors
        "अखेर", "आज", "आता", "उद्या", "कारण", "काल", "तथापि",
        "तरी", "त्यामुळे", "नंतर", "पण", "प्रथम", "मात्र",
        "म्हणून", "शेवटी", "सर्वप्रथम",
    }

    REPORTING_WORDS = {
        # Reporting verb roots (stripped of tense/gender suffixes)
        "आज्ञा", "उत्तर", "ओरड", "कुजबुज", "घोषित", "पुन्हा",
        "बोल", "म्हण", "लिही", "विचार", "विनंती", "सांग",
        "सुचव", "हाक",
    }

# fmt: on
