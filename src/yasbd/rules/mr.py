from yasbd.rules.hi import HiRules


# fmt: off
class MrRules(HiRules):


    TITLE_ABBRVS = (HiRules.TITLE_ABBRVS - {"ले"}) | {
        "सौ",
    }

    DOTTED_GEOPOL_ABBRVS = HiRules.DOTTED_GEOPOL_ABBRVS | {
        # Marathi state and administrative reference
        "म.रा", "भा.रा",
    }

    REFERENCE_ABBRVS = HiRules.REFERENCE_ABBRVS | {
        "मुखपृ", "संद", "पान", "अध्य", "प्रकरण", "कलम",
        "उपकलम", "आदेश", "अधिनियम", "परिपत्रक",
    }

    INLINE_ONLY_ABBRVS = HiRules.INLINE_ONLY_ABBRVS | {
        "बनाम", "जि",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "मी", "आम्ही", "आपण", "तू", "तुम्ही", "तो", "ती", "ते", "त्या",
        "हे", "ही", "हा", "हि", "या", "त्याने", "त्यांनी", "तिने", "त्यानं",

        # Question words
        "कोण", "काय", "कुठे", "केव्हा", "का", "कसे", "कसा", "कशी", "किती",

        # Adverbs & logical connectors
        "पण", "मात्र", "तरी", "कारण", "म्हणून", "आता", "नंतर", "आज", "उद्या",
        "काल", "शेवटी", "अखेर", "प्रथम", "सर्वप्रथम", "त्यामुळे", "तथापि",
    }

    REPORTING_WORDS = {
        # Reporting verb roots (stripped of tense/gender suffixes)
        "म्हण", "बोल", "विचार", "सांग", "लिही", "उत्तर", "ओरड", "हाक",
        "कुजबुज", "पुन्हा", "सुचव", "विनंती", "आज्ञा", "घोषित",
    }

# fmt: on
