from collections.abc import Generator, Iterable
from importlib import import_module
from io import TextIOBase
from itertools import tee

from loguru import logger

from yasbd.utils.cleaner_stub import StreamCleanerStub
from yasbd.utils.input_validator import validate_input
from yasbd.utils.paragraph_stream import ParagraphStream

# Signals transition between paragraphs in relative mode
# during boundary detection
ParagraphEOF = type("_ParagraphEOF", (), {"__repr__": lambda self: "ParagraphEOF"})()


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
            rule_module = import_module(f"yasbd.rules.{lang}")
        except ModuleNotFoundError:
            raise ValueError(f"Unsupported language: {lang!r}") from None

        self._rule = getattr(rule_module, f"{lang.capitalize()}Rules")()

    def _detect_relative_spans(
        self,
        para_iter: Iterable[str],
    ) -> Generator[tuple[int, int], None, None]:
        """Yield per-paragraph sentence spans."""
        for para in para_iter:
            if not para.strip():
                boundaries = [0, len(para)]
            else:
                boundaries = self._rule.apply(para, self.preserve_quote_and_paren)

            for i in range(len(boundaries) - 1):
                start = boundaries[i]
                end = boundaries[i + 1]
                yield (start, end)

    @validate_input
    def detect(
        self,
        source: str | TextIOBase | StreamCleanerStub,
        *,
        relative: bool = False,
    ) -> Generator[int, None, None]:
        """Detect sentence boundaries in the source text.

        Args:
            source: Plain text string, an open text stream (e.g., ``StringIO``),
               or a ``StreamCleaner`` instance.
            relative: If ``False`` (default), yields absolute character
                offsets from the beginning of the entire stream. If ``True``,
                offsets reset at each paragraph break, yielding indices relative
                to the start of the current paragraph.

        Note:
            When ``relative=True``, a ``ParagraphEOF`` sentinel is yielded
            between distinct paragraphs to signal the boundary of the local
            coordinate system. Import via: ``from yasbd import ParagraphEOF``.

        Yields:
            Integer boundary offsets or ``ParagraphEOF`` sentinels.
        """

        if self.verbose:  # pragma: no cover
            logger.info(
                "Called with type={}, relative={}", type(source).__name__, relative
            )

        para_iter = (
            ParagraphStream(source) if isinstance(source, (str, TextIOBase)) else source
        )

        offset = 0
        is_first_pos = True
        for para in para_iter:
            if not para.strip():
                if not relative:
                    offset += len(para)
                continue

            if relative and not is_first_pos:
                yield ParagraphEOF
            is_first_pos = False

            boundaries = self._rule.apply(para.rstrip(), self.preserve_quote_and_paren)

            for pos in boundaries[1:]:
                yield offset + pos if not relative else pos

            if not relative:
                offset += len(para)

    @validate_input
    def segment(
        self,
        source: str | TextIOBase | StreamCleanerStub,
        *,
        preserve_whitespace: bool = False,
    ) -> Generator[str, None, None]:
        """Split text into sentences.

        Args:
            source: Plain text string or ``TextIOBase`` stream (e.g., ``StringIO``, opened file).
            preserve_whitespace: If ``False`` (default), strip leading and
                trailing whitespace from each sentence.

        Yields:
            Individual sentences as strings.
        """
        if self.verbose:  # pragma: no cover
            logger.info("Called with preserve_whitespace={}", preserve_whitespace)

        para_iter = (
            ParagraphStream(source, skip_empty_lines=not preserve_whitespace)
            if isinstance(source, (str, TextIOBase))
            else source
        )

        input_for_detection, input_for_slicing = tee(para_iter)
        curr_para = None
        for start, end in self._detect_relative_spans(input_for_detection):
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
