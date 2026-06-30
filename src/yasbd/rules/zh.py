from yasbd.rules.base import CJK, Rules


# fmt: off
class ZhRules(CJK, Rules):


    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "排球少年！", "总之就是非常可爱", "偶像活动", "轻音少女", "魔笛",
        "潜行吧", "闪跃吧", "笨蛋、测验、召唤兽"
    }

    # Chinese has only one pure postnominal quotative particle
    POST_QUOTATIVE_PARTICLES = {"如是"}

    REPORTING_WORDS = {
        "说", "道", "喊", "问", "答", "回答", "称", "指出",
        "表示", "认为", "坦言", "强调", "写道", "报道", "解释", "反驳"
    }
# fmt: on
