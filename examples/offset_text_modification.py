"""Modify text using detect() character offsets without losing character positions.

When preparing documents for compliance (e.g. PII redaction), search
indexing (e.g. sentence-level keyword highlighting), or downstream NLP
tagging, modifying text after splitting with standard methods breaks
original character offsets, multi-space indentations, and line breaks.

``yasbd.BoundaryDetector.detect()`` yields exact integer boundary offsets
directly from the source text. By pairing these boundaries into spans
(start, end) and applying edits in reverse offset order, earlier character
positions remain completely stable, preserving full document layout and
unmodified content byte-for-byte.

Run:
    python examples/offset_text_modification.py
"""

from collections.abc import Callable, Generator

from yasbd import BoundaryDetector


def get_sentence_spans(
    text: str,
    detector: BoundaryDetector,
) -> Generator[tuple[int, int, str], None, None]:
    """Yield (start_offset, end_offset, sentence_slice) for each sentence in text.

    Args:
        text: The source document text.
        detector: Configured :class:`yasbd.BoundaryDetector` instance.

    Yields:
        Tuples of ``(start, end, text[start:end])`` containing the exact
        character span and original text slice for every detected sentence.
    """
    start = 0
    for boundary in detector.detect(text):
        yield (start, boundary, text[start:boundary])
        start = boundary


def modify_sentences(
    text: str,
    detector: BoundaryDetector,
    transform: Callable[[str, int, int], str | None],
) -> str:
    """Apply a transformation to sentences in a document using exact offsets.

    Args:
        text: The raw source document.
        detector: The boundary detector to locate sentence boundaries.
        transform: A callback taking ``(sentence_text, start_offset, end_offset)``.
            If it returns a string, that string replaces the sentence slice.
            If it returns ``None``, the sentence is left unchanged.

    Returns:
        The modified document with all transformations applied. Because
        replacements are performed from highest offset to lowest offset,
        earlier spans are never invalidated by preceding edits.
    """
    spans = list(get_sentence_spans(text, detector))
    result = text

    # Process in reverse offset order to prevent shift of earlier indices
    for start, end, sentence in reversed(spans):
        replacement = transform(sentence, start, end)
        if replacement is not None and replacement != sentence:
            result = result[:start] + replacement + result[end:]

    return result


# Sample multi-paragraph document with abbreviations, layout, and PII
SAMPLE_DOCUMENT = (
    "CLINICAL STUDY REPORT\n"
    "Dr. H. Adams completed the audit on 2026-03-15. "
    "Patient Jane Doe (ID: 489-01) showed complete remission. "
    "Adverse events: none observed during the 90-day trial period.\n\n"
    "RECOMMENDATION\n"
    "Further studies are planned across the U.S. and Europe. "
    "All participating clinics should maintain standard protocol."
)


def main() -> None:
    detector = BoundaryDetector(lang="en")

    print("=== Original Document ===")
    print(SAMPLE_DOCUMENT)
    print()

    # 1. Inspect character spans
    print("=== Detected Sentence Spans ===")
    spans = list(get_sentence_spans(SAMPLE_DOCUMENT, detector))
    for i, (start, end, sent) in enumerate(spans, start=1):
        print(f"Sentence {i} [{start:>3}:{end:>3}]: {sent.strip()!r}")

    # Verify that concatenating all spans reconstructs the source document exactly
    reconstructed = "".join(sent for _, _, sent in spans)
    assert reconstructed == SAMPLE_DOCUMENT, (  # noqa: S101
        "Reconstructed text drifted from source document."
    )
    print("\nOK: All character spans perfectly reconstruct the source document.\n")

    # 2. Use Case A: PII Redaction
    # Redact sentences containing patient identifiers while preserving whitespace
    def redact_patient_pii(sentence: str, _start: int, _end: int) -> str | None:
        if "Patient Jane Doe" in sentence:
            prefix_ws = sentence[: len(sentence) - len(sentence.lstrip())]
            suffix_ws = sentence[len(sentence.rstrip()) :]
            return f"{prefix_ws}[REDACTED: SENSITIVE PATIENT RECORD]{suffix_ws}"
        return None

    redacted_doc = modify_sentences(SAMPLE_DOCUMENT, detector, redact_patient_pii)
    print("=== Use Case A: PII Redaction ===")
    print(redacted_doc)
    print()

    assert "[REDACTED: SENSITIVE PATIENT RECORD]" in redacted_doc  # noqa: S101
    assert "Dr. H. Adams" in redacted_doc  # noqa: S101
    assert "U.S. and Europe" in redacted_doc  # noqa: S101

    # 3. Use Case B: Keyword/Entity Highlighting
    # Wrap sentences mentioning specific entities or outcomes in markup tags
    def highlight_key_findings(sentence: str, _start: int, _end: int) -> str | None:
        if "remission" in sentence.lower():
            prefix_ws = sentence[: len(sentence) - len(sentence.lstrip())]
            suffix_ws = sentence[len(sentence.rstrip()) :]
            inner = sentence.strip()
            return f"{prefix_ws}<mark>{inner}</mark>{suffix_ws}"
        return None

    highlighted_doc = modify_sentences(SAMPLE_DOCUMENT, detector, highlight_key_findings)
    print("=== Use Case B: Search Result Highlighting ===")
    print(highlighted_doc)
    print()

    expected_highlight = (
        "<mark>Patient Jane Doe (ID: 489-01) showed complete remission.</mark>"
    )
    assert expected_highlight in highlighted_doc  # noqa: S101
    print("OK: Sentence modification completed successfully without offset drift.")


if __name__ == "__main__":
    main()
