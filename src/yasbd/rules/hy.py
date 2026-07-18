from yasbd.rules.base import Rules


# fmt: off
class HyRules(Rules):


    # Armenian does not use `.` as terminator.
    # Instead sentences typically end with the Armenian full stop (։).
    # Exclamations may end with the Armenian exclamation mark (՜)
    # or the ASCII exclamation mark (!) in modern digital text.
    TERMINATORS = {"։", "՜", "!"}

    TITLE_ABBRVS = set()
    DOTTED_GEOPOL_ABBRVS = set()
    REFERENCE_ABBRVS = set()
    SECTION_MARKERS = set()
    INLINE_ONLY_ABBRVS = set()
    NAMES_WITH_EXCLAMATION = set()
    DATE_ABBRVS = set()

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Ես", "Դու", "Նա", "Մենք", "Դուք", "Նրանք",
        "Սա", "Դա", "Սրանք", "Դրանք",

        # Question words
        "Ով", "Որտեղ", "Ինչ", "Ինչու", "Ինչպես",
        "Որը", "Երբ", "Քանի",
    }

    REPORTING_WORDS = {
        "ասաց", "հարցրեց", "պատասխանեց", "ավելացրեց",
        "բացատրեց", "նշեց", "հայտնեց", "պատմեց",
        "խնդրեց", "առաջարկեց", "շշնջաց", "գոռաց",
        "զգուշացրեց", "հրամայեց", "ծիծաղեց",
    }

# fmt: on
