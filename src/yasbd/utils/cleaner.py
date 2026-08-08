import re
from collections.abc import Callable, Collection, Iterator
from io import TextIOBase

import ftfy
import regex as re2  # For complex patterns

from yasbd.exceptions import CleanStepError, InvalidInputError
from yasbd.utils.cleaner_stub import StreamCleanerStub
from yasbd.utils.input_validator import validate_input
from yasbd.utils.logger import log_info
from yasbd.utils.paragraph_stream import ParagraphStream
from yasbd.utils.trie import build_optimized_pattern

# fmt: off
PREFIXES = {
    "anti", "auto", "bi", "counter", "cyber", "de", "dis", "electro", "extra",
    "geo", "hetero", "homo", "hyper", "hypo", "infra", "inter", "intra", "up",
    "macro", "mega", "meta", "micro", "mini", "mis", "mono", "multi", "neo",
    "omni", "pan", "para", "peri", "poly", "pre", "pro", "proto", "post",
    "pseudo", "quasi", "re", "retro", "semi", "sub", "super", "supra",
    "tele", "trans", "tri", "ultra", "un", "uni", "phe", "ani",
}
SUFFIXES = {"sis", "tion", "ry", "nal", "mal", "no", "té"}
# fmt: on

# https://regex101.com/r/dL1zCM/1
DIFFERENT_HYPENS_FINDER = re.compile(r"[\u2010\u2011\u2012\u2013]")

