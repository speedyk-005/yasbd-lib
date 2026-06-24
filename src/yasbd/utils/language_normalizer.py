from yasbd.exceptions import InvalidInputError
from yasbd.utils.input_validator import validate_input


@validate_input
def normalize_lang(lang_code: str) -> str:
    """Normalize a language tag to an ISO-639-1 language code.

    The helper is explicit and opt-in. It does not alter the core
    ``BoundaryDetector`` language handling.

    Examples:

        >>> normalize_lang("EN")
        'en'
        >>> normalize_lang("en-US")
        'en'
        >>> normalize_lang("en-Latn")
        'en'
        >>> normalize_lang("pt-BR")
        'pt'
        >>> normalize_lang("")
        ''
        >>> normalize_lang("   ")
        ''
        >>> normalize_lang("not-a-language-code")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        yasbd.exceptions.InvalidInputError: ...
        >>> normalize_lang("akk")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        yasbd.exceptions.InvalidInputError: ...

    Args:
        lang_code: A language code or tag, such as ``"EN"``, ``"en-US"``,
            or ``"en-Latn"``.

    Returns:
        A two-letter ISO-639-1 language code, or an empty string if empty input.

    Raises:
        ImportError: If the optional ``langcodes`` dependency is missing.
        InvalidInputError: If the tag cannot be parsed or does not resolve to a
            two-letter ISO-639-1 language code.
    """
    if not lang_code.strip():
        return ""

    try:
        from langcodes import Language, LanguageTagError
    except ImportError:  # pragma: no cover
        raise ImportError(
            "normalize_lang(...) requires the 'norm' extra. "
            "Install with 'pip install yasbd-lib[norm]'"
        ) from None

    try:
        normalized = Language.get(lang_code).language
    except LanguageTagError as e:
        raise InvalidInputError(str(e)) from None

    if normalized is None or len(normalized) != 2 or not normalized.isalpha():
        raise InvalidInputError(
            f"{lang_code!r} can't be normalized to a two chars ISO-639-1 language code"
        )

    return normalized
