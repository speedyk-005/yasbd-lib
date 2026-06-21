from functools import wraps
from typing import TypeVar
from collections.abc import Callable

from beartype import beartype
from beartype.roar import BeartypeCallHintViolation

from yasbd.exceptions import InvalidInputError


F = TypeVar("F", bound=Callable)


def validate_input(fn: F) -> F:
    """Validate function arguments and return values using beartype."""

    validated_fn = beartype(fn)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return validated_fn(*args, **kwargs)
        except BeartypeCallHintViolation as e:
            raise InvalidInputError(str(e)) from None

    return wrapper
