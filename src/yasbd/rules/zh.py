import re

from yasbd.rules.base import Rules


# fmt: off
class ZhRules(Rules):


    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "排球少年！", "总之就是非常可爱", "偶像活动", "轻音少女", "魔笛",
        "潜行吧", "闪跃吧", "笨蛋、测验、召唤兽"
    }

    # Chinese has only one pure postnominal quotative particle
    QUOTATIVE_PARTICLES = {"如是"}

    REPORTING_WORDS = {
        "说", "道", "喊", "问", "答", "回答", "称", "指出",
        "表示", "认为", "坦言", "强调", "写道", "报道", "解释", "反驳"
    }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Full-width geopolitical abbreviations
            re.compile(r"(?:[\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19]．){1,5}")
        )

# fmt: on
