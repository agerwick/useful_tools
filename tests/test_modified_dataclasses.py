import pytest

from useful_tools.modified_dataclasses import modified_dataclass


def test_no_defaults():
    @modified_dataclass(exclude_defaults_from_repr=True)
    class NoDefaults:
        a: int
        b: int
        c: int = 1
        d: int = 1

    n = NoDefaults(a = 0, b = 2, c = 3)
    assert repr(n) == "NoDefaults(a=0, b=2, c=3)"

def test_exclude():
    @modified_dataclass(exclude_from_repr=["exclude_this"])
    class Exclude:
        a: int
        b: int = 1
        exclude_this: str = "should be excluded"

    e = Exclude(a = 0, b = 3)
    assert repr(e) == "Exclude(a=0, b=3)"

def test_simplify(a = 0):
    @modified_dataclass(simplify_repr=["simplify_this", "and_this"])
    class Simplify:
        a: int
        b: int = 1
        simplify_this: str = "should be simplidied"
        and_this: str = "should be simplidied"

    s = Simplify(a = 0, and_this = "not simplified")
    assert repr(s) == "Simplify(a=0, b=1, simplify_this=<class 'str'>, and_this=<class 'str'>)"
