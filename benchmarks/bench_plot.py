#!/usr/bin/env python
"""Benchmark all SBD libraries across text sizes and plot."""

import timeit
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from bench_utils import all_segmenters

warnings.filterwarnings("ignore")

BASE = """\
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

segs = all_segmenters(lang=LANG)

sizes = []
results = {name: [] for name in segs}

for m in MULTIPLIERS:
    text = BASE * m
    nchars = len(text)
    sizes.append(nchars)

    print(f"{m:4d}x ({nchars:>7,} chars):", end=" ", flush=True)

    for name, seg in segs.items():
        seg.lang = LANG

        # Warmup
        seg.segment(text)

        t = timeit.timeit(lambda s=seg, t=text: s.segment(t), number=ITERS)
        ms = t / ITERS * 1000
        results[name].append(ms)
        print(f"{name}={ms:.1f}ms", end="  ", flush=True)

    print()

# ── Plotting the Entire Ecosystem with Shaded Bounds ──

COLORS: dict[str, str] = {
    "yasbd": "#0891b2",
    "pysbd": "#dc2626",
    "sentencex": "#16a34a",
    "sentsplit": "#9333ea",
    "nupunkt": "#ea580c",
    "blingfire": "#2563eb",
    "sentence-splitter": "#6b7280",
}

fig, ax1 = plt.subplots(figsize=(8, 5))

# --- Calculate Global Min/Max Envelopes for Shading ---
min_times = [min(results[name][i] for name in results) for i in range(len(sizes))]
max_times = [max(results[name][i] for name in results) for i in range(len(sizes))]


# --- Absolute Processing Speed ---
ax1.fill_between(
    sizes,
    min_times,
    max_times,
    color="#64748b",
    alpha=0.1,
    label="Ecosystem Variance",
)

for name, times in results.items():
    ax1.plot(
        sizes,
        times,
        "o-",
        label=name,
        color=COLORS.get(name, "black"),
        linewidth=2,
        markersize=5,
    )

ax1.set_xlabel("Characters", fontsize=12)
ax1.set_ylabel("ms / iter", fontsize=12)
ax1.set_title("Absolute Time (warm)", fontsize=13)
ax1.legend(fontsize=9, loc="upper left")
ax1.grid(linestyle="--", alpha=0.5)
ax1.xaxis.set_major_formatter(lambda x, _: f"{x:,.0f}")

plt.tight_layout()
output_path = Path("bench.png")
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nSaved {output_path.name} with complete ecosystem variance shading.")
