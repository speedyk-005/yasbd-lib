import json
import os
import shlex
import stat
import subprocess
import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from io import TextIOBase
from typing import Optional

from radicli import Arg, Radicli

from yasbd import BoundaryDetector, ParagraphEOF, __version__, get_supported_langs

cli = Radicli(
    prog="yasbd",
    help="Yet Another Sentence Boundary Detector. "
    "Split text into sentences with multilingual support.",
)

_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_RESET = "\033[0m"

# fmt: off
_LOGO_YA = [
    "╦ ╦ ╔═╗",
    "╚╦╝ ╠═╣",
    " ╩  ╩ ╩"
]
_LOGO_SBD = [
    " ╔═╗ ╔╗  ╔╦╗",
    " ╚═╗ ╠╩╗  ║║",
    " ╚═╝ ╚═╝ ═╩╝"
]
# fmt: on


def _logo_colored() -> str:
    """Return the logo with ANSI color, plain when piped."""
    if _stdout_is_pipe():
        return "\n".join(a + b for a, b in zip(_LOGO_YA, _LOGO_SBD, strict=True))
    lines = [
        f"{_YELLOW}{y}{_CYAN}{s}{_RESET}" for y, s in zip(_LOGO_YA, _LOGO_SBD, strict=True)
    ]
    return "\n".join(lines)


def _version() -> str:
    """Return the colored logo + version string for --version output."""
    return f"{_logo_colored()}   v{__version__}"


def _stdin_is_pipe() -> bool:
    """Check if stdin is a pipe or redirected file (not a TTY)."""
    return not stat.S_ISCHR(os.fstat(0).st_mode)


def _stdout_is_pipe() -> bool:
    """Check if stdout is a pipe (redirected to another process)."""
    return stat.S_ISFIFO(os.fstat(1).st_mode)


