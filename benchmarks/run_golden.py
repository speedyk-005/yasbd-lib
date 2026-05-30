"""Run all SBD libraries against EN_GOLDEN_DATA.py and report accuracy."""

from bench_utils import BaseSegmenter, all_segmenters
from EN_GOLDEN_DATA import GOLDEN_EN_RULES_TEST_CASES

report: list[dict] = []

segmenters: dict[str, BaseSegmenter] = all_segmenters(lang="en")

for name, seg in sorted(segmenters.items()):
    passed = 0
    total = len(GOLDEN_EN_RULES_TEST_CASES)
    failures: list[tuple[str, list[str], list[str]]] = []

    for input_text, expected in GOLDEN_EN_RULES_TEST_CASES:
        try:
            result = [s.strip() for s in seg.segment(input_text)]
        except Exception as e:
            result = [f"<ERROR: {e}>"]

        if result == expected:
            passed += 1
        else:
            failures.append((input_text, expected, result))

    pct = passed / total * 100
    report.append(
        {
            "name": name,
            "passed": passed,
            "total": total,
            "pct": pct,
            "failures": failures,
        }
    )

    print(f"{name:20s} {passed:2d}/{total} ({pct:5.1f}%)", end="")
    if failures:
        top = min(failures, key=lambda f: len(f[0]))  # shortest failing input
        print(f"  worst failure: {top[0][:60]!r}")
    else:
        print()

print()
print(f"{'Library':20s} {'Score':>8s}")
print("-" * 30)
for r in sorted(report, key=lambda x: -x["pct"]):
    print(f"{r['name']:20s} {r['passed']:2d}/{r['total']} ({r['pct']:5.1f}%)")
