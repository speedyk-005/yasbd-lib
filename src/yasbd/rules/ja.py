import re

from yasbd.rules.base import Rules


# fmt: off
class JaRules(Rules):


    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "トニカクカワイイ", "アイカツ", "マギ", "けいおん", "ラブライブ",
        "ハイキュー！", "這いよれ"
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "私は", "私たちは", "あなたは", "彼は", "彼女は",
        "それは", "彼らは", "これは", "あれは", "そこは",

        # Question words
        "誰", "何", "どこ", "いつ", "なぜ", "どう", "どの", "どちら",

        # Adverbs
        "しかし", "さらに", "それでも", "したがって", "その結果",
        "一方", "なお", "さもなければ",
        "そして", "その後", "後で", "現在",
        "最後に", "最初に", "次に", "第一に", "第二に", "第三に",
        "以前",
    }

    POST_QUOTATIVE_PARTICLES = {
        # core quotation particles
        "と", "って", "などと",

        # embedded quotation structures
        "ように", "らしいと", "そうだと",
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
