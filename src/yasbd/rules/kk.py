import regex as re

from yasbd.rules.base import Rules


# fmt: off
class KkRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Standard Professional / Academic (Shared & Native)
        "акад", "проф", "доц", "асс", "д-р", "канд", "дир",
        "орынб", "басқ", "мүше-корр","м.а", "к.м.с",
        "д.м.с", "к.т.н", "д.т.н",

        # Kazakh Academic Degrees (Highly critical dotted abbreviations)
        "ғ-м", "ғыл", "т.ғ.к", "ф.ғ.к", "ф.ғ.д", "з.ғ.к",
        "э.ғ.к", "п.ғ.к",

        # Military / Administrative
        "ген", "полк", "подп", "подполк", "лейт", "кап",
        "май", "генерал-май", "и.о", "қ.м.а",

        # Social & Address
        "аға", "мырз", "ханым", "жолд",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "б", "бб", "бет", "т", "тт", "том", "бап",
        "тарм", "ж.б", "т.с.с", "см", "басп",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Тарау", "Бөлім", "Бап", "Тармақ", "Кітап",
        "Кіріспе", "Қорытынды", "Параграф", "Том",
        "Сілтеме", "Қосымша", "Түсіндірме", "Ереже",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "қар", "қ", "обл", "ауд", "көш", "даң",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "қаң", "ақп", "нау", "сәу", "мам", "мау",
        "шіл", "там", "қыр", "қаз", "қар", "жел",

        # Days
        "дс", "сс", "ср", "бс", "жм", "сб", "жс",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Біз", "Бұл", "Кейбір", "Мен", "Ол", "Олар", "Осы",
        "Сен", "Сендер", "Сол", "Сіз", "Сіздер", "Әлгі",

        # Question words
        "Кім", "Не", "Қайда", "Қашан", "Неге", "Неліктен",
        "Қалай", "Қандай", "Қанша",

        # Adverbs / Transitions
        "Алдымен", "Әрі", "Бірінші", "Екінші", "Үшінші",
        "Бірақ", "Дегенмен", "Сонымен", "Сөйтіп", "Одан кейін",
        "Кейін", "Кейінірек", "Бұрын", "Қазір", "Енді", "Сонда",
        "Сондықтан", "Өйткені", "Себебі", "Алайда", "Демек",
        "Сайып келгенде", "Мысалы", "Атап айтқанда",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle year abbrvs"""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST.append(
            re.compile(r"(?<=\d\s+ж{1,2}\.)")
        )
