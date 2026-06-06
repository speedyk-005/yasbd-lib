import re

from yasbd.rules.base import Rules, _build_abbr_pattern


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
            # Full-width geopolitical abbrv
            re.compile(rf"(?:[\uFF21-\uFF3A\uFF41-\uFF5A]．){{1,5}}")
        )

# fmt: on
