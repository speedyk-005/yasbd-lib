import reprlib
from collections.abc import Iterable
from functools import wraps

from pydantic import ConfigDict, ValidationError, validate_call

IterableOfStr = str | Iterable[str],


class InvalidInputError(Exception):
    """Raised when invalid input(s) are encountered."""
    pass


def _pretty_errors(error: ValidationError) -> str:
    """Formats Pydantic validation errors into a human-readable string.

    Exemple:
    >>> from pydantic import ValidationError
    >>> err = ValidationError.from_exception_data(
    ...     "TestModel",
    ...     [{"type": "int_parsing", "loc": ("x",), "msg": "Input should be a valid integer", "input": "not_an_int"}]
    ... )
    >>> print(_pretty_errors(err))
    ...
    1 validation error for TestModel.
    1) (x) Input should be a valid integer, unable to parse string as an integer.
      Found: (input='not_an_int', type=str)
    ...
    """
    lines = [
        f"{error.error_count()} validation error for {getattr(error, 'subtitle', '') or error.title}."
    ]
    for ind, err in enumerate(error.errors(), start=1):
        msg = err["msg"]

        loc = err.get("loc", [])
        formatted_loc = ""
        if len(loc) >= 1:
            formatted_loc = str(loc[0]) + "".join(f"[{step!r}]" for step in loc[1:])
            formatted_loc = f"({formatted_loc})" if formatted_loc else ""

        input_value = err["input"]
        input_type = type(input_value).__name__

        # Use reprlib for auto-truncation on non-strings (faster for lists/dicts/nested)
        if not isinstance(input_value, str):
            input_value = reprlib.repr(input_value)
        else:
            input_value = input_value if len(input_value) < 500 else input_value[:500] + "..."

        lines.append(
            (
                f"{ind}) {formatted_loc} {msg}.\n"
                f"  Found: (input={input_value!r}, type={input_type})"
            )
        )

    lines.append("  " + getattr(error, "hint", ""))
    return "\n".join(lines)


def validate_input(fn):
    """
    A decorator that validates function inputs and outputs

    A wrapper around Pydantic's `validate_call` that catches`ValidationError` and re-raises it as a more user-friendly `InvalidInputError`.
    """
    validated_fn = validate_call(fn, config=ConfigDict(arbitrary_types_allowed=True))

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return validated_fn(*args, **kwargs)
        except ValidationError as e:
            raise InvalidInputError(_pretty_errors(e)) from None

    return wrapper
