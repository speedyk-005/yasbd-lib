import collections.abc

import pytest

from yasbd.exceptions import InvalidInputError
from yasbd.utils.input_validator import validate_input

@validate_input
def identity(value: int) -> int:
    return value


@validate_input
def union(value: int | str) -> int | str:
    return value


@validate_input
def callable_(value: collections.abc.Callable) -> object:
    return value()


@validate_input
def class_(value: type) -> str:
    return value.__name__


@pytest.mark.parametrize(
    "func, value, expected",
    [
        (identity, 42, 42),
        (union, 42, 42),
        (union, "hello", "hello"),
        (callable_, lambda: 42, 42),
        (class_, str, "str"),
    ],
)
def test_valid_types(func, value, expected):
    """Test that valid inputs pass through unchanged."""
    assert func(value) == expected


@pytest.mark.parametrize(
    "func, value",
    [
        (identity, "42"),
        (union, 42.5),
        (callable_, 42),
        (class_, "str"),
    ],
)
def test_invalid_types(func, value):
    """Test that invalid inputs raise TypeError."""
    with pytest.raises(TypeError):
        func(value)


def test_issubclass():
    """Test that class objects validate via issubclass."""
    class Animal:
        pass

    class Dog(Animal):
        pass

    @validate_input
    def accepts_animal(value: type[Animal]) -> str:
        return value.__name__

    assert accepts_animal(Dog) == "Dog"

    with pytest.raises(InvalidInputError):
        accepts_animal(str)
