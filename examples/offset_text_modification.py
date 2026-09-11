"""Modify text using detect() character offsets without losing original layout.

Demonstrates PII redaction by applying sentence replacements in reverse
offset order so preceding character indices never shift.

Run:
    python examples/offset_text_modification.py
"""

from collections.abc import Generator

from yasbd import BoundaryDetector


def get_sentence_spans(
    text: str,
    detector: BoundaryDetector,
) -> Generator[tuple[int, int, str], None, None]:
    """Yield (start_offset, end_offset, sentence_slice) for each sentence."""
    start = 0
    for boundary in detector.detect(text):
        yield (start, boundary, text[start:boundary])
        start = boundary


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
    result = SAMPLE_DOCUMENT

    # Apply redactions in reverse order so earlier offsets remain stable
    for start, end, sentence in reversed(list(get_sentence_spans(SAMPLE_DOCUMENT, detector))):
        if "Patient Jane Doe" in sentence:
            prefix_ws = sentence[: len(sentence) - len(sentence.lstrip())]
            suffix_ws = sentence[len(sentence.rstrip()) :]
            redaction = f"{prefix_ws}[REDACTED: PATIENT RECORD]{suffix_ws}"
            result = result[:start] + redaction + result[end:]

    print("=== Redacted Document ===")
    print(result)


if __name__ == "__main__":
    main()
