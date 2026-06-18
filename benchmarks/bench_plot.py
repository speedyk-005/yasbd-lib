"""Benchmark SBD libraries across text sizes and plot performance."""

import timeit
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from bench_utils import all_segmenters
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

warnings.filterwarnings("ignore")
console = Console()

# Configuration
BASE_TEXT = """\
Dear Professor Johnson, I am writing to formally request an extension on the upcoming
dissertation deadline. Pursuant to Section 4.3(a)(ii) of the university handbook
(see https://policies.example.edu/handbook.pdf), students are entitled to a 48-hour
grace period under extenuating circumstances. My advisor, Dr. A. B. Patel (M.D., Ph.D.),
can corroborate my claim if needed.

You can reach me at j.doe42@university.example.edu or visit my profile page at
https://www.example.com/~jdoe/about?ref=dept&v=2.0#contact.

As Smith et al. (2021, pp. 128-129) noted: "The implications of this discovery are
far-reaching (see also Jones & Lee, 2019; cf. Brown, 2018)." However, critics argue
that "the methodology employed was fundamentally flawed" -- a claim the authors vehemently
deny (see Appendix A, Fig. 7).

The witness testified: "He said -- and I quote -- 'I will not comply.' Then he turned
around and left. I couldn't believe it."

Copyright 2024 Example Corp. All rights reserved.\
"""

MULTIPLIERS = [1, 5, 10, 20, 50, 100, 200]
ITERS = 20
LANG = "en"

# Color scheme for libraries
COLORS = {
    "yasbd": "#0891b2",
    "pysbd": "#dc2626",
    "sentencex": "#16a34a",
    "sentsplit": "#9333ea",
    "nupunkt": "#ea580c",
    "blingfire": "#2563eb",
    "sentence-splitter": "#6b7280",
}


def run_benchmark():
    """Benchmark all segmenters across increasing text sizes."""
    segmenters = all_segmenters(lang=LANG)
    sizes = []
    results = {name: [] for name in segmenters}

    total_steps = len(MULTIPLIERS) * len(segmenters) * 2

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Benchmarking...", total=total_steps)

        for multiplier in MULTIPLIERS:
            text = BASE_TEXT * multiplier
            char_count = len(text)
            sizes.append(char_count)

            for name, seg in segmenters.items():
                seg.lang = LANG
                progress.update(
                    task, description=f"{multiplier:3d}x ({char_count:>7,} chars) {name}"
                )

                # Warmup
                seg.segment(text)
                progress.advance(task)

                # Timing
                elapsed = timeit.timeit(lambda s=seg, t=text: s.segment(t), number=ITERS)
                progress.advance(task)

                ms_per_iter = elapsed / ITERS * 1000
                results[name].append(ms_per_iter)

            # Print progress line
            times = "  ".join(f"{name}={results[name][-1]:.1f}ms" for name in segmenters)
            console.print(f"{multiplier:3d}x ({char_count:>7,} chars): {times}")

    # Plot results
    fig, ax = plt.subplots(figsize=(8, 5))

    for name, times in results.items():
        color = COLORS.get(name, "black")
        ax.fill_between(sizes, 0, times, color=color, alpha=0.08)
        ax.plot(sizes, times, "o-", label=name, color=color, linewidth=2, markersize=5)

    ax.set_xlabel("Characters", fontsize=12)
    ax.set_ylabel("ms / iteration", fontsize=12)
    ax.set_title("Sentence Boundary Detection Performance", fontsize=13)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(linestyle="--", alpha=0.5)
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:,.0f}")

    plt.tight_layout()
    output_path = Path("bench.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    console.print(f"\n[green]Saved {output_path.name}[/green]")


if __name__ == "__main__":
    run_benchmark()
