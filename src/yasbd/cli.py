import json
import os
import stat
import sys
from pathlib import Path
from typing import Optional

from radicli import Arg, Radicli

from yasbd import BoundaryDetector, ParagraphEOF, __version__, get_supported_langs

cli = Radicli(
    prog="yasbd",
    help="Yet Another Sentence Boundary Detector. "
    "Split text into sentences with multilingual support.",
)


def _stdin_is_pipe() -> bool:
    """Check if stdin is a pipe or redirected file (not a TTY)."""
    return not stat.S_ISCHR(os.fstat(0).st_mode)


def _stdout_is_pipe() -> bool:
    """Check if stdout is a pipe (redirected to another process)."""
    return stat.S_ISFIFO(os.fstat(1).st_mode)


def _resolve_input(text: Optional[str], file: Optional[str]) -> str:
    """Resolve input text from a positional string, --file option, or stdin pipe."""
    if text and file:
        print("Error: provide text argument or --file, not both.", file=sys.stderr)
        sys.exit(1)
    if not text and not file:
        if _stdin_is_pipe():
            return sys.stdin.read()
        print("Error: provide text argument or --file.", file=sys.stderr)
        sys.exit(1)
    return text or Path(file).read_text(encoding="utf-8")


def _to_json(no: int, item) -> str:
    if item is ParagraphEOF:
        return json.dumps({"no": no, "eof": True})
    if isinstance(item, int):
        return json.dumps({"no": no, "offset": item})
    return json.dumps({"no": no, "text": item})


def _output(items, destination: Optional[str], *, label: str):
    """Write enumerated items to stdout or JSONL to a file."""
    count = 0
    if destination:
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
        "--preserve-whitespace", help="Preserve original whitespace in output."
    ),
    verbose=Arg("--verbose", help="Enable verbose logging."),
)
def segment(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    lang: str = "en",
    preserve_whitespace: bool = False,
    verbose: bool = False,
):
    """Split text into sentences."""
    input_text = _resolve_input(text, file)
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
    relative=Arg("--relative", help="Yield paragraph-relative offsets."),
    verbose=Arg("--verbose", help="Enable verbose logging."),
)
def detect(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    lang: str = "en",
    relative: bool = False,
    verbose: bool = False,
):
    """Detect sentence boundary offsets (character positions)."""
    input_text = _resolve_input(text, file)
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
    verbose=Arg("--verbose", help="Enable verbose logging."),
)
def clean(
    text: Optional[str] = None,
    file: Optional[str] = None,
    destination: Optional[str] = None,
    steps_to_skip: Optional[str] = None,
    verbose: bool = False,
):
    """Clean and normalize noisy text paragraphs."""
    input_text = _resolve_input(text, file)

    skip = set(s.strip() for s in steps_to_skip.split(",")) if steps_to_skip else None

    # lazy import to avoid pulling in ftfy et al. for other commands
    from yasbd.utils.cleaner import StreamCleaner

    _output(StreamCleaner(input_text, steps_to_skip=skip), destination, label="paragraph(s)")


@cli.command("langs")
def langs():
    """List supported language codes."""
    print(", ".join(get_supported_langs()))


def main():
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"yasbd v{__version__}")
        sys.exit(0)
    cli.run()


if __name__ == "__main__":
    main()
