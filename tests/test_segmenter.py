import pytest
import io
import random
import string

from yasbd import Segmenter
from tests import ALL_TEST_DATA


@pytest.mark.parametrize("input_text", [
    "",
    "   ",
    "\n\n\n",
    pytest.param(io.StringIO(""), id="empty_stream"),
])
def test_segment_empty_input(input_text):
    seg = Segmenter(lang="en", should_clean=True)
    assert list(seg.segment(input_text)) == []


def test_unsupported_language():
    with pytest.raises(ValueError, match="Unsupported language"):
        Segmenter(lang="ht")


def test_segment_different_input():
    text = "Hello world. How are you? I'm fine."
    seg = Segmenter(lang="en", should_clean=True)

    result_str = list(seg.segment(text))
    result_stream = list(seg.segment(io.StringIO(text)))

    assert result_stream == result_str
    assert result_stream == ["Hello world.", "How are you?", "I'm fine."]


@pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
def test_segment_multiple_langs(subtests, lang, test_data):
    seg = Segmenter(lang=lang, should_clean=True)
    for input_text, expected in test_data:
        with subtests.test():
            result = list(seg.segment(input_text))
            assert result == expected, f"Input: {input_text}"


def test_segment_noisy_input():
    chars = string.ascii_letters + string.digits + string.punctuation + "z.?! Dr. Mr. Inc. etc."
    seg = Segmenter(lang="en", should_clean=True)

    for _ in range(100):
        length = random.randint(1, 500)
        text = "".join(random.choices(chars, k=length))
        try:
            list(seg.segment(text))
        except Exception as e:
            raise AssertionError(f"Crash on random input (len={length}): {e}")


def test_include_char_span():
    text = "Hello World. How are you?"
    n = len(text)

    seg = Segmenter(lang="en", include_char_span=True)
    result = list(seg.segment(text))
    assert len(result) == 2

    last_end = 0
    for res in result:
        assert res.text == text[res.start:res.end]
        assert last_end <= res.start <= n
        assert last_end <= res.end <= n
        last_end = res.end


def test_clean_with_char_span_raises():
    seg = Segmenter(lang="en", should_clean=True, include_char_span=True)
    with pytest.raises(ValueError, match="include_char_span must be False"):
        list(seg.segment("Hello. World."))
        last_end = res.end
