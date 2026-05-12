import pytest
from yasbd import Segmenter
from tests import ALL_TEST_DATA


class TestSegmenter:
    def test_include_char_span(self):
        seg = Segmenter(lang="en", include_char_span=True)
        result = list(seg.segment("Hello. World."))
        assert len(result) == 2
        assert result[0].text == "Hello."
        assert result[0].start == 0
        assert result[0].end == 6

    @pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
    def test_segment(self, subtests, lang, test_data):
        seg = Segmenter(lang=lang, should_clean=True)
        for input_text, expected in test_data:
            with subtests.test():
                result = list(seg.segment(input_text))
                assert result == expected, f"Input: {input_text}"
