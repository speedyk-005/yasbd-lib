"""Chunk text into whole sentences for RAG retrieval.

Character/token cutting splits ideas mid-thought and hurts retrieval.
This example chunks by sentence so boundaries always land between
sentences, with optional overlap to carry context across chunks.
"""

from yasbd import BoundaryDetector

_detector = BoundaryDetector("en")
_MAX_OVERLAP_PERCENT = 80


def chunk_text(text: str, lang: str, max_sentences: int, overlap_percent: int | float):
    """Split text into overlapping sentence chunks for retrieval.

    Segments *text* into sentences with :class:`yasbd.BoundaryDetector`,
    then slides a fixed-size window over the sentence list, keeping
    ``overlap_percent`` of the sentences from the previous chunk at the
    start of the next one. Chunk boundaries therefore always fall on real
    sentence boundaries, and neighbouring chunks share context.

    Args:
        text: The raw document text to chunk.
        lang: ISO language code passed to the boundary detector.
        max_sentences: Positive number of sentences per chunk.
        overlap_percent: Percentage of the window size to carry over
            between consecutive chunks, from 0 to 80 inclusive. Fractional
            percentages are rounded down to a whole number of sentences.

    Returns:
        A list of chunk strings. Each chunk is its sentences joined back
        together without added separators, so the original surrounding
        whitespace is preserved as-is.

    Raises:
        ValueError: If max_sentences is not positive or overlap_percent is
            outside the inclusive range 0 to 80.

    Examples:
        A fractional percentage keeps whole-sentence overlap:

        >>> chunk_text("Alpha. Beta. Gamma. Delta.", "en", 2, 50.5)
        ['Alpha. Beta.', ' Beta. Gamma.', ' Gamma. Delta.']

        Invalid percentages and window sizes are rejected:

        >>> chunk_text("Alpha.", "en", 2, 100)
        Traceback (most recent call last):
            ...
        ValueError: overlap_percent must be between 0 and 80 inclusive
        >>> chunk_text("", "en", 0, 0)
        Traceback (most recent call last):
            ...
        ValueError: max_sentences must be positive
    """
    if max_sentences <= 0:
        raise ValueError("max_sentences must be positive")
    if not 0 <= overlap_percent <= _MAX_OVERLAP_PERCENT:
        raise ValueError("overlap_percent must be between 0 and 80 inclusive")
    if not text:
        return []

    _detector.lang = lang
    sentences = list(_detector.segment(text, preserve_whitespace=True))

    # Each sentence is a unit so we can apply a fixed size windows with overlap
    overlap_num = int((max_sentences * overlap_percent) // 100)
    stride = max(1, max_sentences - overlap_num)

    chunks = [sentences[:max_sentences]]  # First chunk from start
    for idx in range(max_sentences, len(sentences), stride):
        chunk = sentences[idx - overlap_num : idx + stride]
        chunks.append(chunk)

    # Join sentences within each sublist to form final string chunks
    return ["".join(chunk) for chunk in chunks]


# Example usage
if __name__ == "__main__":
    import textwrap

    sample_text = textwrap.dedent("""
        She loves cooking. He studies AI. "You are a Dr." she said. The weather is great.
        We play chess. Books are fun.
        The Playlist contains:
            - two videos
            - one music
        Robots are learning.
        It's raining. Let's code. Mars is red. Sr. sleep is rare.
        Consider item 1. This is a test.
        The year is 2025. This is a good year.
        The section is N.A.S.A. related.
    """)

    chunks = chunk_text(sample_text, lang="en", max_sentences=7, overlap_percent=20)
    for i, chunk in enumerate(chunks):
        print(f"-- Chunk {i + 1} --")
        print(chunk)
        print()
