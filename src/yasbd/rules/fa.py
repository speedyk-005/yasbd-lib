import re

from yasbd.rules.base import Rules


# fmt: off
class FaRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "آقا", "سید", "حاج", "شیخ", "ناو",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "ا.م.ا", "س.ا.ا", "ص.ا.ا", "و.م", "ج.ا.ا", "ن.ا.ت.و",
        "س.م.م", "ک.و.آ.ر",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "ص", "ج", "ش", "ق", "م", "ب", "ط", "خ", "ف", "ض", "ت", "ن",
        "ک", "س", "ه",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "فصل", "فصلنامه", "بخش", "قسمت", "گفتار", "ماده", "بند",
        "تبصره", "ضمیمه", "پیوست", "مقدمه", "دیباچه", "خاتمه",
        "نتیجه", "کتاب", "جلد", "مقاله", "طرح", "الزام",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "م.م", "ر.ک", "بن", "ص.م", "ع.م", "ق.م", "ب.م",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Days (Rarely abbreviated,
        # but initial letters sometimes appear)
        "ش", "ی", "د", "س", "چ", "پ", "ج",

        # Months (almost never abbreviated with periods in Persian)
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "آن", "او", "ایشان", "این", "تو", "شما", "ما", "من",
        "همان", "همین",

        # Question words
        "کی", "چه", "کجا", "چرا", "چگونه", "چطور", "کدام", "آیا",

        # Adverbs & connectors
        "ابتدا", "البته", "اما", "اول", "بااین‌حال",
        "برای مثال", "بعد", "بعداً", "بنابراین", "به‌عنوان",
        "در نتیجه", "در نهایت", "زیرا", "سرانجام", "سپس",
        "علاوه", "عموماً", "لیکن", "مثلاً", "نخست", "نهایتاً",
        "همچنین", "ولی", "پس", "چراکه", "چون",
    }

    REPORTING_WORDS = {
        "اشاره کرد", "اضافه کرد", "اعلام داشت", "اعلام کرد",
        "افزود", "افزودند", "بیان داشت", "بیان کرد",
        "تأکید داشت", "تأکید کرد", "تصریح کرد", "می‌نویسد",
        "می‌پرسد", "می‌گوید", "می‌گویند", "نوشت", "پاسخ داد",
        "پرسید", "گفت", "گفتند",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis and numerical sections."""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Never split after hierarchical section numbers.
            re.compile(r"\d+(?:٫\d+)+\."),

            # Never split after ellipsis (ASCII, Unicode).
            re.compile(rf"{cls.DOTS_PATTERN}{{3,}}|\u2026"),
        ])
