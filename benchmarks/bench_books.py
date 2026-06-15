"""Benchmark all SBD libraries on full-length books."""

import time
import timeit

import requests
from bench_utils import all_segmenters
from rich.console import Console
from rich.table import Table

BOOKS = {
    "Alice in Wonderland": "https://github.com/kuemit/txt_book/raw/master/examples/alice_in_wonderland.txt",
    "Adventures of Sherlock Holmes": "https://www.gutenberg.org/ebooks/1661.txt.utf-8",
}

console = Console()


def fetch_text(url: str) -> str:
    """Download text from URL and decode."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


if __name__ == "__main__":
    # Download all books first
    texts = {}
    for name, url in BOOKS.items():
        console.print(f"Fetching [bold]{name}[/]...")
        texts[name] = fetch_text(url)
        console.print(f"  {len(texts[name]):,} chars\n")

    segmenters = all_segmenters(lang="en")

    for book_name, text in texts.items():
        table = Table(title=book_name)
        table.add_column("Library", style="cyan")
        table.add_column("Cold (ms)", justify="right")
        table.add_column("Warm (ms)", justify="right")
        table.add_column("Sentences", justify="right")

        for name, seg in sorted(segmenters.items()):
            seg.lang = "en"

            try:
                # Cold run
                t0 = time.perf_counter()
                sents = seg.segment(text)
                cold_ms = (time.perf_counter() - t0) * 1000

                # Warm run
                t = timeit.timeit(lambda s=seg, t=text: s.segment(t), number=5)
                warm_ms = t / 5 * 1000

                table.add_row(name, f"{cold_ms:.1f}", f"{warm_ms:.1f}", str(len(sents)))
            except Exception as e:
                err = str(e).split(".")[0]  # first sentence of error
                table.add_row(name, "ERR", "ERR", f"[{err}]")

        console.print(table)
        console.print()
