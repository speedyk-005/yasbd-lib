import re

from yasbd.rules.base import Rules


# fmt: off
class JaRules(Rules):


    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "トニカクカワイイ", "アイカツ", "マギ", "けいおん", "ラブライブ",
        "ハイキュー！", "這いよれ"
    }

    COMMON_SENT_STARTERS = {
        "しかし", "また", "そして", "したがって", "そのため", "一方", "なお", "つまり"
    }

    QUOTATIVE_PARTICLES = {
        # core quotation particles
        "と", "って", "などと",

        # embedded quotation structures
        "ように", "らしいと", "そうだと",
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Full-width geopolitical abbreviations
            re.compile(r"(?:[\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19]．){1,5}")
        )

# fmt: on
