"""Keep sentence offsets valid against the original noisy text.

Cleaning changes character offsets, which breaks anything that must
point at the raw document (highlighting, annotation, redaction). This
example segments the cleaned text with yasbd while mapping every
sentence back to spans in the unmodified input.
"""

import regex as re
from yasbd.cleaner import StreamCleaner

from yasbd import BoundaryDetector

_detector = BoundaryDetector(lang="en")
_ENDING_ARTIFACTS_FINDER = re.compile(r"[\s\p{Po}\p{Pe}\p{Pf}\"'`]+")


def _is_span_char(ch: str) -> bool:
    """Keep ASCII alphanumerics (plus ``#``); drop everything else.

    Accented and mojibake characters are ignored on both sides so that
    cleaning steps rewriting them (cafÃ© -> café) still align.
    """
    return ch.isascii() and (ch.isalnum() or ch == "#")


class DeterministicSpanFinder:
    """
    Find a substring span within full text, ignoring non-alphanumeric characters.

    Only ASCII alphanumerics take part in normalized matching: accented
    and mojibake characters are dropped on both sides, so cleaning steps
    that rewrite them (cafÃ© -> café) cannot break alignment.

    This is a deterministic alternative to regex-based span finding, providing
    ~2x performance improvement by avoiding backtracking and complex pattern matching.
    """

    __slots__ = ("_last_end", "cleaned_full_text", "full_text", "index_map")

    def __init__(self, text: str):
        """
        Initialize the span finder.

        Args:
            text: The full text to search within.
        """
        self.full_text = text
        self.cleaned_full_text, self.index_map = self._build_index_map(text)
        self._last_end = 0

    def _build_index_map(self, text: str) -> tuple[str, dict[int, int]]:
        """Build a cleaned text string and index map for fast searching."""
        index_map = {}
        curr_idx = 0
        chars = []

        for i, ch in enumerate(text):
            if _is_span_char(ch):
                chars.append(ch)
                index_map[curr_idx] = i
                curr_idx += 1

        return "".join(chars), index_map

    def find_span(self, text: str) -> tuple[int, int]:
        """
        Find the start and end indices of a substring within the original text.

        The search is performed in two stages:
        1. Exact match on the original text.
        2. Normalized alphanumeric match if exact match fails.

        Args:
            text: The query substring.

        Returns:
            A tuple consists of start and end indexes in the original text.
            (-1, -1) is returned if no match is found.
        """
        stripped = text.strip()

        if (start := self.full_text.find(stripped, self._last_end)) != -1:
            end = start + len(stripped)
            self._last_end = end
            return start, end

        cleaned_text = "".join(ch for ch in text if _is_span_char(ch))

        pos = self.cleaned_full_text.find(cleaned_text)
        if pos != -1 and cleaned_text:
            start = self.index_map[pos]
            end = self.index_map[pos + len(cleaned_text) - 1] + 1
            self._last_end = end
            return start, end

        return -1, -1


def clean_and_detect_sent_spans(text: str) -> list[tuple[int, int]]:
    """Clean *text*, segment it, and map each sentence to original offsets.

    Runs *text* through :class:`StreamCleaner`, segments the cleaned
    output with yasbd, then finds every cleaned sentence back in the
    *original* text. Trailing artifacts (whitespace, closing quotes and
    brackets, up to 5 chars) are absorbed into each span; sentences that
    cannot be located yield ``(-1, -1)``.

    Args:
        text: The raw noisy text to clean and segment.

    Returns:
        A list of ``(start, end)`` character offsets into the original
        text, one per detected sentence.
    """
    text_len = len(text)
    orig_span_finder = DeterministicSpanFinder(text)
    cleaner = StreamCleaner(text)
    sents = _detector.segment(cleaner)
    spans = [orig_span_finder.find_span(sent) for sent in sents]

    mod_spans = []
    for start, end in spans:
        if start == -1:
            mod_spans.append((start, end))
            continue

        add_offset = _ENDING_ARTIFACTS_FINDER.match(text[end : min(end + 5, text_len)])

        if add_offset:
            end += len(add_offset.group(0))

        mod_spans.append((start, end))

    return mod_spans


if __name__ == "__main__":
    raw = (
        "Visit our café today. An hyphe-\nnated word here. "
        "  Extra   spaces everywhere. <script>x()</script>Done."
    )
    for span in clean_and_detect_sent_spans(raw):
        print(span, repr(raw[span[0] : span[1]]))
