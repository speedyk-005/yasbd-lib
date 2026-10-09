# ruff: noqa: E501, W291, W293 - demo text block keeps long lines and spacing intact
"""Extract quoted speech with its author from English text.

Segments a text with yasbd (which keeps quoted testimony intact instead
of fragmenting it), then finds reporting patterns inside each sentence:
``AUTHOR verb "..."`` and ``"..." verb AUTHOR``. Returns each quote
together with the speaker it belongs to, which is the usual input shape
for dialogue mining and attribution analysis.
"""

import regex as re

from yasbd import BoundaryDetector

_detector = BoundaryDetector(lang="en")

# Base reporting verbs; inflected forms are generated below.
_BASE_VERBS = [
    "say",
    "reply",
    "note",
    "add",
    "ask",
    "shout",
    "whisper",
    "explain",
    "continue",
    "agree",
    "announce",
    "tell",
    "recall",
    "ponder",
    "think",
    "declare",
]

_IRREGULAR = {
    "say": ("said", "says"),
    "tell": ("told", "tells"),
    "think": ("thought", "thinks"),
}


def _verb_variants(verb: str) -> tuple[str, str, str]:
    """Return ``(past, present-3rd-singular, "would + base")`` for *verb*.

    Examples:
        >>> _verb_variants("say")
        ('said', 'says', 'would say')
        >>> _verb_variants("reply")
        ('replied', 'replies', 'would reply')
    """
    if verb in _IRREGULAR:
        past, third = _IRREGULAR[verb]
    elif verb.endswith("y") and verb[-2] not in "aeiou":
        past, third = verb[:-1] + "ied", verb[:-1] + "ies"
    elif verb.endswith("e"):
        past, third = verb + "d", verb + "s"
    else:
        past, third = verb + "ed", verb + "s"
    return past, third, f"would {verb}"


_VERBS = "|".join(form for base in _BASE_VERBS for form in dict.fromkeys(_verb_variants(base)))
_TITLE = r"(?:Dr|Mr|Mrs|Ms|Prof)\.\s+"
_PRONOUN = r"he|she|they|we|I|you|it"
_NAME = rf"(?:{_TITLE})?(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){{0,2}}|{_PRONOUN})"
_QUOTE = r'"[^"]+"'
# Reporting verb, optionally preceded by an -ly adverb ("softly said").
_VERB = rf"(?:\w+ly\s+)?(?:{_VERBS})"

# AUTHOR said "..." (e.g. Dr. Patel said "We agreed.")
LEAD_QUOTE_PATTERN = re.compile(
    rf"(?P<author>{_NAME})\s+(?:{_VERB})\s*,?\s*(?P<quote>{_QUOTE})"
)
# "..." said AUTHOR (e.g. "We agreed," said Dr. Patel.)
TRAIL_QUOTE_PATTERN = re.compile(
    rf"(?P<quote>{_QUOTE})\s*,?\s*(?:{_VERB})\s+(?P<author>{_NAME})"
)
# "..." AUTHOR said (e.g. "That money saved lives," Fauci noted.)
TRAIL_AV_QUOTE_PATTERN = re.compile(
    rf"(?P<quote>{_QUOTE})\s*,?\s*(?P<author>{_NAME})\s+(?:{_VERB})"
)


def extract_quotes(text: str, lang: str = "en") -> list[tuple[str, str]]:
    """Return ``(author, quote)`` pairs found in *text*.

    Segments *text* into sentences with :class:`yasbd.BoundaryDetector`,
    then matches reporting patterns inside each sentence. The author is
    preserved exactly as written (titles included); sentences without a
    reporting pattern are skipped.

    Args:
        text: The raw document text to extract from.
        lang: ISO language code passed to the boundary detector.

    Returns:
        A list of ``(author, quote)`` tuples in document order.
    """
    _detector.lang = lang
    hits = []
    for sentence in _detector.segment(text):
        for pattern in (LEAD_QUOTE_PATTERN, TRAIL_QUOTE_PATTERN, TRAIL_AV_QUOTE_PATTERN):
            hits.extend(
                (match.group("author"), match.group("quote"))
                for match in pattern.finditer(sentence)
            )
    return hits


if __name__ == "__main__":
    article = """
        "The journey of a thousand miles begins with a single step," famously wrote Lao Tzu. Meanwhile, Dr. J. H. Watson recalled Sherlock Holmes saying, "It is a capital mistake to theorize before one has data. Insensibly one begins to twist facts to suit theories, instead of theories to suit facts." 
    
        Can we really trust such old wisdom? "To be, or not to be, that is the question," pondered Hamlet in Act III, Scene I. But as Maya Angelou wisely noted, "People will forget what you said, people will forget what you did, but people will never forget how you made them feel." 
    
        "Wait!" shouted Prof. M. A. Sterling, turning around abruptly. "Did you check the U.S. Census reports for 3.5M records? Mr. Davis said 'No, absolutely not' when we asked him at 4:30 p.m." 
    
        Albert Einstein once left us with this thought: "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world, stimulating progress, giving birth to evolution." Yet, as Oscar Wilde dryly put it, "Experience is simply the name we give our mistakes."
        """
    for author, quote in extract_quotes(article):
        print(f"{author}: {quote}")
