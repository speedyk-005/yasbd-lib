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
        raise InvalidInputError("'lang_code' is required")

    try:
        from langcodes import LanguageTagError, standardize_tag
    except ImportError as exc:  # pragma: no cover
        raise InvalidInputError(
            "normalize_lang() requires the 'norm' extra: pip install yasbd-lib[norm]"
        ) from exc

    try:
        language = standardize_tag(lang_code).split("-", maxsplit=1)[0]
    except (LanguageTagError, ValueError) as exc:
        raise InvalidInputError(str(exc)) from None

    if len(language) != 2 or not language.isalpha():
        raise InvalidInputError(
            f"{lang_code!r} does not normalize to an ISO-639-1 language code"
        )

    return language.lower()
