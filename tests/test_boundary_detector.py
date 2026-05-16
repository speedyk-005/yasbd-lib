import pytest
import io
import random
import string

from yasbd import BoundaryDetector
from tests import ALL_TEST_DATA


@pytest.mark.parametrize("input_text", [
    "",
    "   ",
    "\n\n\n",
    pytest.param(io.StringIO(""), id="empty_stream"),
])
def test_segment_empty_input(input_text):
    seg = BoundaryDetector(lang="en")
    assert list(seg.segment(input_text)) == []


def test_unsupported_language():
    with pytest.raises(ValueError, match="Unsupported language"):
        BoundaryDetector(lang="ht")


def test_segment_different_input():
    text = "Hello world. How are you? I'm fine."
    seg = BoundaryDetector(lang="en")

    result_str = list(seg.segment(text))
    result_stream = list(seg.segment(io.StringIO(text)))

    assert result_stream == result_str
    assert result_stream == ["Hello world.", "How are you?", "I'm fine."]


@pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
def test_segment_multiple_langs(subtests, lang, test_data):
    seg = BoundaryDetector(lang=lang)
    for input_text, expected in test_data:
        with subtests.test():
            result = list(seg.segment(input_text))
            assert result == expected, f"Input: {input_text}"


def test_segment_noisy_input():
    chars = string.ascii_letters + string.digits + string.punctuation + "z.?! Dr. Mr. Inc. etc."
    seg = BoundaryDetector(lang="en")

    for _ in range(100):
        length = random.randint(1, 500)
        text = "".join(random.choices(chars, k=length))
        try:
            list(seg.segment(text))
        except Exception as e:
            raise AssertionError(f"Crash on random input (len={length}): {e}")


def test_include_char_span():
    text = "Hello World. How are you?"

    seg = BoundaryDetector(lang="en")
    result = list(seg.detect(text))
    assert len(result) == 2

    last_end = 0
    for start, end in result:
        assert text[start:end]
        assert last_end <= start
        assert start <= end
        last_end = end

