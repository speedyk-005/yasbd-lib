from bench_utils import all_segmenters
from EN_GOLDEN_DATA import GOLDEN_EN_RULES_TEST_CASES
from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def _score_color(pct: float) -> str:
    if pct > 80:
        return "green"
    if pct > 60:
        return "yellow"
    return "red"


def _evaluate_segmenter(seg, cases):
    passed = 0
    total = len(cases)
    failures = []
    for input_text, expected in cases:
        try:
            result = [s.strip() for s in seg.segment(input_text)]
        except Exception as e:
            result = [f"<ERROR: {e}>"]
        if result == expected:
            passed += 1
        else:
            failures.append((input_text, expected, result))
    return passed, total, failures


def run_golden_tests():
    """
    Validate SBD libraries against golden test cases.

    For each segmenter, runs all golden test cases and reports:
    - Pass/fail count per library
    - First failure example per library
    - Summary table sorted by accuracy

    Golden tests are the authoritative source of truth for expected behavior.
    """
    report: list[dict] = []
    segmenters = all_segmenters(lang="en")

    for name, seg in sorted(segmenters.items()):
        passed, total, failures = _evaluate_segmenter(seg, GOLDEN_EN_RULES_TEST_CASES)
        pct = passed / total * 100
        report.append(
            {"name": name, "passed": passed, "total": total, "pct": pct, "failures": failures}
        )

        console.print(f"{name:20s} {passed:2d}/{total} ({pct:5.1f}%)", end="")
        if failures:
            shortest_failure = min(failures, key=lambda f: len(f[0]))
            console.print(f"  worst: {shortest_failure[0][:60]!r}")
        else:
            console.print("  Perfect!")

    # Summary table sorted by accuracy (highest first)
    table = Table(title="Golden Test Results", box=box.ROUNDED, title_style="bold cyan")
    table.add_column("Library", style="cyan")
    table.add_column("Passed", justify="right")
    table.add_column("Score", justify="right", style="bold")

    for r in sorted(report, key=lambda x: -x["pct"]):
        color = _score_color(r["pct"])
        table.add_row(
            r["name"], f"{r['passed']:2d}/{r['total']}", f"[{color}]{r['pct']:5.1f}%[/{color}]"
        )

    console.print("\n", table)


if __name__ == "__main__":
    run_golden_tests()
