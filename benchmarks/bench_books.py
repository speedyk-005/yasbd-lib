"""Benchmark SBD libraries on full-length books.

Methodology (hybrid):
- Cold: fresh instance per library per book (init + first full segment).
- Warm: median of 10 single runs on that same instance (stall-proof).
"""

import statistics
import time

import requests
from bench_utils import (
    BlingfireWrapper,
    NupunktWrapper,
    PysbdWrapper,
    SentenceSplitterWrapper,
    SentencexWrapper,
    SentsplitWrapper,
    SpacySentencizerWrapper,
    YasbdWrapper,
)
from rich.console import Console
from rich.table import Table

BOOKS = {
    "Alice in Wonderland": "https://github.com/kuemit/txt_book/raw/master/examples/alice_in_wonderland.txt",
    "Adventures of Sherlock Holmes": "https://www.gutenberg.org/ebooks/1661.txt.utf-8",
}

WARM_RUNS = 5

FACTORIES = {
    "yasbd": lambda: YasbdWrapper(lang="en"),
    "pysbd": lambda: PysbdWrapper(lang="en"),
    "sentencex": lambda: SentencexWrapper(lang="en"),
    "sentsplit": lambda: SentsplitWrapper(lang="en"),
    "nupunkt": lambda: NupunktWrapper(lang="en"),
    "blingfire": lambda: BlingfireWrapper(lang="en"),
    "sentence-splitter": lambda: SentenceSplitterWrapper(lang="en"),
    "spacy-sentencizer": lambda: SpacySentencizerWrapper(lang="en"),
}

console = Console()


def fetch_text(url: str) -> str:
    """Download text from URL and decode."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def run_book_benchmark():
    """Benchmark all segmenters on full book texts."""
    # Download all books first
    texts = {}
    for name, url in BOOKS.items():
        console.print(f"Fetching [bold]{name}[/]...")
        texts[name] = fetch_text(url)
        console.print(f"  {len(texts[name]):,} chars\n")

    for book_name, text in texts.items():
        table = Table(title=book_name)
        table.add_column("Library", style="cyan")
        table.add_column("Cold (ms)", justify="right")
        table.add_column("Warm (ms)", justify="right")
        table.add_column("Sentences", justify="right")

        for name in sorted(FACTORIES):
            try:
                # Cold: fresh instance (init + first full segment)
                t0 = time.perf_counter()
                seg = FACTORIES[name]()
                sents = list(seg.segment(text))
                cold_ms = (time.perf_counter() - t0) * 1000

                # Warm: median of single runs on the same instance
                samples = []
                for _ in range(WARM_RUNS):
                    t0 = time.perf_counter()
                    list(seg.segment(text))
                    samples.append((time.perf_counter() - t0) * 1000)
                warm_ms = statistics.median(samples)

                table.add_row(name, f"{cold_ms:.1f}", f"{warm_ms:.1f}", str(len(sents)))
            except Exception as e:
                err = str(e).split(".")[0]  # First sentence of error
                table.add_row(name, "ERR", "ERR", f"[{err}]")

        console.print(table)
        console.print()


if __name__ == "__main__":
    run_book_benchmark()
