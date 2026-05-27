from yasbd.rules.base import Rules


# fmt: off
class JaRules(Rules):
    ISO_CODE = "ja"

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "トニカクカワイイ",  "アイカツ",  "マギ",  "けいおん",  "ラブライブ",
        "ハイキュー！",  "這いよれ"
    }

    COMMON_SENT_STARTERS = {
        "しかし", "また", "そして", "したがって", "そのため", "一方", "なお", "つまり"
    }

    QUOTATIVE_PARTICLES = {
        # core quotation particles
        "と", "って", "などと",

        # embedded quotation structures
        "ように", "らしいと", "そうだと",  # "そう言って"
    }

    CASE_MARKERS = {
        "の", "が", "ん", "之", "乃", "は", "を", "に", "も", "と", "で", "から", "より", "へ", "や"
    }

# fmt: on
