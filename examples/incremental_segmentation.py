"""Segment incrementally received text for live generation pipelines.

Useful for applications that receive text incrementally,
such as LLM output streams, speech generation pipelines,
and other text-processing streams.

YASBD handles sentence detection while StreamSegmenter manages buffered
chunks and retains incomplete trailing text.
"""

from yasbd import BoundaryDetector

FLUSH_THRESHOLD = 10
MIN_SENTENCES_TO_EXTRACT = 2


class IncrementalSegmenter:
    """Incrementally segments streamed text into completed sentences."""

    def __init__(self, lang="en", separator=" "):
        """Initialize the stream segmenter.

        Args:
            lang: Language code used by the sentence boundary detector.
            separator: String used to join buffered text chunks.
        """
        self._buffer = []
        self._completed = []
        self._detector = BoundaryDetector(lang=lang)
        self._separator = separator
        self._dirty = False

    def feed(self, text):
        """Add a text chunk to the stream buffer.

        Args:
            text: New text received from the stream.
        """
        self._buffer.append(text)
        self._dirty = True

        if len(self._buffer) >= FLUSH_THRESHOLD:
            self._extract_completed()

    def _extract_completed(self):
        """Extract completed sentences from the current buffer."""
        if not self._dirty:
            return

        sentences = list(self._detector.segment(self._separator.join(self._buffer)))

        if len(sentences) >= MIN_SENTENCES_TO_EXTRACT:
            self._completed.extend(sentences[:-1])
            self._buffer = [sentences[-1]]

        self._dirty = False

    def get_completed(self):
        """Yield all sentences currently confirmed as complete."""
        self._extract_completed()

        yield from self._completed
        self._completed.clear()

    def get_remnants(self):
        """Return all remaining segments and clear the stream."""
        res = list(self.get_completed())
        res.append(self._separator.join(self._buffer))

        self._buffer.clear()

        return res


if __name__ == "__main__":
    segmenter = IncrementalSegmenter()

    segmenter.feed("My name is")
    segmenter.feed("Mr. Jhon")
    segmenter.feed(". I'm a teacher")
    segmenter.feed("at U.S.A")
    segmenter.feed("since 2029")
    segmenter.feed(". I teach")

    for i, sentence in enumerate(segmenter.get_completed(), start=1):
        print(f"{i}. {sentence}")

    segmenter.feed("English and")
    segmenter.feed("French.")
    segmenter.feed("I also teach")
    segmenter.feed("Python")
    segmenter.feed("to beginners.")
    segmenter.feed("Sometimes")
    segmenter.feed("we study")

    for i, sentence in enumerate(segmenter.get_completed(), start=1):
        print(f"{i}. {sentence}")

    segmenter.feed("machine learning.")
    segmenter.feed("The last sentence")
    segmenter.feed("is not complete")

    for i, sentence in enumerate(segmenter.get_remnants(), start=1):
        print(f"{i}. {sentence}")
