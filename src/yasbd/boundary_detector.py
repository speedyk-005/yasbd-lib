from collections.abc import Generator, Iterable
from importlib import import_module
from itertools import tee

from loguru import logger

from yasbd.utils.input_validator import validate_input
from yasbd.utils.paragraph_streamer import ParagraphStreamer


class BoundaryDetector:
    @validate_input
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

    @validate_input
    def detect(
        self,
        source: str | Iterable[str],
        *,
        relative: bool = False,
    ) -> Generator[tuple[int, int], None, None]:
        """Detect sentence boundaries in text.

        Yields ``(start, end)`` character offset pairs for each
        detected sentence.

        Args:
            source: Plain text string or an iterable of paragraphs.
            relative: If ``False`` (default), yield offsets relative to
                the full text. If ``True``, offsets are per-paragraph.

        Yields:
            ``(start_offset, end_offset)`` for each sentence.
        """
        if self.verbose:  # pragma: no cover
            logger.info(
                "Called with type={}, relative={}", type(source).__name__, relative
            )

        para_iter = ParagraphStreamer(source) if isinstance(source, str) else source
        yield from self._detect(para_iter, relative=relative)

    def _detect(
        self,
        para_iter: Iterable[str],
        *,
        relative: bool = False,
    ) -> Generator[tuple[int, int], None, None]:
        """Internal boundary detection.

        Args:
            para_iter: An iterable of paragraph strings.
            relative: If ``False``, yield offsets relative to
                the full text. If ``True``, offsets are per-paragraph.

        Yields:
            ``(start_offset, end_offset)`` for each sentence.
        """
        yield from self._rule.apply(
            para_iter, self.preserve_quote_and_paren, relative=relative
        )

    @validate_input
    def segment(
        self,
        source: str | Iterable[str],
        *,
        preserve_whitespace: bool = False,
    ) -> Generator[str, None, None]:
        """Split text into sentences.

        Args:
            source: Plain text string or an iterable of paragraphs.
            preserve_whitespace: If ``False`` (default), strip leading and
                trailing whitespace from each sentence.

        Yields:
            Individual sentences as strings.
        """
        if self.verbose:  # pragma: no cover
            logger.info("Called with preserve_whitespace={}", preserve_whitespace)

        para_iter = (
            ParagraphStreamer(source, skip_empty_lines=not preserve_whitespace)
            if isinstance(source, str) else source
        )

        input_for_detection, input_for_slicing = tee(para_iter)
        curr_para = None
        for start, end in self._detect(input_for_detection, relative=True):
            if start == 0:
                curr_para = next(input_for_slicing, None)

            if curr_para is None:
                break

            sent = curr_para[start:end]
            if not preserve_whitespace:
                sent = sent.strip()
                if not sent:
                    continue
            yield sent
