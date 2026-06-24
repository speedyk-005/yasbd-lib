from yasbd.exceptions import InvalidInputError
from yasbd.utils.input_validator import validate_input


@validate_input
def normalize_lang(lang_code: str) -> str:
    """Normalize a language tag to an ISO-639-1 language code.

    The helper is explicit and opt-in. It does not alter the core
    ``BoundaryDetector`` language handling.

    Args:
        lang_code: A language code or tag, such as ``"EN"``, ``"en-US"``,
            or ``"en-Latn"``.

    Returns:
        A two-letter ISO-639-1 language code.

    Raises:
        InvalidInputError: If the optional normalization dependency is missing,
            the tag cannot be parsed, or the tag does not resolve to a
            two-letter ISO-639-1 language code.
    """
    if not lang_code.strip():
        return ""

    try:
        from langcodes import Language, LanguageTagError
    except ImportError as e:  # pragma: no cover
        raise ImportError(
            "normalize_lang(...) requires the 'norm' extra. "
            "Install with 'pip install yasbd-lib[norm]'"
        ) from None

    try:
        # Language auto normalize to ISO-639-1
        return Language.get(lang_code).language
    except LanguageTagError as e:
        raise InvalidInputError(str(e)) from None

    if len(norm_lang) != 2 or not language.isalpha():
        raise InvalidInputError(
            f"{lang_code!r} can't be normalized to a two chars ISO-639-1 language code"
        )

    return norm_lang
