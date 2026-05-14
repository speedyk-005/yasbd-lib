import pytest
from yasbd import Segmenter
from tests import ALL_TEST_DATA


@pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
def test_segment(subtests, lang, test_data):
    seg = Segmenter(lang=lang, should_clean=True)
    for input_text, expected in test_data:
        with subtests.test():
            result = list(seg.segment(input_text))
            assert result == expected, f"Input: {input_text}"

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
