import time

from yasbd.rules.base import Rules
from yasbd.rules.en_rules import EnRules


def test_regex_caching_performance():
    """test that compiled regex patterns are cached per class."""
    t0 = time.perf_counter()
    _ = EnRules()
    cold = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(100):
        _ = EnRules()
    cached = time.perf_counter() - t0

    assert cached / 100 <= 0.10 * cold, \
        f"cached instantiation too slow: {cached/100:.6f}s vs {cold:.6f}s (cold)"


def test_regex_caching_isolation():
    """test that base class caching does not poison subclass caching."""
    # Instantiate base class first
    _ = Rules()

    # EnRules must still compile its own patterns
    e = EnRules()
    assert "NAIVE_BOUNDARY_FINDER" in type(e).__dict__, \
        "EnRules should have its own NAIVE_BOUNDARY_FINDER, not inherit from Rules"
