from yasbd.rules.base import CJKV, Rules


# fmt: off
class KoRules(CJKV, Rules):


    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "하이큐!", "러브라이브", "뱅드림",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns with Topic/Subject Particles Attached
        "저는", "제가", "나는", "내가", "우리는", "우리가", "당신은", "당신이",
        "그는", "그가", "그녀는", "그녀가", "그들은", "그들이", "이것은", "이것이",
        "그것은", "그것이", "저것은", "저것이", "여기는", "여기서",

        # Question Words
        "누구", "누가", "무엇", "무슨", "어디", "언제", "왜", "어떻게", "어느",

        # Adverbs and Discourse Connectors
        "하지만", "그러나", "그렇지만", "그리고", "그러면", "그럼", "그래서",
        "그러니까", "그녀석", "게다가", "더구나", "반면에", "한편", "결국",
        "따라서", "그러므로", "한편으로는", "또한", "마지막으로", "처음에",
        "다음에", "먼저", "우선", "사실", "솔직히", "아무튼", "어쨌든",
    }

    POST_QUOTATIVE_PARTICLES = {
        # Direct Speech Particles
        "라고", "이라고", "하고", "며", "라며", "이라며", "고",

        # Polite speech/Polite reporting forms
        "라고요", "고요",

        # Clausal extensions
        "하며", "하면서", "라고는", "고는",
    }
# fmt: on
