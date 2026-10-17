import pytest

from examples.text_chunking import chunk_text
from yasbd import BoundaryDetector


# fmt: off
@pytest.mark.parametrize(
    "marked_text",
    [
        # Ordinary word + period should not be treated as vertical list marker
        "Note.| The file is ready.",

        # Basic html tags
        "<b>Run!</b>| He yelled with all his strenght.",
        "that is so <sub>cool</sub>.| Did you try it?",

        # Multi-digit vertical list items
        "12. The first item.\n|13. The second item.",
        "    A12. The first item.\n|    B13. The second item.",

        # CORP_ENTITY_ABBRVS must use word boundary
        "Kid!| Don't buy tobacco.| Alright!",

        # Day-month ambiguity (fix for #29)
        "The meeting is at 9 a.m. Monday.",
        "The event starts at 11a.m. Tue.",
        "The store opens at 8 p.m. December.",
        "The meeting is at 2 p.m.| Martin called.",
        "The meeting is at 10 a.m.| Monday's agenda was postponed.",

        # Scientific units (fix for #33)
        "Each tick denotes an increase of 100 meV.| Each data point follows.",
        "The supply reached 10 kV.| Measurements continued.",
        "The frequency was 20 MHz.| The receiver locked.",

        # Bracketed references (fix for #34)
        "Yan et al. [2004] analysed SSH variations.| The study was comprehensive.",
        "Fig. [1] shows the architecture.| Figure 2 provides details.",
        "As shown in pp. [55-60], the results are significant.| This confirms our hypothesis.",
        "See sec. [2.1] for details.| The methodology is described there.",

        # Newlines (fix for #50)
        "The simplest way\nto get started is with pip.",
        "10 languages supported today\n|Target is 22+.",
        "> Somewhere, something incredible\n> is waiting to be known",

        # Not a list (fix for #52)
        "I really want letter A.| I know that I asked you for the B.| I changed my mind.",
        "You are going to the store, and so am I.| We can go together.",

        # Emojis (fix for #73)
        "Nice work! 👍| Next step.",
        "The alternative is to put it before the full stop 👉.| So cool, right?",

        # Coordinate directions ambiguity (fix for #134)
        "Server A at 40.7128° N, 74.0060° W.| Server B at 34.0522° S, 118.2437° E.",
        "N. Scott Momaday is a writer.| He won the Pulitzer.",

        # "&" separator (fix for #150)
        "Trying to get back to Com. & Adm. through the most direct path in the dark.",

        # Dot followed by newline (fix for #205)
        "Hello world.\n|Next sentence.",

        # Flattened list items (fix for #208)
        "• 9. The first item.| • 10. The second item",
        "α· Πρώτο θέμα| β· Δεύτερο θέμα.",
        "The requirements are simple:| 1.) Python 3.12 environment.| 2. At least 8GB of RAM.",

        # Corporate and personal abbreviation boundaries (fix for #260)
        "Acme Inc. USA is expanding its engineering team this quarter.",
        "Beta Corp. North America leads this hiring initiative.",
        "Martin Luther King Jr. Day is a paid holiday at this company.",
        "John Doe Sr. VP of Engineering will be your hiring manager.",

        # markdown headers with trailing numbers stay whole (fix for #305)
        "### 1. The Regex Breakdown\n|### 2. Metric Interpretation",
        "        ### 1. The Regex Breakdown\n|        ### 2. Metric Interpretation",

        # Backtick and doubled-apostrophe quoted boundaries (fix for #347)
        "She replied `sure.`| Then he said ``okay.``| She replied ''OK?''| They both smiled.",

        # Reference abbreviations before a parenthetical continuation (fix for #356)
        "Items A, B, etc. (reference), and more.",

        # Scientific dotted abbreviations (fix for #357)
        "The model estimates the c.d.f. F.| The results are discussed w.r.t. V-TSMixer.",

        # reference abbrv + roman-numeral-like next word splits correctly (fix for #362)
        "I don't know why he mentioned that ref.| It was clearly fake.",

        # Adjacent parentheticals and nested closing delimiters (fix for #375)
        "Anomaly Transformer (A.T.) (Xu et al., 2022), MEMTO (Song et al., 2024).",
        'He wrote, ("Really?")| I answered "Are you serious?".',
        'He wrote, ("Really?") then answered "Yes.".',
        'He wrote, ("Really?") (I answered later.)| Next sentence.',

        # dotted vs (fix for #376)
        "Decoder-only v.s. Encoder-only.| Next sentence.",
    ],
)
def test_universal_regression(marked_text):
    """Test that fixed boundary issues aren't regressed"""
    expected = [sent.strip() for sent in marked_text.split("|")]
    input_text = marked_text.replace("|", "")

    result = list(BoundaryDetector(lang="en").segment(input_text))
    assert result == expected, f"Input: {input_text}"
