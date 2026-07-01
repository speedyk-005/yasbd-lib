import io
import random
import string

import pytest

from tests import ALL_TEST_DATA
from yasbd import (
    BoundaryDetector,
    InvalidInputError,
    ParagraphEOF,
    UnsupportedLanguageError,
)


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


@pytest.mark.parametrize(
    "lang,exc,msg",
    [
        (None, InvalidInputError, "'lang' is required"),
        ("", InvalidInputError, "'lang' is required"),
        ("xx", UnsupportedLanguageError, "doesn't fit any cutting profile"),
    ],
)
def test_invalid_lang(lang, exc, msg):
    with pytest.raises(exc, match=msg):
        BoundaryDetector(lang=lang)


def test_segment_different_input(en_detector):
    """test that string and stream input produce identical results."""
    text = "Hello world. How are you? I'm fine."

    result_str = list(en_detector.segment(text))
    result_stream = list(en_detector.segment(io.StringIO(text)))

    assert result_stream == result_str
    assert result_stream == ["Hello world.", "How are you?", "I'm fine."]


def test_segment_coordinate_direction_sentence_end(en_detector):
    """test that coordinate direction abbreviations can terminate sentences."""
    text = (
        "Server A was located at 40.7128° N, 74.0060° W. "
        "Server B was located at 34.0522° S, 118.2437° E."
    )

    assert list(en_detector.segment(text)) == [
        "Server A was located at 40.7128° N, 74.0060° W.",
        "Server B was located at 34.0522° S, 118.2437° E.",
    ]


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
        string.ascii_letters + string.digits + string.punctuation + "z.?! Dr. Mr. Inc. etc."
    )

    for _ in range(100):
        length = random.randint(1, 500)
        text = "".join(random.choices(chars, k=length))
        try:
            list(en_detector.segment(text))
        except Exception as e:
            raise AssertionError(f"Crash on random input (len={length}): {e}") from e


def test_detect_boundary_offsets(en_detector):
    """test that detect yields valid boundary offsets."""
    text = "Hello World. How are you?"

    result = list(en_detector.detect(text))
    assert result == [12, 25]
    assert all(isinstance(b, int) for b in result)
    assert result == sorted(result)


def test_detect_paragraph_eof_sentinel(en_detector):
    """test that detect yields ParagraphEOF between paragraphs in relative mode."""
    # Single paragraph = no sentinel
    result = list(en_detector.detect("Hello. World.", relative=True))
    assert result == [6, 13]

    # Empty paragraph = sentinel at start
    result = list(en_detector.detect("\n\nHello.", relative=True))
    assert result == [ParagraphEOF, 6]

    # Three paragraphs = two sentinels
    result = list(en_detector.detect("Hi.\n\nBye.\n\nOh.", relative=True))
    assert result == [3, ParagraphEOF, 4, ParagraphEOF, 3]

    # Non-relative = no sentinels,
    result = list(en_detector.detect("First.\n\nSecond.", relative=False))
    assert result == [6, 15]


def test_rule_cache_lru(en_detector):
    """test that rule objects are cached (max 5) and reused on lang switch."""
    # Same lang = same cached object
    r1 = en_detector._get_rule("en")
    r2 = en_detector._get_rule("en")
    assert r1 is r2, "same lang should return cached rule"

    # Different lang = different object
    r_fr = en_detector._get_rule("fr")
    assert r1 is not r_fr, "different lang should return different rule object"

    # Switch back = cached
    r3 = en_detector._get_rule("en")
    assert r1 is r3, "switching back to cached lang should reuse cached rule"

    # LRU eviction: load 5 more languages (cache capacity is 5)
    for lang in ["de", "es", "ht", "ar", "ja"]:
        en_detector._get_rule(lang)
    # 'en' was the first loaded, then pushed out by 5 newer entries
    r_en = en_detector._get_rule("en")
    assert r_en is not r1, "en should have been evicted after 6 other langs"
    assert type(r_en) is type(r1), "freshly loaded en rule should exist"  # type: ignore[unreachable]
