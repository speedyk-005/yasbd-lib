import pytest

from yasbd.exceptions import InvalidInputError
from yasbd.normalize import normalize_lang


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("EN", "en"),
        ("en-US", "en"),
        ("en-Latn", "en"),
        ("pt-BR", "pt"),
    ],
)
def test_normalize_lang_returns_iso_639_1_code(raw, expected):
    assert normalize_lang(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "not-a-language-code"])
def test_normalize_lang_rejects_invalid_input(raw):
    with pytest.raises(InvalidInputError):
        normalize_lang(raw)


def test_normalize_lang_rejects_codes_without_iso_639_1_mapping():
    with pytest.raises(InvalidInputError, match="ISO-639-1"):
        normalize_lang("akk")
