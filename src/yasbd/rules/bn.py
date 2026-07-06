import regex as re

from yasbd.rules.base import Rules


# fmt: off
class BnRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "ড", "ডা", "প্র", "প্রফ", "অধ্যা", "ইঞ্জি", "বৈদ্য",

        # Military, Legal, Administrative & Political
        "ক্যাপ্ট", "লে", "সচি", "অধি", "পরি", "ব্যা",

        # Religious, Classical & Cultural Honorifics
        "শ্রী", "পণ্ড", "মুফ", "মাউ",

        # Social & Formal Address
        "জনাব", "মো", "মোঃ", "মুহম্মদ", "মোছা",
        "মি", "মিস", "কু", "সু",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        # Native Political, Administrative & Security Entities
        "বি.এন.পি", "আ.লীগ", "ইউ.পি", "জা.দল", "রা.সে.সং", "বি.জি.বি", "সি.আই.ডি",

        # Transliterated Geopolitical Countries & Regions
        "বি.ডি", "ইউ.এস", "ইউ.এস.এ", "ইউ.কে", "ই.ইউ", "ইউ.এ.ই", "ইউ.এস.এস.আর",

        # Transliterated International Organizations
        "ইউ.এন", "ডব্লিউ.এইচ.ও", "আই.এম.开放", "আই.এম.এফ", "ডব্লিউ.টি.ও",
        "এফ.এ.ও", "আই.এ.ই.এ", "ডব্লিউ.বি", "এ.ইউ", "ও.এ.এস",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Layout, Citations, Volume & Document Hierarchies
        "পৃ", "চি", "ভা", "অনু", "অধ", "অধ্যা", "প্যারা", "ক্র", "নং", "ক্র.নং",
        "পরি", "সম্পা", "অনুবা", "প্রকা", "সার", "বিব", "তা", "সূ", "সূচ",

        # Legal, Legislative & Statutory Code Subsections
        "ধা", "উ.ধা", "নি", "আদে", "আবে", "প্রক",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "উদা", "দ্র", "তুল", "টী", "বনাম", "লি", "কো",
        "কোম্পানি", "ভা", "চৌ", "জি",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "আমি", "আমরা", "তুমি", "তোমরা", "আপনি", "আপনারা", "সে", "তারা",
        "তিনি", "তাঁরা", "এটি", "ইহা", "ওটা", "যিনি", "যারা", "যাহা",

        # Question words
        "কে", "কী", "কখন", "কোথায়", "কেন", "কিভাবে", "কত", "কোনটি",

        # Adverbs, Logic, and Transitions
        "কিন্তু", "তবে", "যদিও", "সুতরাং", "অতএব", "কারণ", "তাই", "তদনুসারে",
        "বর্তমানে", "আজ", "অবশেষে", "তাছাড়া", "অন্যথায়", "আসলে", "বিশেষ করে",
        "পরিশেষে", "বস্তুত", "যেমন"
    }

    REPORTING_WORDS = {
        # Base Verb Stems
        "বল", "কহ", "জিজ্ঞেস", "জানা", "লিখ", "বুঝ", "বুঝা",

        # Nominal / Adjectival Components of Conjunct Verbs
        "উত্তর", "জবাব", "আদেশ", "আজ্ঞা", "পরামর্শ",
        "উপদেশ", "ঘোষণা", "এলান", "মন্তব্য", "স্বীকার",
        "দাবি", "চিৎকার", "ফিসফিস"
    }

    REPORTING_WORDS = {
        # Pure Verb Roots / Base Forms
        "বল", "কহ", "জিজ্ঞেস", "জানা", "লিখ", "বুঝ", "বুঝা", "ডাক",

        # Nominal / Adjectival Components of Conjunct Verbs
        "উত্তর", "জবাব", "আদেশ", "আজ্ঞা", "পরামর্শ", "উপদেশ",
        "ঘোষণা", "এলান", "মন্তব্য", "স্বীকার", "দাবি", "চিৎকার",
        "ফিসফিস", "তর্জন", "দোহাই"
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix ellipsis, geopol and dot+space splits"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Ellipsis
            re.compile(r"\.{3,}"),

            # Terminators + no space = initialism/acronyms
            re.compile(r"\.(?!\s)"),

            # Geopolitical abbreviations
            re.compile(rf"(?<={cls.DOTTED_GEOPOL_ABBRVS_PATTERN})\.")
        ])
