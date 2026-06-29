import re

from yasbd.rules.base import Rules


# fmt: off
class FaRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Social titles
        "آقا", "خانم", "جناب", "سرکار",

        # Academic & Professional
        "دکتر", "مهندس", "استاد", "پروفسور", "وکیل", "قاضی",

        # Religious
        "آیت‌الله", "حجت‌الاسلام", "سید", "حاجی", "حاج", "شیخ", "آخوند",

        # Military
        "سرتیپ", "سرلشکر", "سپهبد", "سرهنگ", "سرهنگ‌دوم",
        "سرگرد", "سروان", "ستوان", "استوار", "ناو", "ناخدا",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "ا.م.ا", "س.ا.ا", "ص.ا.ا", "و.م", "ج.ا.ا", "ن.ا.ت.و",
        "س.م.م", "ک.و.آ.ر",
    }

    REFERENCE_ABBRVS = {
        "ص", "ج", "ش", "ق", "م", "ب", "ط", "خ",
        "ف", "ض", "ت", "ن", "ک", "س", "ه",
        "انظر", "قارن",
    }

    SECTION_MARKERS = {
        "فصل", "فصلنامه", "بخش", "قسمت", "گفتار",
        "ماده", "بند", "تبصره", "ضمیمه", "پیوست",
        "مقدمه", "دیباچه", "خاتمه", "نتیجه",
        "کتاب", "جلد", "مقاله", "طرح", "الزام",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "م.م", "ر.ک", "بن", "همان", "ص.م", "ع.م",
        "ق.م", "ب.م",
    }

    DATE_ABBRVS = {
        # Days (Rarely abbreviated,
        # but initial letters sometimes appear)
        "ش", "ی", "د", "س", "چ", "پ", "ج",

        # Months (almost never abbreviated with periods in Persian)
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "من", "تو", "او", "ما", "شما", "ایشان",
        "این", "آن", "همین", "همان",

        # Question words
        "کی", "چه", "کجا", "چرا", "چگونه", "چطور", "کدام",
        "آیا",

        # Adverbs & connectors
        "اما", "ولی", "لیکن", "بااین‌حال",
        "زیرا", "چراکه", "چون",
        "بنابراین", "پس", "سپس", "در نتیجه",
        "مثلاً", "برای مثال",
        "ابتدا", "اول", "نخست",
        "بعد", "بعداً",
        "سرانجام", "نهایتاً", "در نهایت",
        "همچنین", "علاوه", "به‌عنوان",
        "البته", "عموماً",
    }

    REPORTING_WORDS = {
        "گفت", "گفتند", "می‌گوید", "می‌گویند",
        "افزود", "افزودند", "اضافه کرد", "اعلام کرد",
         "اعلام داشت", "تأکید کرد", "تأکید داشت",
        "بیان کرد", "بیان داشت", "تصریح کرد",
        "اشاره کرد", "نوشت", "می‌نویسد", "پرسید",
        "می‌پرسد", "پاسخ داد",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis protection."""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST.append(
            # Never split after ellipsis (ASCII, Unicode)
            re.compile(rf"{cls.DOTS_PATTERN}{{3,}}|\u2026")
        )
