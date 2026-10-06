import reprlib
import sys

from yasbd.exceptions import InvalidInputError


def _format_err_msg(
    ind: int, value: object, expecting_list: list[str]
) -> str:  # pragma: no cover
    """Format one validation failure entry with truncated input display."""
    if len(expecting_list) == 1:
        expecting = expecting_list[0]
    else:
        expecting = f"{', '.join(expecting_list[:-1])} or {expecting_list[-1]}"

    if not isinstance(value, str):
        shown = reprlib.repr(value)
    else:
        shown = value if len(value) < 500 else value[:500] + "..."

    return (
        f"{ind}) invalid input, expecting: {expecting}.\n"
        f"  Found: (input={shown!r}, type={type(value).__name__})"
    )


def validate_inputs(items: list[tuple[object, tuple[type, ...]]]) -> None:
    """Shallow runtime type check over ``(value, allowed types)`` pairs.

    Each pair is checked with :func:`isinstance`; all mismatches are
    collected and raised together as one :class:`InvalidInputError`.
    Unlike beartype, this never inspects generics or nested structure —
    only the top-level type.

    Example:
        >>> validate_inputs([("text", (str,)), ([1, 2], (list, tuple))])
        >>> validate_inputs([(42, (str,))])
        Traceback (most recent call last):
        ...
        yasbd.exceptions.InvalidInputError: ...
    """
    title = sys._getframe(1).f_code.co_name  # noqa: SLF001

    errors = []
    for ind, (value, allowed) in enumerate(items, start=1):
        allowed_types = allowed if isinstance(allowed, tuple) else (allowed,)

        if isinstance(value, allowed_types):
            continue

        errors.append(_format_err_msg(ind, value, [t.__name__ for t in allowed_types]))

    if errors:
        lines = [f"{len(errors)} validation error for {title}.", *errors]
        raise InvalidInputError("\n".join(lines))
