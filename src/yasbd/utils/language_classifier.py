import math
from functools import lru_cache

import py3langid as langid

from yasbd.rules import get_supported_langs

PREFERRED = get_supported_langs()
TOP_K = 5

# Maximum allowed log-score difference from the best candidate.
# Larger values make the detector more willing to favor preferred languages.
MAX_GAP = 15.0


@lru_cache(maxsize=12)
def classify_language(text: str) -> tuple[str, float]:
    """Classify text with a preference for expected languages.

    This function avoids the explicit ``py3langid.LanguageIdentifier`` initialization
    and its associated cold-start cost by relying on this convenience API.

    The algorithm works as follows:
        1. Obtain the ranked language predictions.
        2. Look for preferred languages within the top ``TOP_K`` results.
        3. Only consider preferred languages whose score is within
           ``MAX_GAP`` of the top prediction.
        4. If no suitable preferred language is found, fall back to the
           model's top prediction.
        5. Compute a normalized confidence score using a softmax over the
           selected candidates.

    Args:
        text: The text to classify.

    Returns:
        A tuple containing:
            - The predicted ISO 639-1 language code.
            - A confidence score between 0.0 and 1.0.

    Examples:
        >>> language, confidence = classify_language("kiyès ?")
        >>> language
        'ht'
        >>> 0.0 <= confidence <= 1.0
        True

    Raises:
        ValueError: If the detector returns no language scores.
    """
    ranks = langid.rank(text)
    _, top_score = ranks[0]

    # Prefer expected languages if they are among the strongest candidates.
    candidates = [
        (language, score)
        for language, score in ranks[:TOP_K]
        if (language in PREFERRED and top_score - score <= MAX_GAP)
    ]

    if not candidates:
        candidates = ranks

    # -- Compute a numerically stable softmax. --
    max_score = max(score for _, score in candidates)
    total = sum(math.exp(score - max_score) for _, score in candidates)

    language, score = max(
        candidates,
        key=lambda item: item[1],
    )
    confidence = math.exp(score - max_score) / total

    return language, round(confidence, 2)


if __name__ == "__main__":
    texts = [
        "Hello, how are you?",
        "¿Cómo estás?",
        "Guten Tag!",
        "Привет!",
        "مرحبا",
        "こんにちは",
        "你好",
        "kiyès ?",
    ]
    for text in texts:
        lang, conf = classify_language(text)
        print(f"{lang} ({conf:.2f})  {text}")
