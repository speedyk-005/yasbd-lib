import io
from collections.abc import Generator
from importlib import import_module
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


class Segmenter:
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

    def _is_empty(self, input):
        """Check whether *input* contains any text without consuming it."""
        if isinstance(input, str):
            return not input.strip()

        if hasattr(input, 'peek'):
            return not input.peek(1)

        if hasattr(input, 'seekable') and input.seekable():
            curr = input.tell()
            exists = bool(input.read(1))
            input.seek(curr)
            return not exists

        return False

    def segment(
        self,
        text_or_stream: str | io.IOBase,
        *,
        preserve_whitespace: bool = False,
    ) -> Generator[str | TextSpan, None, None]:
        """Split text into sentences.

        Args:
            text_or_stream: Plain text string or an iterable of lines
                (e.g. ``io.StringIO``).
            preserve_whitespace: If ``False`` (default), strip leading and
                trailing whitespace from each sentence.

        Yields:
            Individual sentences as strings, or ``TextSpan`` objects when
            ``include_char_span`` is ``True``.
        """
        if self._is_empty(text_or_stream):
            if self.verbose:
                logger.info("Input is empty. Returns empty result")
            return

        line_iter = io.StringIO(text_or_stream) if isinstance(text_or_stream, str) else text_or_stream

        for sent, span in self._rule.apply(line_iter, self.preserve_quote_and_paren):
            if not preserve_whitespace:
                sent = sent.strip()
            yield (
                TextSpan(start=span[0], end=span[1], text=sent)
                if self.include_char_span else sent
            )
