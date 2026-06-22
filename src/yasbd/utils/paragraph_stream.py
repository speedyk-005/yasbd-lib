from collections.abc import Iterator
from io import StringIO, TextIOBase

from yasbd.utils.cleaner_stub import StreamCleanerStub
from yasbd.utils.input_validator import validate_input


class ParagraphStream:
    """An iterator that groups lines of text into paragraph blocks.

    This class implements Python's Iterator Protocol (__iter__ and __next__),
    retaining state across calls and yielding reconstructed paragraph blocks.

    Examples:
        >>> streamer = ParagraphStream('Hello\\n\\nWorld', skip_empty_lines=False)
        >>> list(streamer)
        ['Hello\\n\\n', 'World']

        >>> streamer = ParagraphStream('Hello\\n\\nWorld', skip_empty_lines=True)
        >>> list(streamer)
        ['Hello\\n', 'World']
    """

    @validate_input
    def __init__(
        self,
        source: str | TextIOBase | StreamCleanerStub,
        skip_empty_lines: bool = False,
    ) -> None:
        """Initialize ParagraphStream.

        Args:
            source: Input text as a string, ``TextIOBase`` stream, or ``StreamCleaner``.
            skip_empty_lines: If True, blank separator lines are omitted from paragraph blocks.
        """
        self.skip_empty_lines = skip_empty_lines

        # Normalise to an iterator so __next__ can call next() on it
        # StringIO works line-by-line and supports the iterator protocol natively
        self._lines = StringIO(source) if isinstance(source, str) else source
        self._line_iterator = iter(self._lines)

        # Stateful buffers to manage text stream boundaries across __next__ invocations
        self._buffer: list[str] = []
        self._is_flush_pending = False

    def __iter__(self) -> Iterator[str]:
        return self

    def close(self) -> None:
        """Close the underlying source stream if applicable."""
        if hasattr(self._lines, "close"):
            self._lines.close()

    def __del__(self) -> None:
        self.close()

    def _flush_eof(self) -> str:
        if self._buffer:
            paragraph = "".join(self._buffer)
            self._buffer = []
            return paragraph
        raise StopIteration

    def __next__(self) -> str:
        """Advance the stream and return the next paragraph.

        Yields paragraphs reconstructed as strings, preserving original line endings.

        Returns:
            The next complete paragraph string.

        Raises:
            StopIteration: When there are no more paragraphs to return.
        """
        while True:
            line = next(self._line_iterator, None)

            if line is None:
                return self._flush_eof()

            stripped_line = line.strip()

            # A blank line signals that the current paragraph is ending
            if not stripped_line:
                self._is_flush_pending = True

            # A non-blank line with a pending flush means we've crossed a paragraph
            # boundary. Emit the buffered paragraph (or drop it if empty + skip_empty_lines)
            if stripped_line and self._is_flush_pending:
                if not self._buffer and self.skip_empty_lines:
                    self._buffer = [line]
                    self._is_flush_pending = False
                    continue
                paragraph = "".join(self._buffer)
                self._buffer = [line]
                self._is_flush_pending = False
                return paragraph

            # When skip_empty_lines is active, skip blank separator lines
            # entirely instead of including them in the buffer.
            if self.skip_empty_lines and not stripped_line:
                continue

            self._buffer.append(line)


if __name__ == "__main__":  # pragma: no cover
    text = """Hello


    world"""

    # Correctly instantiate the iterable class and consume its stream
    para = ParagraphStream(text, False)
    for p in para:
        print(repr(p))
