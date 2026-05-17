import io
from collections.abc import Generator, Iterable
from importlib import import_module
from itertools import chain, islice, tee

from loguru import logger
from typeguard import typechecked


class BoundaryDetector:
    @typechecked
    def __init__(
        self,
        lang: str = "en",
        *,
        preserve_quote_and_paren: bool = True,
        verbose: bool = False,
    ):
        """Initialize the segmenter.

        Args:
            lang: Two chars ISO language code (e.g. en, fr, ...).
            preserve_quote_and_paren: Do not split on terminators inside
                quoted or parenthesised text.
            verbose: Enable verbose logging.
        """
        self.preserve_quote_and_paren = preserve_quote_and_paren
        self.verbose = verbose
        self.lang = lang.lower()
        if self.verbose:  # pragma: no cover
            logger.info(
                "Initialized with lang={!r}, preserve_quote_and_paren={}, verbose={}",
                self._lang,
                self.preserve_quote_and_paren,
                self.verbose,
            )

    @property
    def lang(self) -> str:
        """ISO language code of the active rule set."""
        return self._lang

    @lang.setter
    def lang(self, lang: str) -> None:
        lang = lang.lower()
        old_lang = getattr(self, "_lang", None)
        if lang == old_lang:
            return

        self._load_rule(lang)
        self._lang = lang
        if self.verbose:  # pragma: no cover
            logger.info("Language switched from {} to {}", old_lang, self._lang)

    def _load_rule(self, lang: str) -> None:
        """Dynamically import and instantiate the rule module for *lang*."""
        if self.verbose:  # pragma: no cover
            logger.info("Trying to load rule module for {}", lang)

        try:
            rule_module = import_module(f"yasbd.rules.{lang}_rules")
        except ModuleNotFoundError:
            raise ValueError(f"Unsupported language: {lang!r}") from None

        self._rule = getattr(rule_module, f"{lang.capitalize()}Rules")()

    @typechecked
    def detect(
        self,
        text_data: Iterable[str],
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
        if self.verbose:  # pragma: no cover
            logger.info(
                "Called with type={}, relative={}", type(text_data).__name__, relative
            )

        if isinstance(text_data, str):
            text_data = io.StringIO(text_data)

        # Quick heuristic empty check
        first_5_lines = list(islice(text_data, 5))
        if len(first_5_lines) == 0:
            if self.verbose:  # pragma: no cover
                logger.info("Input is empty. Returns empty result")
            return

        # Re-stich the stream
        text_data = chain(first_5_lines, text_data)

        yield from self._rule.apply(
            text_data, self.preserve_quote_and_paren, relative=relative
        )

    @typechecked
    def segment(
        self,
        text_data: Iterable[str],
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
        if self.verbose:  # pragma: no cover
            logger.info("Called with preserve_whitespace={}", preserve_whitespace)

        if isinstance(text_data, str):
            text_data = io.StringIO(text_data)

        input_for_detection, input_for_slicing = tee(text_data)
        curr_line = None
        for start, end in self.detect(input_for_detection, relative=True):
            if start == 0:
                curr_line = next(input_for_slicing, None)

            if curr_line is None:
                break

            sent = curr_line[start:end]
            if not preserve_whitespace:
                sent = sent.strip()
                if not sent:
                    continue
            yield sent
