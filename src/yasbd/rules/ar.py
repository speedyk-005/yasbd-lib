import re

from yasbd.rules.base import Rules


# fmt: off
class ArRules(Rules):

    TITLE_ABBRVS = {
        # Academic & Professional
        "أ", "د", "أ.د", "م", "أ.م", "د.م", "ط", "ص", "باحث",

        # Military, Legal & Administrative
        "لو", "عم", "عق", "مقد", "رائد", "نق", "لـو", "عـم",
        "ستشار", "ق", "ر.م", "س", "س.س", "م.ع", "م.م", "م.ع.م",

        # Religious & Classical Honorifics
        "ع", "ر", "ج", "ط.ع", "ب.ع", "ح", "أب", "مطران", "نّيافة",

        # Social & Formal Address
        "سـم", "معالي", "دولة"
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "و.م.أ", "المملكة.المتحدة", "الاتحاد.الأوروبي",
        "أ.م", "الاتحاد.السوفيتي",
        "الإمارات", "ج.ص.ش", "كوريا.الجنوبية"
    }

    REFERENCE_ABBRVS = {
        "ص", "ج", "مج", "ت", "ط", "ع", "ب", "ح", "خ", "ف", "ق", "ن", "انظر", "قارن"
    }

    SECTION_MARKERS = {
        "فصل", "الفصل", "باب", "الباب", "جزء", "الجزء", "قسم", "القسم",
        "مادة", "المادة", "بند", "البند", "مقدمة", "المقدمة", "تمهيد", "التمهيد",
        "خاتمة", "الخاتمة", "كتاب", "الكتاب", "ملحق", "الملحق", "فهرس", "الفهرس",
        "المبحث", "المطلب", "المسألة"
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
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
        # Pronouns
        "هو", "هي", "هم", "هن", "أنا", "نحن",
        "أنت", "أنتم", "أنتما",
        "هذا", "هذه", "ذلك", "تلك",

        # Question words
        "هل", "ماذا", "ما", "من", "أين", "لماذا",
        "كيف", "أي", "متى", "كم",

        # Adverbs & connectors
        "لكن", "ولكن", "بيد", "غير", "إلا", "بينما",
        "حيث", "علماً", "منذ",
        "بناءً", "لذلك", "وبالتالي", "نتيجة",
        "مثلاً", "عموماً",
        "ثم", "بعد", "لاحقاً", "أخيراً",
        "أولاً", "ثانياً", "ثالثاً",
    }

    REPORTING_WORDS = {
        "قال", "تقول", "يقول", "قالوا", "قلت",
        "صرح", "يصرح", "صرحت", "مصرح", "مصرحا",
        "أضاف", "يضيف", "تضيف", "أضافت", "مضاف",
        "أكد", "يؤكد", "أكدت", "مؤكد", "مؤكدا",
        "أوضح", "يوضح", "أوضحت", "موضح", "موضحا",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis protection."""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST.append(
            # Never split after ellipsis (ASCII, Unicode, full-width)
            re.compile(rf"{cls.DOTS_PATTERN}{{3,}}|\u2026")
        )
