import re
from collections.abc import Collection, Iterator
from io import TextIOBase

import ftfy
import regex as re2  # For complex patterns

from yasbd.utils.cleaner_stub import StreamCleanerStub
from yasbd.utils.input_validator import validate_input
from yasbd.utils.paragraph_stream import ParagraphStream

# fmt: off
PREFIXES = {
    "hyper", "ultra", "super", "extra", "semi", "multi", "pre", "post",
    "ex", "cross", "inter", "trans", "anti", "counter", "non", "quasi",
    "self", "auto", "cyber", "techno", "electro", "high", "low", "open",
    "closed", "up", "down", "off", "mid", "vice",
}
# fmt: on

# https://regex101.com/r/csjyrs/2/substitution
_vowels_pattern = "aeiouyæœ"
_suffix_pattern = "|".join(PREFIXES)
HYPHENATED_WORD_FINDER = re2.compile(
    rf"""
    (?<=[{_vowels_pattern}]\p{{M}}?-)\s+(?=[{_vowels_pattern}])|
    (?<=(?:{_suffix_pattern})-)\s|
    (?<!(?:{_suffix_pattern}))-\s|
""",
    re2.X,
)

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

# https://regexr.com/8n5a8
HTML_TAGS_FINDER = re.compile(
    r"""
    # Branch 1: Strip the tag AND its content
    <(script|img|iframe|object|embed|style|code)[^>]*?>.*?</\1>|

    # Branch 2: Just strip the brackets except quick formatting
    </?\b[^libu][^>]*?>
    """,
    re.X | re.I | re.S,
)

# -- Regex ported from pysbd --

# https://regex101.com/r/0dTHBO/3/substitution
NEWLINE_IN_MIDDLE_OF_WORD_FINDER = re2.compile(r"(?<=\b[a-zA-Z]{1,2})\n")

# https://regex101.com/r/VMfP98/3/substitution
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile(r"\n(?=\.(?=\s))")

# https://regex101.com/r/xN77B6/2/substitution
NO_SPACE_BETWEEN_SENTENCES_FINDER = re.compile(r"(?<=\w\.)(?=[A-Z][a-z])")

# https://regex101.com/r/Nw2I67/1
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile(r"\/{3}")


def _clean_ocr_text(text: str) -> str:
    cleaned_text = text.replace("''", '"')
    cleaned_text = NEWLINE_IN_MIDDLE_OF_WORD_FINDER.sub("", cleaned_text)
    cleaned_text = NEWLINE_FOLLOWED_BY_PERIOD_FINDER.sub("", cleaned_text)
    cleaned_text = HEADING_OR_LIST_FINDER.sub(" ", cleaned_text)
    cleaned_text = NO_SPACE_BETWEEN_SENTENCES_FINDER.sub(" ", cleaned_text)
    cleaned_text = ARTIFACT_FINDER.sub("", cleaned_text)
    cleaned_text = HYPHENATED_WORD_FINDER.sub("", cleaned_text)
    cleaned_text = PAGE_FINDER.sub("", cleaned_text)
    return cleaned_text


CLEANING_PIPELINE = {
    "fix_mojibake": ftfy.fix_text,
    "fix_ocr_text": _clean_ocr_text,
    "unwrap_htmls": lambda t: t if "<" not in t else HTML_TAGS_FINDER.sub("", t),
    "normalize_slashes": lambda t: (
        t if "///" not in t else CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", t)
    ),
    "normalize_spaces": lambda t: t if " " not in t else MULTIPLE_SPACES_FINDER.sub(" ", t),
}


class StreamCleaner(StreamCleanerStub):
    """Normalize and clean noisy text by applying ``ftfy``, HTML sanitization,
    and various regex cleanup rules across paragraphs.

    Examples:
        >>> list(StreamCleaner("Hello <b>world</b>. How are you?"))
        ['Hello <b>world</b>. How are you?']
        >>> list(StreamCleaner("<script>alert('xss')</script>clean text"))
        ['clean text']
        >>> list(StreamCleaner("<b>Hello</b> world", steps_to_skip=["unwrap_htmls"]))
        ['<b>Hello</b> world']
        >>> list(StreamCleaner("Text with ///slashes"))
        ['Text with slashes']
        >>> list(StreamCleaner("W\\nO\\nR\\nD"))
        ['WORD']
        >>> list(StreamCleaner("An hyphe-\\nnated sentence"))
        ['An hyphenated sentence']
        >>> list(StreamCleaner("Don't be naï-\\nve"))
        ["Don't be naïve"]
        >>> list(StreamCleaner(""))
        []
        >>> StreamCleaner("Hello world", steps_to_skip=["nothing"])
        Traceback (most recent call last):
        ...
        ValueError: Invalid step(s) to skip: ...
    """

    @validate_input
    def __init__(
        self, source: str | TextIOBase, steps_to_skip: Collection[str] | None = None
    ) -> None:
        """Implements the iterator protocol. Yields cleaned paragraph strings.

        Args:
            source: Plain text string or open text stream (e.g., ``StringIO``).
            steps_to_skip: A collection of steps to ignore. All steps will run if not provided.
                choices are:
                    - fix_mojibake
                    - fix_ocr_text
                    - unwrap_htmls
                    - normalize_slashes
                    - normalize_spaces
        """
        if isinstance(source, (str, TextIOBase)):
            source = ParagraphStream(source, skip_empty_lines=True)
        self._source = iter(source)
        self.steps_to_skip = set(steps_to_skip or ())

        if invalid_steps := self.steps_to_skip - set(CLEANING_PIPELINE):
            raise ValueError(
                f"Invalid step(s) to skip: {', '.join(sorted(invalid_steps))}. "
                f"Valid steps are: {', '.join(CLEANING_PIPELINE.keys())}"
            )

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        for para in self._source:
            stripped = para.strip()
            if not stripped:
                continue

            cleaned_text = stripped
            for step in CLEANING_PIPELINE:
                if step not in self.steps_to_skip:
                    cleaned_text = CLEANING_PIPELINE[step](cleaned_text)
            return cleaned_text

        raise StopIteration
