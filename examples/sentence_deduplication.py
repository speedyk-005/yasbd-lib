"""Deduplicate repeated sentences while retaining their original source spans.

Release notes and support articles often repeat boilerplate. This example
keeps one copy of each sentence and records every occurrence for tracing
search results or dataset records back to the original documents.

Install YASBD from the repository, then run the built-in sample or UTF-8 files:

    pip install -e .
    python examples/sentence_deduplication.py
    python examples/sentence_deduplication.py release.txt support.txt --lang en
    python -m doctest examples/sentence_deduplication.py

Output is JSONL with ``text`` and ``occurrences`` (source, start, end).
Offsets are Python character indices with an exclusive end, not byte offsets.
The sample produces three unique sentences; its repeated maintenance notice
has two occurrences, one from each document.

Matching normalizes whitespace and Unicode NFC only: case and punctuation
remain significant. The first occurrence supplies the unmodified sentence
text, and all offsets refer to unmodified input. This is exact normalized
deduplication, not semantic similarity. Memory grows with the number of unique
sentences and recorded occurrences; this is not a bounded-memory corpus tool.
"""

import argparse
import json
import unicodedata
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from yasbd import BoundaryDetector


@dataclass
class Occurrence:
    """Location of a sentence in an original source document."""

    source: str
    start: int
    end: int


@dataclass
class UniqueSentence:
    """First sentence text and the locations of all matching occurrences."""

    text: str
    occurrences: list[Occurrence] = field(default_factory=list)


def deduplicate_sentences(
    documents: Iterable[tuple[str, str]], detector: BoundaryDetector
) -> list[UniqueSentence]:
    r"""Group sentences in first-seen order without discarding source locations.

    Args:
        documents: Pairs of source identifier and original document text.
        detector: YASBD detector configured for the documents' language.

    Returns:
        Unique sentences with every occurrence, including repeats within a file.

    >>> detector = BoundaryDetector(lang="en")
    >>> documents = [("release", "  Maintenance is complete. All services are online."),
    ...              ("support", "Maintenance  is complete. Contact support for help.")]
    >>> result = deduplicate_sentences(documents, detector)
    >>> [sentence.text for sentence in result]
    ['Maintenance is complete.', 'All services are online.', 'Contact support for help.']
    >>> [(item.source, item.start, item.end) for item in result[0].occurrences]
    [('release', 2, 26), ('support', 0, 25)]
    >>> texts = dict(documents)
    >>> [texts[item.source][item.start:item.end] for item in result[0].occurrences]
    ['Maintenance is complete.', 'Maintenance  is complete.']
    >>> repeated = deduplicate_sentences([("one", "Done. Done.")], detector)
    >>> [(item.start, item.end) for item in repeated[0].occurrences]
    [(0, 5), (6, 11)]
    >>> distinct = deduplicate_sentences([("one", "Done. DONE. Done!")], detector)
    >>> [sentence.text for sentence in distinct]
    ['Done.', 'DONE.', 'Done!']
    >>> unicode_result = deduplicate_sentences(
    ...     [("nfc", "Caf\u00e9 opens today."), ("nfd", "Cafe\u0301 opens today.")], detector)
    >>> len(unicode_result), len(unicode_result[0].occurrences)
    (1, 2)
    >>> deduplicate_sentences([("empty", ""), ("blank", " \n\n ")], detector)
    []
    >>> paragraphs = deduplicate_sentences([("one", "\n\nDone.\n\nDone.")], detector)
    >>> [(item.start, item.end) for item in paragraphs[0].occurrences]
    [(2, 7), (9, 14)]
    """
    unique: dict[str, UniqueSentence] = {}
    for source, text in documents:
        start = 0
        for end in detector.detect(text):
            raw_sentence = text[start:end]
            sentence = raw_sentence.strip()
            if sentence:
                trimmed_start = start + len(raw_sentence) - len(raw_sentence.lstrip())
                trimmed_end = end - len(raw_sentence) + len(raw_sentence.rstrip())
                key = unicodedata.normalize("NFC", " ".join(sentence.split()))
                if key not in unique:
                    unique[key] = UniqueSentence(sentence)
                unique[key].occurrences.append(Occurrence(source, trimmed_start, trimmed_end))
            start = end
    return list(unique.values())


SAMPLE_DOCUMENTS = [
    ("release.txt", "Maintenance is complete. All services are online."),
    ("support.txt", "Maintenance  is complete. Contact support for help."),
]


def main() -> None:
    """Read UTF-8 documents or the sample, and write unique sentences as JSONL."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("documents", nargs="*", type=Path, help="UTF-8 text files")
    parser.add_argument("--lang", default="en", help="YASBD language code (default: en)")
    args = parser.parse_args()
    documents = SAMPLE_DOCUMENTS
    if args.documents:
        try:
            documents = []
            for path in args.documents:
                with path.open(encoding="utf-8", newline="") as document:
                    documents.append((str(path), document.read()))
        except (OSError, UnicodeError) as exc:
            parser.error(str(exc))

    for sentence in deduplicate_sentences(documents, BoundaryDetector(lang=args.lang)):
        print(json.dumps(asdict(sentence), ensure_ascii=False))


if __name__ == "__main__":
    main()