# https://regex101.com/r/csjyrs/3/substitution
_preffixes_pattern = build_optimized_pattern(PREFIXES)
_suffixes_pattern = build_optimized_pattern(SUFFIXES)
HYPHENATED_WORD_FINDER = re2.compile(
    rf"""
    \u00ad\n|   # Soft hyphens are invisible hints

    # Common pre/sufixes that are ussualy not hyphenated
    (?<=(?:{_preffixes_pattern}))-\R|
    -\R(?=(?:{_suffixes_pattern}))|

    (?<=-)\R   # Any hyphen + Vertical space
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

# https://regex101.com/r/Am0FSD/2
HTML_TAGS_FINDER = re.compile(
    r"""
    # HTML comments
    <!--.*?-->|

    # Declarations (<!DOCTYPE html>, <!ENTITY ...>, etc.)
    <![^>]+>|

    # Processing instructions (<?xml ... ?>, <?php ... ?>)
    <\?.*?\?>|

    # Strip the tag AND its content (container elements only)
    <(script|style|iframe|object|code|noscript|svg|canvas|template)\b[^>]*?>.*?</\1>|

    # Strip all remaining tags except lightweight formatting (<b>, <i>, <u>)
    </?(?!/?[bui]\b)[a-zA-Z][^>]*?>
    """,
    re.X | re.I | re.S,
)

# -- Regex ported from pysbd --

# https://regex101.com/r/0dTHBO/4/substitution
NEWLINE_BETWEEN_WORD_CHARS = re2.compile(r"(?<=\w)\n(?=\w)")

# https://regex101.com/r/VMfP98/3/substitution
NEWLINE_FOLLOWED_BY_PERIOD_FINDER = re.compile(r"\n(?=\.(?=\s))")

# https://regex101.com/r/xN77B6/2/substitution
NO_SPACE_BETWEEN_SENTENCES_FINDER = re.compile(r"(?<=\w\.)(?=[A-Z][a-z])")

# https://regex101.com/r/Nw2I67/1
CONSECUTIVE_FORWARD_SLASH_FINDER = re.compile(r"\/{3}")

NEWLINE_NORMALIZER = re.compile(r"\r\n|\r")


def normalize_newlines(text: str) -> str:
    """Normalize Windows (\r\n) and Classic Mac (\r) line endings to Unix (\n)."""
    return NEWLINE_NORMALIZER.sub("\n", text)


def _clean_ocr_text(text: str) -> str:
    cleaned_text = text.replace("''", '"')
    cleaned_text = NEWLINE_BETWEEN_WORD_CHARS.sub("", cleaned_text)
    cleaned_text = NEWLINE_FOLLOWED_BY_PERIOD_FINDER.sub("", cleaned_text)
    cleaned_text = HEADING_OR_LIST_FINDER.sub(" ", cleaned_text)
    cleaned_text = NO_SPACE_BETWEEN_SENTENCES_FINDER.sub(" ", cleaned_text)
    cleaned_text = ARTIFACT_FINDER.sub("", cleaned_text)
    cleaned_text = DIFFERENT_HYPENS_FINDER.sub("-", cleaned_text)
    cleaned_text = HYPHENATED_WORD_FINDER.sub("", cleaned_text)
    return PAGE_FINDER.sub("", cleaned_text)


def unwrap_htmls(text: str) -> str:
    """Strip HTML tags only when the text actually contains angle brackets."""
    return text if "<" not in text else HTML_TAGS_FINDER.sub("", text)


def normalize_slashes(text: str) -> str:
    """Collapse runaway forward-slash runs used as OCR/layout artifacts."""
    return text if "///" not in text else CONSECUTIVE_FORWARD_SLASH_FINDER.sub("", text)


def normalize_spaces(text: str) -> str:
    """Collapse repeated spaces when present; skip the regex otherwise."""
    return text if " " not in text else MULTIPLE_SPACES_FINDER.sub(" ", text)


DEFAULT_CLEANING_PIPELINE = {
    "normalize_newlines": normalize_newlines,
    "fix_mojibake": ftfy.fix_text,
    "fix_ocr_text": _clean_ocr_text,
    "unwrap_htmls": unwrap_htmls,
    "normalize_slashes": normalize_slashes,
    "normalize_spaces": normalize_spaces,
}


class StreamCleaner(StreamCleanerStub):
    """Normalize line endings, clean noisy text by applying ``ftfy``, HTML sanitization,
    and various regex cleanup rules across paragraphs.

    Examples:
        >>> list(StreamCleaner("x < 5 and y > 3"))
        ['x < 5 and y > 3']
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
        >>> list(StreamCleaner("state-of-the-\\nart"))
        ['state-of-the-art']
        >>> list(StreamCleaner(""))
        []
        >>> StreamCleaner("Hello world", steps_to_skip=["nothing"])
        Traceback (most recent call last):
        ...
        yasbd.exceptions.InvalidInputError: 🧩 Oops! Unknown step(s): 'nothing'...
        >>> list(StreamCleaner("Hello™ world", extra_steps=[lambda t: t.replace("™", "")]))
        ['Hello world']
        >>> list(StreamCleaner("hello", extra_steps=[lambda t: 1/0]))
        Traceback (most recent call last):
        ...
        yasbd.exceptions.CleanStepError: extra step '<lambda>' raised an error.
        Details: division by zero
    """

    @validate_input
    def __init__(
        self,
        source: str | TextIOBase,
        steps_to_skip: Collection[str] | None = None,
        extra_steps: Collection[Callable[[str], str]] | None = None,
        *,
        verbose: bool = False,
    ) -> None:
        """Implements the iterator protocol. Yields cleaned paragraph strings.

        Args:
            source: Plain text string or open text stream (e.g., ``StringIO``).
            steps_to_skip: A collection of steps to ignore. All steps will run if not provided.
                choices are:
                    - normalize_newlines
                    - fix_mojibake
                    - fix_ocr_text
                    - unwrap_htmls
                    - normalize_slashes
                    - normalize_spaces
            extra_steps: Optional user-defined cleaning functions, run after built-in steps.
                Each function must accept and return ``str``.
            verbose: Enable verbose logging.
        """
        if isinstance(source, (str, TextIOBase)):
            source = ParagraphStream(source, skip_empty_lines=True)
        self._source = iter(source)
        self.steps_to_skip = set(steps_to_skip or ())
        self.verbose = verbose

        if invalid_steps := self.steps_to_skip - set(DEFAULT_CLEANING_PIPELINE):
            raise InvalidInputError(
                f"🧩 Oops! Unknown step(s): {', '.join(repr(s) for s in sorted(invalid_steps))}. "
                f"Valid steps: {', '.join(DEFAULT_CLEANING_PIPELINE.keys())}."
            )

        self.extra_steps = list(extra_steps or ())
        log_info(
            self.verbose,
            "StreamCleaner initialized with {} extra step(s)",
            len(self.extra_steps),
        )

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        for para in self._source:
            stripped = para.strip()
            if not stripped:
                continue
            return self._apply_cleaning_pipeline(stripped)

        raise StopIteration

    def _apply_cleaning_pipeline(self, text: str) -> str:
        for step_name in DEFAULT_CLEANING_PIPELINE:
            if step_name not in self.steps_to_skip:
                log_info(self.verbose, "Applying step: {}", step_name)
                text = DEFAULT_CLEANING_PIPELINE[step_name](text)

        for step in self.extra_steps:
            log_info(self.verbose, "Applying extra step: {}", getattr(step, "__name__", step))

            try:
                result = step(text)
            except Exception as e:
                raise CleanStepError(
                    f"extra step {getattr(step, '__name__', step)!r} raised an error.\n"
                    f"Details: {e!s}"
                ) from e

            if not isinstance(result, str):
                raise CleanStepError(
                    f"extra step {getattr(step, '__name__', step)!r} "
                    f"returned {type(result).__name__}, expected str"
                )
            text = result
        return text
