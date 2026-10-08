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

_VERBS = (
    r"said|says|say|noted|notes|added|replied|asked|shouted|"
    r"whispered|explained|continued|agreed|announced|told|recalled|"
    r"pondered|saying|thought|declared"
)
_TITLE = r"(?:Dr|Mr|Mrs|Ms|Prof)\.\s+"
_PRONOUN = r"he|she|they|we|I|you|it"
_NAME = rf"(?:{_TITLE})?(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){{0,2}}|{_PRONOUN})"
_QUOTE = r'"[^"]+"'
# Reporting verb, optionally preceded by an -ly adverb ("softly said").
_VERB = rf"(?:\w+ly\s+)?(?:{_VERBS})"

# AUTHOR said "..." (e.g. Dr. Patel said "We agreed.")
_LEAD_PATTERN = re.compile(rf"(?P<author>{_NAME})\s+(?:{_VERB})\s*,?\s*(?P<quote>{_QUOTE})")
# "..." said AUTHOR (e.g. "We agreed," said Dr. Patel.)
_TRAIL_PATTERN = re.compile(rf"(?P<quote>{_QUOTE})\s*,?\s*(?:{_VERB})\s+(?P<author>{_NAME})")
# "..." AUTHOR said (e.g. "That money saved lives," Fauci noted.)
_TRAIL_AV_PATTERN = re.compile(
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
        for pattern in (_LEAD_PATTERN, _TRAIL_PATTERN, _TRAIL_AV_PATTERN):
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
