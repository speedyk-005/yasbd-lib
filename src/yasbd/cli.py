import sys
from pathlib import Path
from typing import Optional

from radicli import Arg, Radicli

from yasbd import BoundaryDetector, __version__, get_supported_langs

cli = Radicli(
    prog="yasbd",
    help="Yet Another Sentence Boundary Detector. "
    "Split text into sentences with multilingual support.",
)


def _resolve_input(text: Optional[str], file: Optional[str]) -> str:
    """Resolve input text from a positional string or --file option. Mutually exclusive."""
    if text and file:
        print("Error: provide text argument or --file, not both.", file=sys.stderr)
        sys.exit(1)
    if not text and not file:
        print("Error: provide text argument or --file.", file=sys.stderr)
        sys.exit(1)
    return text or Path(file).read_text(encoding="utf-8")


def _output(items, destination: Optional[str], *, label: str):
    """Write enumerated items to stdout or pipe-separated to a file."""
    count = 0
    if destination:
        with open(destination, "w", encoding="utf-8") as f:
            first = True
            for item in items:
                if first:
                    f.write(str(item))
                    first = False
                else:
                    f.write(" | " + str(item))
                count += 1
            f.write("\n")
        print(
            f"Wrote {count} {label} to {destination} separated by ' | '",
            file=sys.stderr,
        )
    else:
        for i, item in enumerate(items, 1):
            print(f"[{i}] {item!r}")


@cli.command(
    "segment",
    text=Arg(help="Text to split. Use --file to read from a file instead."),
    file=Arg("--file", "-f", help="Read input from a text file."),
    destination=Arg("--destination", "-d", help="Write output to a file."),
    lang=Arg("--lang", "-l", help="Language code (e.g., 'en', 'fr', 'de')."),
    preserve_whitespace=Arg("--preserve-whitespace", help="Preserve original whitespace in output."),
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
