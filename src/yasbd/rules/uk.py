from yasbd.rules.ru import RuRules


# fmt: off
class UkRules(RuRules):


    TITLE_ABBRVS = RuRules.TITLE_ABBRVS | {
        "пан", "пані", "панна", "підп", "асист", "інж",
        "в.о", "уклад", "упоряд",
    }

    REFERENCE_ABBRVS = RuRules.REFERENCE_ABBRVS | {
        "перекл", "передм", "вид", "покажч",
        "уклад", "часоп", "розд", "дод",
    }

    SECTION_MARKERS = RuRules.SECTION_MARKERS | {
        "Розділ", "Частина", "Додаток", "Вступ", "Висновок",
    }

    INLINE_ONLY_ABBRVS = RuRules.INLINE_ONLY_ABBRVS | {
        # General inline
        "тобто", "зокр", "згідно", "включ", "у т.ч",

        # Address
        "вул", "буд", "просп", "пров",
    }

    DATE_ABBRVS = RuRules.DATE_ABBRVS | {
        "січ", "лют", "бер", "кві", "тра", "чер", "лип",
        "сер", "вер", "жов", "лис", "гру","нд",
    }

    COMMON_SENT_STARTERS = RuRules.COMMON_SENT_STARTERS | {
        "Вона", "Воно", "Вони", "Навіщо", "Отже",
        "Проте", "Потім", "Нарешті", "Спочатку",
    }

# fmt: on
