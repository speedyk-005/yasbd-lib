from collections.abc import Iterable
from types import SimpleNamespace

from yasbd import BoundaryDetector
from yasbd.utils.cleaner import StreamCleaner
from yasbd.utils.input_validator import validate_input


class TextSpan:
    """A sentence with its character-offset span in the original text.

    Args:
        sent: Sentence text.
        start: Start character offset of a sentence in original text.
        end: End character offset of a sentence in original text.
    """

    def __init__(self, sent, start, end):
        self.sent = sent
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"[{self.start}:{self.end}] {self.sent}"

    def __eq__(self, other) -> bool:
        if (
            isinstance(other, TextSpan)
            or hasattr(other, "sent")
            and hasattr(other, "start")
            and hasattr(other, "end")
        ):
            return (self.start, self.end, self.sent) == (
                other.start,
                other.end,
                other.sent,
            )
        return NotImplemented


class Segmenter:
    @validate_input
    def __init__(
        self,
        language: str = "en",  # Match pysbd default
        clean: bool = False,
        doc_type: str | None = None,
        char_span: bool = False,
    ):
        """Initializes the Segmenter.

        Args:
            language: Two-character ISO 639-1 language code. Defaults to "en".
            clean: Whether to clean the original text. Defaults to False.
            doc_type: Normal text or OCRed text (e.g. "pdf"). Defaults to None.
            char_span: Whether to return character offset spans. Defaults to False.
        """
        if clean and char_span:
            raise ValueError(
                "char_span must be False if clean is True. "
                "Since `clean=True` will modify original text."
            )
        if doc_type == "pdf" and not clean:
            raise ValueError(
                "`doc_type='pdf'` should have `clean=True` & "
                "`char_span` should be False since original "
                "text will be modified."
            )
        self.clean = clean
        self.doc_type = doc_type
        self.char_span = char_span
        self._detector = BoundaryDetector(lang=language)

        # Legacy pysbd API compatibility mappings
        self.cleaner = lambda t: SimpleNamespace(clean=lambda: "".join(StreamCleaner(t)))
        self.processor = lambda t: SimpleNamespace(process=lambda: self._process_text(t))
        self.language_module = SimpleNamespace(ISO_CODE=language)

    @property
    def language(self) -> str:
        return self._detector.lang

    @language.setter
    def language(self, value: str):
        self._detector.lang = value
        self.language_module.ISO_CODE = value

    @staticmethod
    def _convert_leading_space_to_trails(sentences: list[str]) -> list[str]:
        """Move leading whitespace from each sentence to the previous sentence's tail.

        ``BoundaryDetector`` preserves inter-sentence whitespace (``\\n``,
        spaces) as *leading* whitespace on the following sentence. Pysbd
        compatibility expects it as *trailing* whitespace on the preceding
        sentence instead.
        """
        result = []
        for sent in sentences:
            if not result:
                stripped = sent.lstrip()
                if stripped:
                    result = [stripped]
                continue

            lead_ws = len(sent) - len(sent.lstrip())
            if lead_ws:
                result[-1] += sent[:lead_ws]
                sent = sent[lead_ws:]

            if sent:
                result.append(sent)
        return result

    def _process_text(self, text: str | Iterable[str]) -> list[str | TextSpan]:
        """Detect sentence boundaries in text."""
        if self.char_span:
            boundaries = list(self._detector.detect(text))

            res = []
            start = 0
            for end in boundaries:
                res.append(TextSpan(text[start:end], start, end))
                start = end
            return res

        if self.clean:
            sents = list(self._detector.segment(text))
            return sents
        else:
            sents = list(self._detector.segment(text, preserve_whitespace=True))
            return self._convert_leading_space_to_trails(sents)

    @validate_input
    def sentences_with_char_spans(self, sentences: list[str]) -> list[TextSpan]:
        """Map sentences to their char offsets using cumulative lengths.

        Pysbd compatibility method
        """
        pos = 0
        result = []
        for sent in sentences:
            result.append(TextSpan(sent, pos, pos + len(sent)))
            pos += len(sent)
        return result

    @validate_input
    def segment(self, text: str) -> list[str | TextSpan]:
        """Segments *text* into sentences.

        Args:
            text: Raw text to be segmented into sentences.

        Returns:
            A list of sentences (strings) by default, or a list of TextSpan
            objects if ``char_span`` was set to ``True``.
        """
        # Pysbd stored the original text in object
        # Keep a preview for compatibility for libs depending on it
        self.original_text = f"{text[:500]}..." if len(text) > 500 else text

        if self.clean:
            text = StreamCleaner(text)

        return self._process_text(text)
