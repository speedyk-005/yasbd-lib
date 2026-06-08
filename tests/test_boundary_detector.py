import io
import random
import string

import pytest

from tests import ALL_TEST_DATA
from yasbd import BoundaryDetector, ParagraphEOF


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
        BoundaryDetector(lang="xx")


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
