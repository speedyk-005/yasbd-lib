import collections.abc
import typing
from collections.abc import Iterator
from functools import wraps
from types import UnionType

from yasbd.exceptions import InvalidInputError


class IteratorValidator:
    """Lazy iterator instance validator.

    >>> it = IteratorValidator([1, 2, 3], int)
    >>> list(it)
    [1, 2, 3]
    >>> it2 = IteratorValidator([1, "x"], int)
    >>> list(it2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    InvalidInputError: 🧩 Oops! Invalid type for 'iterator[1]'...
    """

    def __init__(self, target, expected_item_type, name=None):
        if not isinstance(target, (collections.abc.Iterable, collections.abc.Iterator)):
            raise TypeError(f"Cannot create IteratorValidator from {type(target).__name__}")

        self.target_iterator = iter(target)
        self.expected_item_type = expected_item_type
        self._index = 0
        self._name = name or "iterator"

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self.target_iterator)
        _validate_type(item, self.expected_item_type, f"{self._name}[{self._index}]")
        self._index += 1
        return item


def _trunc_repr(value):  # pragma: no cover
    """Truncate string values to 120 chars for readable error messages."""
    if isinstance(value, str) and len(value) >= 120:
        return value[:120] + "..."
    return repr(value)


def _raise_error(name, value, expected_type):
    """Raise InvalidInputError with formatted message."""
    if name is None:
        name = repr(value)
    ex = InvalidInputError(
        f"🧩 Oops! Invalid type for '{name}'.\n"
        f"Expected {getattr(expected_type, '__name__', repr(expected_type))}.\n"
        f"  Found: (input={_trunc_repr(value)}, type={type(value).__name__})"
    )
    raise ex


def _validate_type(value, expected_type, name=None):
    """
    Validate a value against an expected type at runtime.

    Returns the value itself on success, or raises InvalidInputError
    with a clear message.

    Args:
        value: The object to validate.
        expected_type: The type to validate against. Supports simple types,
            unions (int | str), Iterator[X], and None.
        name: Optional display name for the value in error messages.
            Defaults to repr(value).

    Returns:
        The value itself, unchanged, on success.

    Raises:
        InvalidInputError: If the value does not match expected_type.

    Limitations:
        - Nested container subtypes (list[int] ignores the inner type,
          only checks it's a list)
        - TypedDict, dataclasses, attrs, or any structured object shapes
        - Callable signatures
        - Forward references (strings)
        - Type variables / generics

    Examples:
        >>> _validate_type(None, None) is None
        True
        >>> _validate_type(42, int | str)
        42
        >>> it = _validate_type(iter([1, 2]), Iterator[int])
        >>> list(it)
        [1, 2]
        >>> _validate_type(42, None)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidInputError: 🧩 Oops! Invalid type for '42'...
        >>> _validate_type(42, float | str)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidInputError: 🧩 Oops! Invalid type for '42'...
        >>> _validate_type("hi", int)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        InvalidInputError: 🧩 Oops! Invalid type for '...'...
    """
    # Fast path: plain types (most common case)
    if isinstance(expected_type, type):
        if isinstance(value, expected_type):
            return value
        _raise_error(name, value, expected_type)

    # Handle None type
    if expected_type is None or expected_type is type(None):
        if value is not None:
            _raise_error(name, value, expected_type)
        return value

    if name is None:
        name = repr(value)

    origin = typing.get_origin(expected_type) or expected_type

    # Handle Union types (X | Y or Union[X, Y])
    if origin is typing.Union or origin is UnionType:
        args = typing.get_args(expected_type)
        for t in args:
            try:
                return _validate_type(value, t, name=name)
            except InvalidInputError:
                pass
        ex = InvalidInputError(
            f"🧩 Oops! Invalid type for '{name}'.\n"
            f"Expected one of: {', '.join(getattr(a, '__name__', repr(a)) for a in args)}.\n"
            f"  Found: (input={_trunc_repr(value)}, type={type(value).__name__})"
        )
        raise ex

    # Handle Iterator types (Iterator[X])
    if origin is Iterator or (isinstance(origin, type) and issubclass(origin, Iterator)):
        args = typing.get_args(expected_type)
        item_type = args[0] if args else object
        if isinstance(value, IteratorValidator):
            return value
        if isinstance(value, collections.abc.Iterator):
            return IteratorValidator(value, item_type, name=name)
        _raise_error(name, value, expected_type)

    # Handle simple types via origin
    if isinstance(value, origin):
        return value
    _raise_error(name, value, expected_type)


def validate_input(fx):
    """Decorator to validate type hints at runtime.

    >>> @validate_input
    ... def noop(x):
    ...     return x
    >>> noop(5)
    5
    """

    hints = typing.get_type_hints(fx)
    ret_type = hints.pop("return", None)
    if not hints and ret_type is None:

        @wraps(fx)
        def wrapper(*args, **kwargs):
            return fx(*args, **kwargs)

        return wrapper

    # Pre-compute positional param indices (skip self)
    pos_param_count = fx.__code__.co_argcount
    pos_param_names = fx.__code__.co_varnames[:pos_param_count]
    kwonly_count = fx.__code__.co_kwonlyargcount
    kwonly_start = pos_param_count
    kwonly_names = list(fx.__code__.co_varnames[kwonly_start : kwonly_start + kwonly_count])

    pos_checks = []
    kw_checks = []
    for i, name in enumerate(pos_param_names):
        if name in hints:
            if i == 0 and name == "self":
                continue
            pos_checks.append((i, name, hints[name]))

    for name in kwonly_names:
        if name in hints:
            kw_checks.append((name, hints[name]))

    @wraps(fx)
    def wrapper(*args, **kwargs):
        args = list(args)

        # Validate positional-or-keyword arguments
        for idx, name, expected_type in pos_checks:
            if idx < len(args):
                args[idx] = _validate_type(args[idx], expected_type, name=name)
            elif name in kwargs:
                kwargs[name] = _validate_type(kwargs[name], expected_type, name=name)

        # Validate keyword-only arguments
        for name, expected_type in kw_checks:
            if name in kwargs:
                kwargs[name] = _validate_type(kwargs[name], expected_type, name=name)

        try:
            result = fx(*args, **kwargs)
        except TypeError:
            raise

        # Validate return type (skip if unannotated)
        if ret_type is not None:
            result = _validate_type(result, ret_type, name=f"Return of {fx.__name__!r}")
        return result

    return wrapper
