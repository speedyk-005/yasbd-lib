"""Compare document revisions sentence by sentence using YASBD and difflib.

Install with ``pip install -e .``, then run
``python examples/sentence_revision_diff.py`` and enter each revision on one
line. For example, changing a support policy can replace a response-time
sentence and add a weekend-support sentence.

The JSON output contains inserted, deleted and replaced sentence groups.
Sentence text is stripped for display; start/end are YASBD boundary offsets
in the original revision, with an exclusive end. Matching ignores whitespace
within sentences but preserves case, punctuation, order and repeated sentences.
Both revisions are held in memory. This is an exact comparison of detected
sentences, not a semantic comparison.
"""

import json
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from itertools import pairwise

from yasbd import BoundaryDetector


@dataclass
class SentenceSpan:
    """Sentence text stripped for display, with its original boundary offsets."""

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
    for start, end in pairwise([0, *detector.detect(text)]):
        spans.append(SentenceSpan(start, end, text[start:end].strip()))
    return spans


def compare_revisions(
    before: str, after: str, detector: BoundaryDetector
) -> list[SentenceChange]:
    """Return changed sentence groups in document order.

    Args:
        before: Original revision text.
        after: Updated revision text.
        detector: YASBD detector configured for the revisions' language.

    Returns:
        Inserted, deleted and replaced groups, with text and boundary offsets.
        Unchanged groups are omitted.

    >>> before = "Replies arrive within two days. Contact the support desk."
    >>> after = ("Replies arrive within one day. Contact the support desk. "
    ...          "Weekend support is available.")
    >>> [c.operation for c in compare_revisions(before, after, BoundaryDetector(lang="en"))]
    ['replace', 'insert']
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


def main() -> None:
    """Read two revisions interactively and print their sentence changes."""
    before = input("Original revision: ")
    after = input("Updated revision: ")
    changes = compare_revisions(before, after, BoundaryDetector(lang="en"))
    print(json.dumps([asdict(change) for change in changes], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
