import re

from yasbd.rules.base import Rules


# fmt: off
class ArRules(Rules):

    # Arabic uses a reversed question mark (؟) alongside standard terminators.
    TERMINATORS = Rules.TERMINATORS | {"؟"}

    TITLE_ABBRVS = {
        # Academic & Professional
        "أ", "د", "أ.د", "م", "أ.م", "د.م", "ط", "ص", "باحث",
        
        # Military, Legal & Administrative
        "لو", "عم", "عق", "مقد", "رائد", "نق", "لـو", "عـم",
        "ستشار", "ق", "ر.م", "س", "س.س", "م.ع", "م.م", "م.ع.م",
        
        # Religious & Classical Honorifics
        "ص", "ع", "ر", "ق", "ج", "ط.ع", "ب.ع", "ح", "أب", "مطران", "نّيافة",
        
        # Social & Formal Address
        "أ", "سـم", "معالي", "دولة"
    }

    GEOPOLITICAL_ABBRVS = Rules.GEOPOLITICAL_ABBRVS | {
        "و.م.أ", "و.م.أ", "المملكة.المتحدة", "الاتحاد.الأوروبي",
        "أ.م", "الاتحاد.السوفيتي",
        "الإمارات", "ج.ص.ش", "كوريا.الجنوبية"
    }

    REFERENCE_ABBRVS = {
        "ص", "ج", "مج", "ت", "ط", "ع", "ب", "ح", "خ", "ف", "ق", "ن", "انظر", "قارن"
    }

    HEADING_TOKENS = {
        "فصل", "الفصل", "باب", "الباب", "جزء", "الجزء", "قسم", "القسم",
        "مادة", "المادة", "بند", "البند", "مقدمة", "المقدمة", "تمهيد", "التمهيد",
        "خاتمة", "الخاتمة", "كتاب", "الكتاب", "ملحق", "الملحق", "فهرس", "الفهرس",
        "المبحث", "المطلب", "المسألة"
    }

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {
        # Calendar & Time Eras
        "هـ", "م", "ق.م", "ب.م", "ش", "س", "د",
        
        # Location & General
        "ص.ب", "ت.إ", "إلخ", "ت.ف", "ت"
    }

    DATE_ABBRVS = {
        # Days (Rarely abbreviated, but initial letters sometimes appear in schedules)
        "ح", "ن", "ث", "ر", "خ", "ج", "س",
        
        # Months (Almost never abbreviated with periods; full names are always preferred)
    }

    COMMON_SENT_STARTERS = {
        # Transitions & Adversatives (However, Yet, While)
        "ولكن", "بيد", "غير", "إلا", "بينما", 

        # Contextual Markers (Since, Given that)
        "حيث", "علماً", "منذ", 

        # Logical Payouts (Therefore, Consequently, For example)
        "بناءً", "لذلك", "وبالتالي", "نتيجة", "مثلاً", "عموماً"
    }

    CASE_MARKERS = {"بـ", "لـ", "كـ", "فـ", "وـ"}

    REPORTING_WORDS = {
        "قال", "تقول", "يقول", "قالوا", "قلت",
        "صرح", "يصرح", "صرحت", "مصرح", "مصرحا",
        "أضاف", "يضيف", "تضيف", "أضافت", "مضاف",
        "أكد", "يؤكد", "أكدت", "مؤكد", "مؤكدا",
        "أوضح", "يوضح", "أوضحت", "موضح", "موضحا",
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis protection."""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST.append(
            # Never split after ellipsis
            re.compile(r"\.{3,}")
        )
# fmt: on
