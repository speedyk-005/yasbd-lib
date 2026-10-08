"""Compare document revisions at sentence boundaries, retaining source offsets.

Policy updates and support articles often arrive as wrapped paragraphs, where
a line-based diff obscures which sentences changed. This example uses YASBD
to segment each revision, then difflib to report inserted, deleted or replaced
sentence groups. Whitespace is normalized within each detected sentence;
case and punctuation changes remain significant. Sentence order and repeated
occurrences are kept.

Install YASBD from the repository, then run the sample or two UTF-8 files:

    pip install -e .
    python examples/sentence_revision_diff.py
    python examples/sentence_revision_diff.py before.txt after.txt --lang en
    python -m doctest examples/sentence_revision_diff.py

Output is JSON with the operation and before/after sentence groups. Each
sentence has its unmodified text and start/end Python character indices in
its respective revision (exclusive end, not byte offsets). Files are read
without translating line endings, so source slices retain their original
layout. Adjacent edits may share one change group. This is an exact sentence
comparison, not a semantic comparison or a detector of moved paragraphs.
Both revisions and their sentence lists are held in memory.
"""

import argparse
import json
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path

from yasbd import BoundaryDetector


@dataclass
class SentenceSpan:
    """Unmodified sentence text and its location in one revision."""

    start: int
    end: int
    text: str


@dataclass
class SentenceChange:
    """An insertion, deletion or replacement of consecutive sentence groups."""

    operation: str
    before: list[SentenceSpan]
    after: list[SentenceSpan]


def _sentence_spans(text: str, detector: BoundaryDetector) -> list[SentenceSpan]:
    spans = []
    start = 0
    for end in detector.detect(text):
        raw = text[start:end]
        left = start + len(raw) - len(raw.lstrip())
        right = start + len(raw.rstrip())
        if left < right:
            spans.append(SentenceSpan(left, right, text[left:right]))
        start = end
    return spans


def compare_revisions(
    before: str, after: str, detector: BoundaryDetector
) -> list[SentenceChange]:
    r"""Return changed sentence groups in document order.

    Args:
        before: Original revision text.
        after: Updated revision text.
        detector: YASBD detector configured for the revisions' language.

    Returns:
        Change groups with source spans from each revision. Unchanged groups
        are omitted. Matching collapses whitespace only; returned text and
        offsets always refer to the original inputs.

    >>> detector = BoundaryDetector(lang="en")
    >>> before = ("Dr. Lee checks tickets. Replies arrive within two days. "
    ...           "Contact the support desk.")
    >>> after = ("Dr. Lee checks tickets. Replies arrive within one day. "
    ...          "Contact the support desk. Weekend support is available.")
    >>> changes = compare_revisions(before, after, detector)
    >>> [change.operation for change in changes]
    ['replace', 'insert']
    >>> [span.text for span in changes[0].before]
    ['Replies arrive within two days.']
    >>> [span.text for span in changes[0].after]
    ['Replies arrive within one day.']
    >>> changes[1].before, [span.text for span in changes[1].after]
    ([], ['Weekend support is available.'])
    >>> all(before[s.start:s.end] == s.text for c in changes for s in c.before)
    True
    >>> all(after[s.start:s.end] == s.text for c in changes for s in c.after)
    True
    >>> compare_revisions("Dr. Lee reviews\nurgent tickets.",
    ...                   "Dr. Lee reviews urgent   tickets.", detector)
    []
    >>> compare_revisions(" \n\n ", "", detector)
    []
    >>> added = compare_revisions("", "Welcome. Service is online.", detector)
    >>> added[0].operation, len(added[0].after)
    ('insert', 2)
    >>> removed = compare_revisions("Done. Done.", "Done.", detector)
    >>> removed[0].operation, removed[0].before[0].start
    ('delete', 6)
    >>> compare_revisions("Service is online.", "Service is online!", detector)[0].operation
    'replace'
    >>> before = "\n\nCafé opens today.\n\nService is stable."
    >>> after = "\r\n\r\nCafé opens today.\r\n\r\nService is restored."
    >>> change = compare_revisions(before, after, detector)[0]
    >>> change.before[0].start == before.index("Service")
    True
    >>> change.after[0].start == after.index("Service")
    True
    >>> after[change.after[0].start:change.after[0].end]
    'Service is restored.'
    >>> repeated = "Boilerplate remains unchanged. "
    >>> old = repeated * 210 + "End."
    >>> new = repeated * 105 + "New contact details follow. " + repeated * 105 + "End."
    >>> changes = compare_revisions(old, new, detector)
    >>> [(c.operation, [s.text for s in c.after]) for c in changes]
    [('insert', ['New contact details follow.'])]
    >>> chinese = BoundaryDetector(lang="zh")
    >>> change = compare_revisions("设备运行正常。明天维护。",
    ...                            "设备运行正常。周末维护。", chinese)[0]
    >>> [s.text for s in change.after]
    ['周末维护。']
    """
    old_spans = _sentence_spans(before, detector)
    new_spans = _sentence_spans(after, detector)
    matcher = SequenceMatcher(
        None,
        [" ".join(span.text.split()) for span in old_spans],
        [" ".join(span.text.split()) for span in new_spans],
        autojunk=False,
    )
    return [
        SentenceChange(operation, old_spans[left:right], new_spans[new_left:new_right])
        for operation, left, right, new_left, new_right in matcher.get_opcodes()
        if operation != "equal"
    ]


def _read_text(path: Path) -> str:
    with path.open(encoding="utf-8", newline="") as source:
        return source.read()


def main() -> None:
    """Compare two supplied files or print the built-in support-policy example."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("before", nargs="?", type=Path, help="Original UTF-8 revision")
    parser.add_argument("after", nargs="?", type=Path, help="Updated UTF-8 revision")
    parser.add_argument("--lang", default="en", help="YASBD language code (default: en)")
    args = parser.parse_args()
    if (args.before is None) != (args.after is None):
        parser.error("provide both revision files, or neither to run the sample")

    if args.before is None:
        before = (
            "Dr. Lee checks tickets. Replies arrive within two days. Contact the support desk."
        )
        after = (
            "Dr. Lee checks tickets. Replies arrive within one day. "
            "Contact the support desk. Weekend support is available."
        )
    else:
        before, after = _read_text(args.before), _read_text(args.after)

    changes = compare_revisions(before, after, BoundaryDetector(lang=args.lang))
    print(json.dumps([asdict(change) for change in changes], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
