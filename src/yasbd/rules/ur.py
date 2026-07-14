import re

from yasbd.rules.base import Rules


# fmt: off
class UrRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "ڈاکٹر", "ڈاکٹ", "ڈ", "پروفیسر", "پروف", "پ",
        "انجینئر", "انج",

        # Military, Legal & Administrative
        "جنرل", "کیپٹن", "لفٹیننٹ", "کرنل", "اسپ",
        "ایس.ایچ.او", "ایس.ڈی.او",

        # Religious, Classical Honorific Prefixes
        "حضرت", "مولانا", "مول", "مفتی", "مف",
        "علامہ", "علام", "شیخ", "حکیم", "قاری",
        "حافظ", "سید", "آقا",

        # Social & Formal Address
        "جناب", "محترم", "محترمہ", "صاحب",
        "صاحبہ", "خاتون", "بی بی", "بھائی", "جی",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "ا.م", "و.م.ا", "یو.کے", "یو.ایس.اے", "کے.پی.کے",
        "یو.این", "ڈبلیو.ایچ.او", "آئی.ایم.ایف", "ڈبلیو.ٹی.او",
        "ایف.بی.آر", "سی.آئی.ڈی", "ایف.اے.او",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "ص", "ج", "ش", "ق", "م", "ب", "ط", "خ", "ف", "ن", "ک",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "باب", "فصل", "حصہ", "شق", "پیراگراف",
        "تعارف", "آغاز", "اختتام", "نتیجہ", "فہرست",
        "ضمیمہ", "حوالہ", "حواشی", "اشاریہ", "عنوان",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "آپ", "اس", "ان", "انہوں", "انہیں", "تم", "تو", "جس",
        "جو", "جیسے", "میں", "وہ", "کوئی", "کچھ", "ہم", "یہ",

        # Question Words
        "آیا", "کب", "کتنا", "کس", "کون", "کہاں", "کیا", "کیسے",
        "کیوں",

        # Logical Conjunctions & Connectors
        "بلکه", "کیونکہ", "چنانچہ", "لہذا", "اگرچہ",
        "اس لیے", "بنا بریں", "علاوہ ازیں", "پس", "بقول",
    }

    REPORTING_WORDS = {
        "کہ", "بول", "پوچھ", "لکھ", "سمجھ", "بتا",
        "سمجھا", "جواب", "اعلان", "واضح", "دعویٰ",
        "تصدیق", "اعتراف", "انکار", "کہتے", "بتاتے",
        "پوچھتے", "فرما",
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
