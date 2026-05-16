import pytest

from yasbd.utils.pysbd_adapter import Segmenter, TextSpan


def test_segment_basic():
    seg = Segmenter(language="en")
    result = seg.segment("Hello world. How are you? I'm fine.")
    assert result == ["Hello world.", "How are you?", "I'm fine."]


def test_segment_empty():
    seg = Segmenter(language="en")
    assert seg.segment("") == []


def test_segment_with_newlines():
    seg = Segmenter(language="en")
    result = seg.segment("First.\n\nSecond.\nThird.")
    assert result == ["First.", "Second.", "Third."]


def test_char_span():
    seg = Segmenter(language="en", char_span=True)
    text = "Hello world. How are you?"
    result = seg.segment(text)
    assert len(result) == 2
    for ts in result:
        assert isinstance(ts, TextSpan)
        assert text[ts.start:ts.end] == ts.sent


def test_value_errors():
    with pytest.raises(ValueError, match="char_span must be False"):
        Segmenter(language="en", clean=True, char_span=True)
    with pytest.raises(ValueError, match="doc_type='pdf'"):
        Segmenter(language="en", doc_type="pdf")


def test_textspan():
    ts = TextSpan("hello", 0, 5)
    assert str(ts) == "[0:5] hello"
    assert ts == TextSpan("hello", 0, 5)
