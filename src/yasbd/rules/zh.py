import re

from yasbd.rules.base import FULLWIDTH_GEOPOLITICAL_ABBRVS, Rules, _build_abbr_pattern


# fmt: off
class ZhRules(Rules):


    GEOPOLITICAL_ABBRVS = FULLWIDTH_GEOPOLITICAL_ABBRVS

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "排球少年！", "总之就是非常可爱", "偶像活动", "轻音少女", "魔笛", 
        "潜行吧", "闪跃吧", "笨蛋、测验、召唤兽"
    }

    # Chinese has only one pure postnominal quotative particle
    QUOTATIVE_PARTICLES = {"如是"}

    # Focuses on morphological suffixes that routinely attach to any noun or verb type
    # including loanwords, acronyms, and variables.
    CASE_MARKERS = {"的", "地", "得", "之"}

    REPORTING_WORDS = {
        "说", "道", "喊", "问", "答", "回答", "称", "指出", 
        "表示", "认为", "坦言", "强调", "写道", "报道", "解释", "反驳"
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        # Let the base class build the default rules first
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Geopolitical abbrv is followed by a case maker (e.g., Ｕ．Ｓ．Ａ．的经济)
            re.compile(rf"""
                (?i:{cls.GEOPOLITICAL_ABBRVS_PATTERN}){cls.DOTS_PATTERN}
                (?=(?:{_build_abbr_pattern(cls.CASE_MARKERS)}))
                """, re.X
            ),
        )

# fmt: on
