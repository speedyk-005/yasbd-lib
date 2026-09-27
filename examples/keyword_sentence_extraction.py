"""Extract sentences containing specific keywords from a Chinese news article.

For use cases like social listening or information retrieval, you often
want only the sentences that mention a given entity (company, person,
product) instead of the whole article. This example segments a Chinese
news text with yasbd and keeps only the sentences that contain any of
the supplied keywords.
"""

from yasbd import BoundaryDetector

_detector = BoundaryDetector(lang="zh")


def extract_sentences_with_keywords(text: str, keywords: list[str], lang: str = "zh"):
    """Return the sentences of *text* that mention any of *keywords*.

    Segments *text* into sentences with :class:`yasbd.BoundaryDetector`,
    then keeps every sentence whose lower-cased form contains the lower-
    cased form of at least one keyword. Matching is substring-based, so
    partial matches (e.g. "小米" inside "小米公司") are counted.

    Args:
        text: The raw document text to extract from.
        keywords: The keywords/entities to look for.
        lang: ISO language code passed to the boundary detector.

    Returns:
        A list of sentences that mention at least one keyword.
    """
    _detector.lang = lang
    sentences = list(_detector.segment(text))

    lowered_keywords = [kw.lower() for kw in keywords]
    hits = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(kw in lowered for kw in lowered_keywords):
            hits.append(sentence)
    return hits


if __name__ == "__main__":
    news = (
        "小米公司今天发布了新款手机。雷军在发布会上表示，"
        "这款产品定价3999元，主打影像能力。"
        "与此同时，华为也公布了自家的芯片进展。"
        "你怎么看这次发布？评论区聊聊。"
    )
    result = extract_sentences_with_keywords(news, ["小米", "华为"])
    for sentence in result:
        print(sentence)