# fmt: on


def test_cyrillic_newline_inside_sentence():
    """Test that Cyrillic lowercase after a newline is sentence-internal (fix for #274)."""
    detector = BoundaryDetector(lang="ru")
    result = list(detector.segment("Это\nслово продолжается."))
    assert len(result) == 1
    assert result[0].replace("\n", " ") == "Это слово продолжается."


@pytest.mark.parametrize("max_sentences", [1, 2, 3, 8])
@pytest.mark.parametrize("overlap_percent", [0, 0.5, 50, 50.5, 80])
def test_text_chunking_preserves_sentences(max_sentences, overlap_percent):
    sentences = ["Alpha.", " Beta.", " Gamma.", " Delta.", " Epsilon.", " Zeta."]
    chunks = chunk_text("".join(sentences), "en", max_sentences, overlap_percent)
    assert all(chunks)
    assert all(chunk in "".join(sentences) for chunk in chunks)
    assert chunks[0].startswith("Alpha.")
    assert chunks[-1].endswith("Zeta.")
    assert all(sentence.strip() in "".join(chunks) for sentence in sentences)
    detector = BoundaryDetector("en")
    assert all(len(list(detector.segment(chunk))) <= max_sentences for chunk in chunks)


@pytest.mark.parametrize("text", ["Alpha. Beta.", ""])
@pytest.mark.parametrize("overlap_percent", [-50, -0.1, 80.1, 100, 150, float("nan"), float("inf"), -float("inf")])
def test_text_chunking_rejects_invalid_overlap(text, overlap_percent):
    with pytest.raises(ValueError, match="overlap_percent must be between 0 and 80 inclusive"):
        chunk_text(text, "en", 2, overlap_percent)


@pytest.mark.parametrize("text", ["Alpha.", ""])
@pytest.mark.parametrize("max_sentences", [0, -1])
def test_text_chunking_rejects_invalid_window(text, max_sentences):
    with pytest.raises(ValueError, match="max_sentences must be positive"):
        chunk_text(text, "en", max_sentences, 50)


@pytest.mark.parametrize("overlap_percent", [0, 0.5, 50.5, 80])
def test_text_chunking_empty_input(overlap_percent):
    assert chunk_text("", "en", 2, overlap_percent) == []


@pytest.mark.parametrize("overlap_percent, expected", [
    (0, ["Alpha. Beta.", " Gamma. Delta."]),
    (0.5, ["Alpha. Beta.", " Gamma. Delta."]),
    (50, ["Alpha. Beta.", " Beta. Gamma.", " Gamma. Delta."]),
    (50.5, ["Alpha. Beta.", " Beta. Gamma.", " Gamma. Delta."]),
    (80, ["Alpha. Beta.", " Beta. Gamma.", " Gamma. Delta."]),
])
def test_text_chunking_whole_sentence_overlap(overlap_percent, expected):
    assert chunk_text("Alpha. Beta. Gamma. Delta.", "en", 2, overlap_percent) == expected
