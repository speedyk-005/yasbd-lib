import io
from types import SimpleNamespace

from yasbd import BoundaryDetector
from yasbd.utils.cleaner import clean_stream


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
            or hasattr(other, "sent") and hasattr(other, "start") and hasattr(other, "end")
        ):
            return (self.start, self.end, self.sent) == (other.start, other.end, other.sent)
        return NotImplemented


class Segmenter:
    def __init__(
        self,
        language: str ="en",
        clean: bool = False,
        doc_type: str | None = None,
        char_span: bool = False
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
        self.cleaner = lambda t: SimpleNamespace(clean=lambda: "".join(clean_stream(t)))
        self.processor = lambda t: SimpleNamespace(process=lambda: self._process_text(t))
        self.language_module = SimpleNamespace(ISO_CODE=language)

    @property
    def language(self) -> str:
        return self._detector.lang

    @language.setter
    def language(self, value: str):
        self._detector.lang = value
        self.language_module.ISO_CODE = value

    def _process_text(self, text: str) -> list[str | TextSpan]:
        """Internal worker to process raw text into strings or spans."""
        if self.char_span:
            return [
                TextSpan(text[start:end], start, end)
                for start, end in self._detector.detect(text)
            ]
        return list(self._detector.segment(text, preserve_whitespace=True))

    def sentences_with_char_spans(
        self, sentences: list[str]
    ) -> list[tuple[int, int]]:
        """Map sentences to their char offsets using cumulative lengths.

        Pysbd compatibility method
        """
        pos = 0
        result = []
        for sent in sentences:
            result.append(TextSpan(sent, pos, pos + len(sent)))
            pos += len(sent)
        return result

    def segment(self, text: str) -> list[str | TextSpan]:
        """Segments *text* into sentences.

        Args:
            text: Raw text to be segmented into sentences.

        Returns:
            A list of sentences (strings) by default, or a list of TextSpan
            objects if ``char_span`` was set to ``True``.
        """
        # Pysbd stored the original text in object
        # Keep a preview for compatibility, 
        self.original_text = f"{text[:500]}..." if len(text) > 125 else text

        if self.clean:
            return list(self._detector.segment(clean_stream(text)))

        return self._process_text(text)
