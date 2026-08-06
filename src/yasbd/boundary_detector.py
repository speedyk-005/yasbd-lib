from collections import OrderedDict
from collections.abc import Callable, Generator, Iterable
from io import TextIOBase
from itertools import chain, pairwise, tee

from yasbd.exceptions import HookError, InvalidInputError
from yasbd.rules import get_supported_langs, load_rule
from yasbd.utils.cleaner_stub import StreamCleanerStub
from yasbd.utils.input_validator import validate_input
from yasbd.utils.language_classifier import classify_language
from yasbd.utils.logger import log_info
from yasbd.utils.paragraph_stream import ParagraphStream

# Signals transition between paragraphs in relative mode
# during boundary detection
ParagraphEOF = type("_ParagraphEOF", (), {"__repr__": lambda _: "ParagraphEOF"})()

# Confidence threshold for auto language detection
_MIN_CONFIDENCE = 0.8

# Maximum number of rule instances to keep in cache
_MAX_CACHED_RULES = 5


class BoundaryDetector:
    @validate_input
    def __init__(
        self,
        lang: str | None = None,
        *,
        preserve_quote_and_paren: bool = True,
        verbose: bool = False,
        hook: Callable[[dict[str, object]], None] | None = None,
    ):
        """Initialize the boundary detector.

        Args:
            lang: Two chars ISO language code (e.g., 'en', 'fr', ...).
                Use 'auto' for automatic language detection via py3langid.
                Explicit is faster and more reliable; use auto if you don't
                mind a slight decrease in both.
            preserve_quote_and_paren: Do not split on terminators inside
                quoted or parenthesised text.
            verbose: Enable verbose logging.
            hook: Optional per-paragraph post-processing callback. Receives
                a dict with ``text``, ``lang``, ``boundaries`` and
                ``paragraph_index`` keys; mutate ``boundaries`` (a list of
                paragraph-relative offsets) in place to add or remove
                sentence boundaries.
        """
        self.preserve_quote_and_paren = preserve_quote_and_paren
        self.verbose = verbose
        self.hook = hook
        self._rule_cache: OrderedDict[str, object] = OrderedDict()

        if not lang:
            raise InvalidInputError(
                f"'lang' is required.\nOptions: {', '.join(get_supported_langs())}"
            )
        self.lang = lang.lower()

        if self.lang == "auto":
            classify_language("MOCK")  # prime py3langid model

        log_info(
            self.verbose,
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

        if lang == "auto":
            self._lang = "auto"
            log_info(self.verbose, "Language set to auto-detection")
            return

        self._get_rule(lang)  # warm cache
        self._lang = lang
        log_info(self.verbose, "Language switched from {} to {}", old_lang, self._lang)

    def _get_rule(self, lang: str, snippet: str = "") -> object:
        """Return the rule object for *lang*, using a 5-entry LRU cache.

        When *lang* is ``"auto"``, language is detected from *snippet*
        using :func:`classify_language`.
        """
        if lang == "auto":
            lang, confidence = classify_language(snippet)
            if confidence < _MIN_CONFIDENCE:
                log_info(
                    self.verbose,
                    "Low confidence ({:.2f}) for detected lang {!r} in auto mode",
                    confidence,
                    lang,
                )

        if lang in self._rule_cache:
            self._rule_cache.move_to_end(lang)
            return self._rule_cache[lang]

        rule = load_rule(lang, verbose=self.verbose)
        self._rule_cache[lang] = rule

        if len(self._rule_cache) > _MAX_CACHED_RULES:
            self._rule_cache.popitem(last=False)

        return rule

    def _run_hook(self, text: str, boundaries: list[int], para_index: int) -> list[int]:
        """Run the user hook on *boundaries* for *text*, if configured.

        The hook mutates ``boundaries`` in place. Returns the (possibly
        re-sorted) list.
        """
        if self.hook is None:
            return boundaries
        ctx: dict[str, object] = {
            "text": text,
            "lang": self._lang,
            "boundaries": boundaries,
            "paragraph_index": para_index,
        }
        try:
            self.hook(ctx)
        except Exception as exc:
            raise HookError(
                f"post-processing hook raised an error: {exc!r}"
            ) from exc

        result = ctx["boundaries"]
        if not isinstance(result, list) or not all(
            isinstance(pos, int) and 0 <= pos <= len(text) for pos in result
        ):
            raise HookError(
                "post-processing hook must leave 'boundaries' as a list of "
                "int offsets within the paragraph"
            )
        return sorted(result)

    def _detect_relative_spans(
        self,
        para_iter: Iterable[str],
    ) -> Generator[tuple[int, int], None, None]:
        """Yield per-paragraph sentence spans."""
        first_para = next(para_iter, "")  # Needed for auto
        rule = self._get_rule(self._lang, first_para)

        for para_index, para in enumerate(chain([first_para], para_iter)):
            if not para or para.isspace():
                boundaries = [0, len(para)]
            else:
                boundaries = rule.apply(para, self.preserve_quote_and_paren)
                boundaries = self._run_hook(para, boundaries, para_index)
            yield from pairwise(boundaries)

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
        log_info(
            self.verbose,
            "Called with type={}, relative={}",
            type(source).__name__,
            relative,
        )

        para_iter = (
            ParagraphStream(source) if isinstance(source, (str, TextIOBase)) else source
        )

        offset = 0

        # Handle first para differently
        is_first_para = True
        first_para = next(para_iter, "")
        if relative and first_para.isspace():
            yield ParagraphEOF

        rule = self._get_rule(self._lang, first_para)

        for para_index, para in enumerate(chain([first_para], para_iter)):
            if para.isspace():
                continue

            if relative and not is_first_para:
                yield ParagraphEOF
            is_first_para = False

            stripped = para.rstrip()
            boundaries = rule.apply(stripped, self.preserve_quote_and_paren)
            boundaries = self._run_hook(stripped, boundaries, para_index)

            for pos in boundaries[1:]:
                yield offset + pos

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
            source: Plain text string or ``TextIOBase`` stream
                (e.g., ``StringIO``, opened file).
            preserve_whitespace: If ``False`` (default), strip leading and
                trailing whitespace from each sentence.

        Yields:
            Individual sentences as strings.
        """
        log_info(self.verbose, "Called with preserve_whitespace={}", preserve_whitespace)

        para_iter = (
            ParagraphStream(source, skip_empty_lines=not preserve_whitespace)
            if isinstance(source, (str, TextIOBase))
            else source
        )

        input_for_detection, input_for_slicing = tee(para_iter)
        curr_para = None
        for start, end in self._detect_relative_spans(input_for_detection):
            # start == 0 signals the first sentence span of a new paragraph.
            # At that signal we advance input_for_slicing to get the paragraph
            # text to slice from (both iterators advance in lockstep).
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
