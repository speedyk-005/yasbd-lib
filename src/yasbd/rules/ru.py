from yasbd.rules.base import Rules


# fmt: off
class RuRules(Rules):


    TITLE_ABBRVS = {
        # Standard Professional
        "ак", "акад", "доц", "проф", "д-р", "канд",
        "дир", "зам. дир", "зав. каф", "асп", "в.н.с", "гл. науч. сотр",
        "вед. науч. сотр", "ст. науч. сотр", "науч. сотр", "мл. науч. сотр", "м.н.с",
        "чл.-к", "чл.-корр", "чл.-кор", "к.м.с",

        # Military / Political / Administrative
        "ген", "полк", "подп", "лейт", "кап", "и.о",

        # Noble / Royal
        "кн", "вел. кн", "гр", "бар", "св.кн", "имп",
        "имп-ца", "цес", "цес-на",

        # Others
        "г-н", "г-жа", "госп", "тов", "св", "бл",
        "о", "оо",
    }

    # English geopolitical abbreviations (USA, UK, NATO, etc.) may appear in
    # Russian texts but are typically replaced by Russian equivalents or treated
    # as foreign Latin-script tokens rather than native patterns.
    GEOPOLITICAL_ABBRVS = set()

    REFERENCE_ABBRVS = {
        "см", "ср", "цит", "цит по", "с", "стр", "гл", "разд", "раздл", "§",
        "п", "пп", "ст", "табл", "рис", "прим", "прил", "напр", "вып", "т.к",
        "и.о", "ч", "изд", "собр", "соч", "т", "тт"
    }

    HEADING_TOKENS = {
        "Глава", "Часть", "Раздел", "Статья", "Параграф",
        "Том", "Книга", "Подраздел", "Модуль", "Дивизион",
        "Использование", "Единица", "Предисловие", "Введение"
    }

    MID_SENTENCE_ABBRVS = Rules.MID_SENTENCE_ABBRVS | {
        "в", "вв", "г", "гг", "до н.э", "н.э", "руб", "коп", "долл", "тыс",
        "млн", "млрд", "трлн", "экз", "ед", "шт", "ул", "пр", "пер", "пл",
        "обл", "р-н", "окт", "нояб", "дек", "янв", "февр", "март", "апр",
        "июн", "июл", "авг", "сент", "и др", "и пр", "и т.д", "и т.п"
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "Яндекс", "Билайн", "Сбер",
    }

    DATE_ABBRVS = {
        # Months
        "янв", "фев", "мар", "апр", "июн", "июл", "авг", "сен",
        "сен", "окт", "ноя", "дек", "дек",

        # Day
        "пн", "вт", "ср", "чт", "чт", "чт", "пт",
        "сб", "вс", "пн", "вт", "вс",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Я", "Мы", "Вы", "Он", "Она", "Оно", "Они", "Это", "Тот",
        "Эти", "Те", "Там",

        # Question words
        "Кто", "Что", "Где", "Когда", "Почему", "Зачем", "Как", "Какой",
        "Чей", "Кого", "Кому",

        # Adverbs / Transitions
        "Однако", "Более", "Тому", "Тем", "Не менее", "Поэтому",
        "Следовательно", "Между", "Тем временем", "Кроме", "Того",
        "Впрочем", "Далее", "Иначе",

        # Other common starters
        "Делают", "Сделал", "Миллионы",
    }

    # Particles like "мол", "де", "дескать" exist in Russian but are rarely
    # used alongside quoted text, so they don't affect sentence boundaries.
    QUOTATIVE_PARTICLES = set()
# fmt: on
