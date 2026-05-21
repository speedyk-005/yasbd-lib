import io
import random
import string
import time

import pytest

from tests import ALL_TEST_DATA
from yasbd import BoundaryDetector
from yasbd.rules.en_rules import EnRules


@pytest.fixture(scope="module")
def en_detector():
    return BoundaryDetector(lang="en")


@pytest.mark.parametrize(
    "input_text",
    [
        "",
        "   ",
        "\n\n\n",
        pytest.param(io.StringIO(""), id="empty_stream"),
    ],
)
def test_segment_empty_input(input_text, en_detector):
    """test that empty or whitespace-only input produces no sentences."""
    assert list(en_detector.segment(input_text)) == []


def test_unsupported_language():
    """test that unknown language codes raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported language"):
        BoundaryDetector(lang="ht")


def test_segment_different_input(en_detector):
    """test that string and stream input produce identical results."""
    text = "Hello world. How are you? I'm fine."

    result_str = list(en_detector.segment(text))
    result_stream = list(en_detector.segment(io.StringIO(text)))

    assert result_stream == result_str
    assert result_stream == ["Hello world.", "How are you?", "I'm fine."]


@pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
def test_segment_multiple_langs(subtests, lang, test_data):
    """test that each language's test data passes."""
    seg = BoundaryDetector(lang=lang)
    for marked_text in test_data:
        # Extract the expected sentences by splitting on the marker
        expected = [sent.strip() for sent in marked_text.split("|")]

        # Reconstruct the clean original input text by removing the marker
        input_text = marked_text.replace("|", "")

        with subtests.test():
            result = list(seg.segment(input_text))
            assert result == expected, f"Input: {input_text}"


def test_segment_noisy_input(en_detector):
    """test that random noisy input does not crash the segmenter."""
    chars = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + "z.?! Dr. Mr. Inc. etc."
    )

    for _ in range(100):
        length = random.randint(1, 500)
        text = "".join(random.choices(chars, k=length))
        try:
            list(en_detector.segment(text))
        except Exception as e:
            raise AssertionError(f"Crash on random input (len={length}): {e}") from e


def test_include_char_span(en_detector):
    """test that detect yields valid (start, end) offset pairs."""
    text = "Hello World. How are you?"

    result = list(en_detector.detect(text))
    assert len(result) == 2

    last_end = 0
    for start, end in result:
        assert text[start:end]
        assert last_end <= start
        assert start <= end
        last_end = end


def test_regex_caching():
    """test that compiled regex patterns are cached per class."""
    # Wipe cache to start fresh
    EnRules._REGEX_CACHED = False

    t0 = time.perf_counter()
    _ = EnRules()
    cold = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(100):
        _ = EnRules()
    cached = time.perf_counter() - t0

    assert cached / 100 <= 0.10 * cold, \
        f"cached instantiation too slow: {cached/100:.6f}s vs {cold:.6f}s (cold)"
