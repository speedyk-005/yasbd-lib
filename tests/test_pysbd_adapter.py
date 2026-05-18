import pytest

from yasbd.utils.pysbd_adapter import Segmenter, TextSpan


@pytest.fixture(scope="module")
def seg():
    return Segmenter()


def test_segment_basic(seg):
    """test that basic text splits into sentences preserving whitespace."""
    result = seg.segment("Hello world. How are you? I'm fine.")
    assert result == ["Hello world. ", "How are you? ", "I'm fine."]


def test_segment_empty(seg):
    """test that empty input returns empty list."""
    assert seg.segment("") == []


def test_segment_with_newlines(seg):
    """test that newlines are preserved in output sentences."""
    result = seg.segment("First.\n\nSecond.\nThird.")
    assert result == ["First.\n\n", "Second.\n", "Third."]


def test_char_span():
    """test that char_span returns TextSpan objects with correct offsets."""
    seg = Segmenter(char_span=True)
    text = "Hello world. How are you?"
    result = seg.segment(text)
    assert len(result) == 2
    for ts in result:
        assert isinstance(ts, TextSpan)
        assert text[ts.start : ts.end] == ts.sent


def test_char_span_incompatible_with_clean():
    """test that clean=True with char_span raises ValueError."""
    with pytest.raises(ValueError, match="char_span must be False"):
        Segmenter(language="en", clean=True, char_span=True)
    with pytest.raises(ValueError, match="doc_type='pdf'"):
        Segmenter(language="en", doc_type="pdf")


def test_textspan():
    """test that TextSpan has correct str and eq."""
    ts = TextSpan("hello", 0, 5)
    assert str(ts) == "[0:5] hello"
    assert ts == TextSpan("hello", 0, 5)


def test_sentences_with_char_spans():
    """test that sentences_with_char_spans computes cumulative offsets."""
    seg = Segmenter(language="en")
    sents = ["Hello world.", " How are you?", " I'm fine."]
    result = seg.sentences_with_char_spans(sents)
    assert len(result) == 3
    for i, ts in enumerate(result):
        assert isinstance(ts, TextSpan)
        assert ts.sent == sents[i]
    assert result[0] == TextSpan("Hello world.", 0, 12)
    assert result[1] == TextSpan(" How are you?", 12, 25)
    assert result[2] == TextSpan(" I'm fine.", 25, 35)
