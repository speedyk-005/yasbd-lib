import io
from collections.abc import Generator, Iterator
from importlib import import_module
from itertools import tee, islice, chain
from typing import NamedTuple

from loguru import logger


class TextSpan(NamedTuple):
    start: int
    end: int
    text: str

    @property
    def sent(self) -> str:
        """Alias for pysbd compatibility.

        Returns:
            str: The sentence text, identical to ``.text``.
        """
        return self.text

    def __str__(self) -> str:
        return f"[{self.start}:{self.end}] {self.text}"

    def __eq__(self, other) -> bool:
        if (
            isinstance(other, TextSpan)
            or hasattr(other, "sent") and hasattr(other, "start") and hasattr(other, "end")
        ):
            return (self.start, self.end, self.sent) == (other.start, other.end, other.sent)
        return NotImplemented


class BoundaryDetector:
    def __init__(
        self,
        lang: str = "en",
        *,
        include_char_span: bool = False,
        preserve_quote_and_paren: bool = True,
        verbose: bool = False,
    ):
        """Initialize the segmenter.

        Args:
            lang: Two chars ISO language code (e.g. en, fr, ...).
            include_char_span: Yield ``TextSpan`` objects with character
                spans instead of plain strings.
            preserve_quote_and_paren: Do not split on terminators inside
                quoted or parenthesised text.
            verbose: Enable verbose logging.
        """
        self.include_char_span = include_char_span
        self.preserve_quote_and_paren = preserve_quote_and_paren
        self.verbose = verbose
        self.lang = lang

    @property
    def lang(self) -> str:
        """ISO language code of the active rule set."""
        return self._lang

    @lang.setter
    def lang(self, lang: str) -> None:
        self._lang = lang
        self._load_rule(lang)

    def _load_rule(self, lang: str) -> None:
        """Dynamically import and instantiate the rule module for *lang*."""
        try:
            rule_module = import_module(f"yasbd.rules.{lang}_rules")
        except ModuleNotFoundError:
            raise ValueError(f"Unsupported language: {lang!r}") from None
        self._rule = getattr(rule_module, f"{lang.capitalize()}Rules")()

    def detect(
        self,
        text_data: str | Iterator[str],
        *,
        relative: bool = False,
    ) -> Generator[tuple[int, int], None, None]:
        """Detect sentence boundaries in text.

        Yields ``(start, end)`` character offset pairs for each
        detected sentence.

        Args:
            text_data: Plain text string or an iterable of lines
                (e.g. ``io.StringIO``).
            relative: If ``False`` (default), yield offsets relative to
                the full text. If ``True``, offsets are per-line.

        Yields:
            ``(start_offset, end_offset)`` for each sentence.
        """
        if isinstance(text_data, str):
            text_data = io.StringIO(text_data)

        # Quick heuristic empty check
        first_5_lines = list(islice(text_data, 5))
        if len(first_5_lines) == 0:
            if self.verbose:
                logger.info("Input is empty. Returns empty result")
            return

        # Re-stich the stream
        text_data = chain(first_5_lines, text_data)

        yield from self._rule.apply(
            text_data, self.preserve_quote_and_paren, relative=relative
        )

    def segment(
        self,
        text_data: str | Iterator[str],
        *,
        preserve_whitespace: bool = False,
    ) -> Generator[str, None, None]:
        """Split text into sentences.

        Args:
            text_data: Plain text string or an iterable of lines
                (e.g. ``io.StringIO``).
            preserve_whitespace: If ``False`` (default), strip leading and
                trailing whitespace from each sentence.

        Yields:
            Individual sentences as strings.
        """
        if isinstance(text_data, str):
            text_data = io.StringIO(text_data)

        input_for_detection, input_for_slicing = tee(text_data)
        line_gen = (line for line in input_for_slicing if line.strip())
        curr_line = None
        for start, end in self.detect(input_for_detection, relative=True):
            if start == 0:
                curr_line = next(line_gen, None)

            if curr_line is None:
                break

            sent = curr_line[start:end]
            if not preserve_whitespace:
                sent = sent.strip()
            yield sent
