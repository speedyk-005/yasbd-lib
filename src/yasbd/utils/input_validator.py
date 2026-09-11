"""Partial runtime type validation for public entry points.

This module intentionally covers only what yasbd uses: plain types,
``None``, unions (``X | Y``), and subscripted generics checked via their
origin (e.g. ``Collection[str]`` validates as ``collections.abc.Collection``
without checking element types). Exotic forms (``Literal``, ``Annotated``,
``TypeVar``, nested parameters) are accepted unchecked rather than rejected.

It is a lightweight beartype replacement, not a full type checker: when in
doubt it passes the value through instead of raising.
"""

import reprlib
import typing
from collections.abc import Callable
from functools import wraps
from types import UnionType

from yasbd.exceptions import InvalidInputError

F = typing.TypeVar("F", bound=Callable)


def _trunc_repr(value):  # pragma: no cover
    """Truncate values for readable error messages."""
    # Use reprlib for auto-truncation on non-strings
    # (faster for lists/dicts/nested)
    if isinstance(value, str) and len(value) >= 120:
        return value[:500] + "..."
    return reprlib.repr(value)


def _validate_type(value, expected_type, name):
    """Validate a value against an expected type."""
    # Origin first: `isinstance(hint, type)` is version-flaky for generics
    # (e.g. `type[X]` passes it on 3.10), so never let them reach that gate.
    origin = typing.get_origin(expected_type)
    if origin is UnionType or origin is typing.Union:
        valid = False
        for option in typing.get_args(expected_type):
            try:
                _validate_type(value, option, name)
                valid = True
                break
            except InvalidInputError:
                continue
    elif origin is type:
        args = typing.get_args(expected_type)
        valid = isinstance(value, type) and (not args or issubclass(value, args[0]))
    elif origin is not None:
        valid = isinstance(value, origin)
    elif expected_type is None or expected_type is type(None):
        valid = value is None
    elif isinstance(expected_type, type):
        valid = isinstance(value, expected_type)
    else:
        try:
            valid = isinstance(value, expected_type)
        except TypeError:
            valid = True

    if valid:
        return value

    raise InvalidInputError(
        f"Invalid type for {name!r}.\n"
        f"Expected {expected_type}.\n"
        f"Found: (input={_trunc_repr(value)}, type={type(value).__name__!r})"
    )


def _validate_call(pos_checks, kw_checks, args, kwargs):
    """Validate call arguments in place (validators never transform values)."""
    # Validate positional-or-keyword arguments
    for idx, name, expected_type in pos_checks:
        if idx < len(args):
            _validate_type(args[idx], expected_type, name=name)
        elif name in kwargs:
            _validate_type(kwargs[name], expected_type, name=name)

    # Validate keyword-only arguments
    for name, expected_type in kw_checks:
        if name in kwargs:
            _validate_type(kwargs[name], expected_type, name=name)


def validate_input(fx: F) -> F:
    """Validate function arguments based on  type hints."""
    hints = typing.get_type_hints(fx)
    ret_type = hints.pop("return", None)

    if not hints and ret_type is None:
        return fx

    # Pre-compute positional param indices (skip self)
    code = fx.__code__
    varnames = code.co_varnames
    argcount = code.co_argcount
    kwonlycount = code.co_kwonlyargcount

    pos_names = varnames[:argcount]
    kwonly_names = varnames[argcount : argcount + kwonlycount]

    is_method = pos_names and pos_names[0] in ("self", "cls")

    pos_checks = []
    kw_checks = []
    for i, name in enumerate(pos_names):
        if name not in hints or (i == 0 and is_method):
            continue
        pos_checks.append((i, name, hints[name]))

    kw_checks = [(name, hints[name]) for name in kwonly_names if name in hints]

    @wraps(fx)
    def wrapper(*args, **kwargs):
        _validate_call(pos_checks, kw_checks, args, kwargs)

        result = fx(*args, **kwargs)

        # Validate return type (skip if unannotated)
        if ret_type is not None:
            result = _validate_type(result, ret_type, name=f"Return of {fx.__name__!r}")
        return result

    return wrapper
