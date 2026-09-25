"""Rerun warm-speed timings for every case in the README benchmark tables."""

import re
import timeit
from pathlib import Path

from bench_utils import all_segmenters
from rich.console import Console
from rich.table import Table

console = Console()
README = Path(__file__).with_name("README.md").read_text()

CASES = [
    ("complex_academic", "Complex academic text"),
    ("newline", "Newline continuation"),
    ("emoji", "Emoji boundaries"),
    ("chat", "Chat Log"),
    ("fr", "French"),
    ("ja", "Japanese"),
    ("pl", "Polish"),
    ("es", "Spanish"),
    ("el", "Greek"),
    ("ht", "Haitian Creole"),
]

LANGS = {
    "complex_academic": "en",
    "newline": "en",
    "emoji": "en",
    "chat": "en",
    "fr": "fr",
    "ja": "ja",
    "pl": "pl",
    "es": "es",
    "el": "el",
    "ht": "ht",
}


def extract_text(heading: str) -> str:
    """Grab the first ```txt fenced block following the given heading."""
    m = re.search(re.escape(heading) + r".*?```txt\n(.*?)```", README, re.S)
    if not m:
        raise ValueError(f"No txt block found for {heading!r}")
    return m.group(1).rstrip("\n")


def main():
    number = 10
    for key, heading in CASES:
        text = extract_text(heading)
        lang = LANGS[key]
        segmenters = all_segmenters(lang=lang)
        table = Table(title=f"{heading} ({lang}, {len(text):,} chars)")
        table.add_column("Library", style="cyan")
        table.add_column("Warm (ms)", justify="right")
        table.add_column("Sentences", justify="right")

        for name, seg in segmenters.items():
            try:
                sents = seg.segment(text)
                elapsed = timeit.timeit(lambda s=seg, t=text: s.segment(t), number=number)
                ms = elapsed / number * 1000
                table.add_row(name, f"{ms:.2f}", str(len(sents)))
                console.print(f"  {name:20s} {ms:.2f}ms ({len(sents)} sents)")
            except Exception as e:
                err = str(e).split(".")[0]
                table.add_row(name, "ERR", f"[{err}]")
                console.print(f"  {name:20s} ERROR: {err}", style="red")

        console.print(table)
        console.print()


if __name__ == "__main__":
    main()