def _create_external_cleaner(
    command_str: str, timeout: int | None = None
) -> Callable[[str], str]:
    """Create a cleaner function from a shell command string.

    The command receives text on stdin and must output cleaned text on stdout.

    Args:
        command_str: Shell command to execute (e.g., ``"sed 's/foo/bar/g'"``).
        timeout: Optional timeout in seconds for each call.

    Returns:
        A callable that accepts a string and returns the cleaned string.

    Example:
        >>> cleaner = _create_external_cleaner("tr 'a-z' 'A-Z'")
        >>> cleaner("hello")
        'HELLO'
    """
    command_list = shlex.split(command_str)

    def external_cleaner(text: str) -> str:
        try:
            process = subprocess.run(
                command_list,
                shell=False,
                input=text,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
            )
            return process.stdout.removesuffix("\n")

        except subprocess.TimeoutExpired:
            print(f"Cleaner command timed out after {timeout}s", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error executing cleaner command: {e}", file=sys.stderr)
            sys.exit(1)

    return external_cleaner


@contextmanager
def _resolve_input(
    text: Optional[str], file: Optional[str]
) -> Generator[str | TextIOBase, None, None]:
    """Context manager that yields input as text string or opened file handle.

    Yields a string for positional text argument, or an opened file object
    for --file/pipe (zero-copy, passed directly to BoundaryDetector).
    File handles are closed on context exit.

    >>> with _resolve_input("Hello.", None) as s:
    ...     s
    'Hello.'
    >>> with _resolve_input("hi", "f.txt"):  # doctest: +IGNORE_EXCEPTION_DETAIL
    ...     pass
    Traceback (most recent call last):
    SystemExit
    """
    if text is not None and file is not None:
        print("Error: provide text argument or --file, not both.", file=sys.stderr)
        sys.exit(1)
    if text is None and file is None:
        if _stdin_is_pipe():
            yield sys.stdin
            return
        print("Error: provide text argument or --file.", file=sys.stderr)
        sys.exit(1)
    if file is not None:
        f = open(file, encoding="utf-8")  # noqa: SIM115
        try:
            yield f
        finally:
            f.close()
    else:
        yield text


def _to_json(no: int, item) -> str:
    """Serialize an output item to one JSONL line.

    >>> _to_json(1, "Hello.")
    '{"no": 1, "text": "Hello."}'
    >>> _to_json(1, 6)
    '{"no": 1, "offset": 6}'
    >>> from yasbd import ParagraphEOF
    >>> _to_json(3, ParagraphEOF)
    '{"no": 3, "eof": true}'
    """
    if item is ParagraphEOF:
        return json.dumps({"no": no, "eof": True})
    if isinstance(item, int):
        return json.dumps({"no": no, "offset": item})
    return json.dumps({"no": no, "text": item})


def _output(items, destination: Optional[str], *, label: str):
    """Write enumerated items to stdout or JSONL to a file.

    >>> _output(["A.", "B."], None, label="test")  # doctest: +SKIP
    [1] 'A.'
    [2] 'B.'
    >>> _output(["Hi.", ParagraphEOF, "There."], None, label="test")  # doctest: +SKIP
    [1] 'Hi.'
    ---
    [3] 'There.'
    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl")
    >>> _output(["A.", "B.", "C."], tmp.name, label="test")
    >>> os.path.getsize(tmp.name) > 0
    True
    >>> open(tmp.name).read()
    '{"no": 1, "text": "A."}\\n{"no": 2, "text": "B."}\\n{"no": 3, "text": "C."}\\n'
    >>> os.unlink(tmp.name)
    """
    if destination:
        count = 0
        with open(destination, "w", encoding="utf-8") as f:
            for i, item in enumerate(items, 1):
                f.write(_to_json(i, item) + "\n")
                count += 1
        print(
            f"Wrote {count} {label} to {destination}",
            file=sys.stderr,
        )
    elif _stdout_is_pipe():
        for item in items:
            print(item)
    else:
        for i, item in enumerate(items, 1):
            if item is ParagraphEOF:
                print("---")
            else:
                print(f"[{i}] {item!r}")


@cli.command(
    "segment",
    text=Arg(help="Text to split. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination", "-d", help="Write output to a file."),
    lang=Arg("--lang", "-l", help="Language code (e.g., 'en', 'fr', 'de')."),
    preserve_whitespace=Arg(
        "--preserve-whitespace", "-w", help="Preserve original whitespace in output."
    ),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def segment(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    lang: str = "en",
    preserve_whitespace: bool = False,
    verbose: bool = False,
):
    """Split text into sentences.

    Reads from a positional string, --file, or stdin pipe.
    Writes enumerated sentences to stdout or JSONL to --destination.
    """
    with _resolve_input(text, file) as input_text:
        detector = BoundaryDetector(lang=lang, preserve_quote_and_paren=True, verbose=verbose)
        _output(
            detector.segment(input_text, preserve_whitespace=preserve_whitespace),
            destination,
            label="sentence(s)",
        )


@cli.command(
    "detect",
    text=Arg(help="Text to detect boundaries in. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination", "-d", help="Write boundary offsets to a file."),
    lang=Arg("--lang", "-l", help="Language code (e.g., 'en', 'fr', 'de')."),
    relative=Arg("--relative", "-r", help="Yield paragraph-relative offsets."),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def detect(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    lang: str = "en",
    relative: bool = False,
    verbose: bool = False,
):
    """Detect sentence boundary offsets (character positions).

    Reads from a positional string, --file, or stdin pipe.
    Writes boundary offsets to stdout or JSONL to --destination.
    Use --relative for per-paragraph offsets (ParagraphEOF marks gaps).
    """
    with _resolve_input(text, file) as input_text:
        detector = BoundaryDetector(lang=lang, preserve_quote_and_paren=True, verbose=verbose)
        _output(
            detector.detect(input_text, relative=relative),
            destination,
            label="boundary offset(s)",
        )


@cli.command(
    "clean",
    text=Arg(help="Text to clean. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination", "-d", help="Write cleaned text to a file."),
    steps_to_skip=Arg(
        "--steps-to-skip", "--skip", help="Comma-separated cleaning steps to skip."
    ),
    extra_step=Arg(
        "--extra-step",
        "-e",
        help="External shell command to run as an extra cleaning step (repeatable).",
    ),
    verbose=Arg("--verbose", "-v", help="Enable verbose logging."),
)
def clean(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    steps_to_skip: Optional[str] = None,
    extra_step: Optional[list[str]] = None,
    verbose: bool = False,
):
    """Clean and normalize noisy text paragraphs.

    Applies ftfy mojibake fixing, OCR cleanup, HTML tag stripping,
    slash normalization, and whitespace normalization.
    Use --skip to omit specific steps (comma-separated).
    Use --extra-step to run external shell commands as extra cleaning steps.
    """
    with _resolve_input(text, file) as input_text:
        skip = {s.strip() for s in steps_to_skip.split(",")} if steps_to_skip else None

        extra_steps = None
        if extra_step:
            extra_steps = [_create_external_cleaner(cmd) for cmd in extra_step]

        # lazy import to avoid pulling in ftfy et al. for other commands
        from yasbd.utils.cleaner import StreamCleaner

        _output(
            StreamCleaner(
                input_text, steps_to_skip=skip, extra_steps=extra_steps, verbose=verbose
            ),
            destination,
            label="paragraph(s)",
        )


@cli.command("langs")
def langs():
    """List supported language codes."""
    print(", ".join(get_supported_langs()))


def main():
    """CLI entry point. Handles --version, --help, and dispatches to radicli."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-v"):
        print(_version())
        sys.exit(0)
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h")):
        print(_logo_colored(), end="\n\n")
    cli.run()


if __name__ == "__main__":
    main()
