import re

from yasbd.rules.base import FULLWIDTH_GEOPOLITICAL_ABBRVS, Rules, _build_abbr_pattern


# fmt: off
class JaRules(Rules):

    GEOPOLITICAL_ABBRVS = FULLWIDTH_GEOPOLITICAL_ABBRVS
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

    CASE_MARKERS = {
        "の", "が", "ん", "之", "乃", "は", "を", "に", "も", "と", "で", "から", "より", "へ", "や"
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Geopolitical abbrv is followed by a case maker (e.g., Ｕ．Ｓ．Ａ．の経済政策)
            re.compile(rf"""
                (?i:{cls.GEOPOLITICAL_ABBRVS_PATTERN}){cls.DOTS_PATTERN}
                (?=\s*(?:{_build_abbr_pattern(cls.CASE_MARKERS)}))
                """, re.X
            ),
        )

# fmt: on
