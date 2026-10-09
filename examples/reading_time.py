"""Build a sentence-by-sentence reading schedule for an English article.

Run from a checkout after `pip install -e .`:
    python examples/reading_time.py

The pace is a configurable estimate, not a measured reading speed. Word counting
uses whitespace-separated tokens with at least one letter or number; this model
is intended for English text, not languages that omit spaces between words.
"""

import math
from dataclasses import dataclass

from yasbd import BoundaryDetector


@dataclass(frozen=True)
class SentenceTiming:
    """A sentence and its estimated start/end times in seconds."""

    sentence: str
    start: float
    end: float


def reading_schedule(text: str, words_per_minute: float = 200) -> list[SentenceTiming]:
    """Return cumulative timings suitable for a reading-progress display.

    Args:
        text: English text to segment into sentences.
        words_per_minute: Positive, finite estimated reading pace.

    Returns:
        Sentence timings, without rounding each sentence's duration.

    Raises:
        ValueError: If the reading pace is nonpositive or nonfinite.

    Examples:
        >>> schedule = reading_schedule("Dr. Smith writes. We read his report.", 60)
        >>> [(item.sentence, item.start, item.end) for item in schedule]
        [('Dr. Smith writes.', 0.0, 3.0), ('We read his report.', 3.0, 7.0)]
        >>> reading_schedule("")
        []
        >>> reading_schedule("   ")
        []
        >>> reading_schedule("...", 60)[0].end
        0.0
        >>> reading_schedule("An editor's note contains five words.", 120)[0].end
        3.0
        >>> reading_schedule("News.", 0)
        Traceback (most recent call last):
        ...
        ValueError: words_per_minute must be positive and finite
        >>> reading_schedule("News.", float("inf"))
        Traceback (most recent call last):
        ...
        ValueError: words_per_minute must be positive and finite
    """
    if not math.isfinite(words_per_minute) or words_per_minute <= 0:
        raise ValueError("words_per_minute must be positive and finite")

    schedule = []
    words = 0
    for sentence in BoundaryDetector("en").segment(text):
        start = words * 60 / words_per_minute
        words += sum(any(char.isalnum() for char in token) for token in sentence.split())
        schedule.append(SentenceTiming(sentence, start, words * 60 / words_per_minute))
    return schedule


if __name__ == "__main__":
    article = (
        "Dr. Smith writes the weekly library newsletter. "
        "This week, volunteers restored the reading room. "
        "The library will reopen on Monday."
    )
    for timing in reading_schedule(article):
        print(f"{timing.start:5.1f}s–{timing.end:5.1f}s  {timing.sentence}")
