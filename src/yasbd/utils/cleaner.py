import re
from collections.abc import Iterator
from io import TextIOBase

import ftfy
import regex as re2  # For complex patterns
from selectolax.lexbor import LexborHTMLParser

from yasbd.utils.input_validator import validate_input
from yasbd.utils.paragraph_streamer import ParagraphStreamer

# https://regex101.com/r/PEPPA7/1/substitution
# HYPHENATED_WORD_FINDER = re.compile(r"([a-z])\u00AD\n([a-z])")

# https://regex101.com/r/POTL2H/5/substitution
HEADING_OR_LIST_FINDER = re2.compile(r"(?<=^\s?(?:[-•*+]|[\w\d][.)]))\s*\n", re2.M)

# https://regex101.com/r/J5Cpyk/8
ARTIFACT_FINDER = re.compile(r"^\s*[-•*+=#\/\\_⯀∎]\s*$", re.M)

# https://regex101.com/r/pKi6y3/1
MULTIPLE_SPACES_FINDER = re.compile(r"\s{2,}")

# https://regex101.com/r/DgnxSq/2
PAGE_FINDER = re.compile(
    r"""
    ^\s*(?:
        Page\ \d+\ of\ \d+|  # Match "Page X of Y"
        -\s*\d+\s*-|          # Match "- X -"
        \|\s*Page\ \d+\s*\|   # Match "| Page X |"
    )\s*$
    """,
    re.X | re.M,
)


# -- Regex ported from pysbd --

# https://regex101.com/r/0dTHBO/1/substitution
NEWLINE_IN_MIDDLE_OF_WORD_FINDER = re2.compile(r"(?<=[a-zA-Z]{1,2})\n")

# https://regex101.com/r/VMfP98/3/substitution
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile(r"\n(?=\.(?=\s))")

# https://regex101.com/r/xN77B6/2/substitution
NO_SPACE_BETWEEN_SENTENCES_FINDER = re.compile(r"(?<=\w\.)(?=[A-Z][a-z])")

# https://regex101.com/r/Nw2I67/1
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile(r"\/{3}")


def _sanitize_html(text: str) -> str:
    """Sanitizes dangerous HTML markup and layout tags from a text."""
    if "<" in text:
        tree = LexborHTMLParser(text)
        tree.strip_tags(["script", "style", "iframe", "object", "embed"])
        return tree.text(separator=" ")
    return text


class StreamCleaner:
    """Normalize and clean noisy text by applying ``ftfy``, HTML sanitization,
    and various regex cleanup rules across paragraphs.

    Implements the iterator protocol. Yields cleaned paragraph strings.

    Args:
        source: Plain string or iterable of pre-paragraphed strings.

    Examples:
        >>> cleaner = StreamCleaner("Hello <b>world</b>. How are you?")
        >>> list(cleaner)
        ['Hello world . How are you?']
        >>> cleaner = StreamCleaner("<script>alert('xss')</script>clean text")
        >>> list(cleaner)
        ['clean text']
        >>> cleaner = StreamCleaner("Text with ///slashes")
        >>> list(cleaner)
        ['Text with slashes']
        >>> cleaner = StreamCleaner("Plain text with no HTML")
        >>> list(cleaner)
        ['Plain text with no HTML']
        >>> list(StreamCleaner(""))
        []
    """

    @validate_input
    def __init__(self, source: str | TextIOBase) -> None:
        if isinstance(source, (str, TextIOBase)):
            source = ParagraphStreamer(source, skip_empty_lines=True)
        self._source = iter(source)

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        for para in self._source:
            stripped = para.strip()
            if not stripped:
                continue

            stripped = ftfy.fix_text(stripped)
            stripped = stripped.replace("''", '"')

            stripped = _sanitize_html(stripped)

            if "///" in stripped:
                stripped = CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", stripped)

            if "\n" in stripped:
                stripped = NEWLINE_IN_MIDDLE_OF_WORD_FINDER.sub("", stripped)
                stripped = NEWLINE_FOLLOWED_BY_PERIOD_FINDER.sub("", stripped)

            stripped = HEADING_OR_LIST_FINDER.sub(" ", stripped)
            stripped = NO_SPACE_BETWEEN_SENTENCES_FINDER.sub(" ", stripped)
            stripped = ARTIFACT_FINDER.sub("", stripped)
            stripped = PAGE_FINDER.sub("", stripped)

            if "  " in stripped:
                stripped = MULTIPLE_SPACES_FINDER.sub(" ", stripped)

            return stripped

        raise StopIteration
