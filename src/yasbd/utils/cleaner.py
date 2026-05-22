import re
from collections.abc import Generator, Iterable

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

# https://regex101.com/r/VMfP98/2/substitution
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile(r"\n(?=\.(\s|\n))")

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


@validate_input
def clean_stream(source: str | Iterable[str]) -> Generator[str, None, None]:
    """Normalize and clean noisy text.

    Applies ``ftfy`` for mojibake repair, strips HTML tags, removes standalone
    characters, page-number artifacts, and re-joins list markers split across
    lines. Non-string iterables are treated as pre-paragraphed input.

    Args:
        source: Plain string or iterable of paragraphs. Strings are split into
            paragraphs via ``ParagraphStreamer``.

    Yields:
        Cleaned text paragraphs.

    Examples:
        >>> from yasbd.utils.cleaner import clean_stream
        >>> list(clean_stream("Hello <b>world</b>. How are you?"))
        ['Hello world . How are you?']
        >>> list(clean_stream(["Page 12 of 45", "line one\\n. text two"]))
        ['', 'line one. text two']
        >>> list(clean_stream("<script>alert('xss')</script>clean text"))
        ['clean text']
        >>> list(clean_stream("Text with ///slashes"))
        ['Text with slashes']
        >>> list(clean_stream("Plain text with no HTML"))
        ['Plain text with no HTML']
        >>> list(clean_stream(""))
        []
    """
    if isinstance(source, str):
        source = ParagraphStreamer(source, skip_empty_lines=True)

    for para in source:
        stripped_para = para.strip()
        if stripped_para:
            stripped_para = ftfy.fix_text(stripped_para)
            stripped_para = stripped_para.replace(
                "''", '"'
            )  # "Pseudo-Double" quote fix
            stripped_para = _sanitize_html(stripped_para)

            if "///" in stripped_para:
                stripped_para = CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", stripped_para)

            if "\n" in stripped_para:
                stripped_para = NEWLINE_IN_MIDDLE_OF_WORD_FINDER.sub("", stripped_para)
                stripped_para = NEWLINE_FOLLOWED_BY_PERIOD_FINDER.sub("", stripped_para)

            stripped_para = HEADING_OR_LIST_FINDER.sub(" ", stripped_para)
            stripped_para = NO_SPACE_BETWEEN_SENTENCES_FINDER.sub(" ", stripped_para)
            stripped_para = ARTIFACT_FINDER.sub("", stripped_para)
            stripped_para = PAGE_FINDER.sub("", stripped_para)

            if "  " in stripped_para:
                stripped_para = MULTIPLE_SPACES_FINDER.sub(" ", stripped_para)

            yield stripped_para
