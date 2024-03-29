import os
import sys
import pytest

if not any('pytest' in arg for arg in sys.argv):
    # running the file directly, not as a test
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # add the parent directory to the path # pragma: no cover

from useful_tools.modified_dataclasses import modified_dataclass, ModifiedDataclassTypeError

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

def test_replace_repr_with_attr():
    # test incorrect usage -- the first param represents the attribute to be replaced, and the second param represents the attribute ON THAT ATTIRBUTE to replace it with
    # in this case, the attribute "replace_this" is a string, so only attributes of string are allowed
    # "replace_with_this" is not an attribute of string, so this should raise an AttributeError
    @modified_dataclass(replace_repr_with_attr={"replace_this": "replace_with_this"})
    class Replace:
        a: int
        b: int = 1
        replace_this: str = "should be replaced"
        replace_with_this: str = "replaced"

    # check that the following statement fails with an AttributeError
    with pytest.raises(AttributeError):
        r = Replace(a = 0, b = 3) # pragma: no cover
        repr(r)
        # assert repr(r) == "Replace(a=0, b=3, replace_this=replaced, replace_with_this=replaced)"

def test_replace_repr_with_attr_of_different_object():
    # test correct usage -- the first param represents the attribute to be replaced, and the second param represents the attribute ON THAT ATTIRBUTE to replace it with
    # in this case, the attribute "session" is an object, so any attribute of that object is allowed, and "hash" is an attribute of the object "Session"
    class Session:
        def __init__(self, hash):
            self.hash = hash
            self.other_var = "other_var"

    @modified_dataclass(replace_repr_with_attr={"session": "hash"}) # in the string representation of Test, replace the string representation of session with session.hash
    class Test():
        id: int = None
        status: str = None
        session: 'Session' = None

    session = Session(hash = "ABCD1234XYZ")
    t = Test(id = 1, status = "running", session = session)
    assert repr(t) == "Test(id=1, status=running, session=ABCD1234XYZ)"

def test_replace_repr_with_attr_missing():
    @modified_dataclass(replace_repr_with_attr={"replace_this": "attr_on_Replace_class_that_does_not_exist"})
    class Replace:
        a: int
        b: int = 1
        replace_this: str = "should be replaced"

    # construct the class
    r = Replace(a = 0, b = 3) # this does not raise an error
    # the error is only raised when the repr method is called (such as when using print)
    with pytest.raises(AttributeError):
        print(r) # pragma: no cover

def test_TypeError_when_wrong_type_is_passed_to_replace_repr_with_attr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(replace_repr_with_attr=0)
        class Test: # pragma: no cover
            pass # pragma: no cover

def test_TypeError_when_wrong_type_is_used_in_dict_keys_in_replace_repr_with_attr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(replace_repr_with_attr={0: "a"})
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_used_in_dict_values_in_replace_repr_with_attr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(replace_repr_with_attr={"a": 0})
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_passed_to_simplify_repr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(simplify_repr=0)
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_passed_as_list_elements_in_simplify_repr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(simplify_repr=[0])
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_passed_to_exclude_from_repr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(exclude_from_repr=0)
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_passed_as_list_elements_in_exclude_from_repr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(exclude_from_repr=[0])
        class Test: # pragma: no cover
            pass

def test_TypeError_when_wrong_type_is_passed_to_exclude_defaults_from_repr():
    with pytest.raises(ModifiedDataclassTypeError):
        @modified_dataclass(exclude_defaults_from_repr=0)
        class Test: # pragma: no cover
            pass
