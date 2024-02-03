import pytest
from useful_tools.act_as_list import act_as_list

@act_as_list('objects')
class MyClassThatLooksLikeAList:
    def __init__(self, objects = []):
        self.objects = objects
    def in_uppercase(self):
        return " ".join(self).upper()
    def contains_both_hello_and_world(self):
        return "hello" in self and "world" in self

@act_as_list('actual_list')
class MyClassWithExtraAttrs:
    def __init__(self, actual_list = [], extra_attr = None):
        if extra_attr == None:
            raise Exception("extra_attr is required")
        else:
            self.extra_attr = extra_attr
        self.actual_list = actual_list
    def _from_list(self, actual_list):
        return MyClassWithExtraAttrs(actual_list, extra_attr=self.extra_attr)


def test_getitem():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list[0] == "hello"
    assert fake_list[1] == "world"

def test_setitem():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list[0] = "foo"
    assert fake_list[0] == "foo"

def test_eq():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list == ["hello", "world"]

def test_append():
    fake_list = MyClassThatLooksLikeAList()
    fake_list.append("hello")
    fake_list.append("world")
    assert fake_list[0] == "hello"
    assert fake_list[1] == "world"

def test_remove():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list.remove("hello")
    assert fake_list == ["world"]

def test_iter():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    for item in fake_list:
        assert item in ["hello", "world"]

def test_extend():
    fake_list = MyClassThatLooksLikeAList()
    fake_list.extend(["hello", "world"])
    assert fake_list[0] == "hello"
    assert fake_list[1] == "world"

def test_clear():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list.clear()
    assert fake_list == []

def test_copy():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list_copy = fake_list.copy()
    assert fake_list_copy == ["hello", "world"]

def test_count():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.count("hello") == 1

def test_len():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert len(fake_list) == 2

def test_contains():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert ("hello" in fake_list) == True
    assert ("world" in fake_list) == True
    assert ("foobar" in fake_list) == False

def test_index():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.index("world") == 1

def test_reversed():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    reversed_list = reversed(fake_list)
    normal_reversed_list = reversed([1,2,3])
    assert list(reversed_list) == ["world", "hello"]
    assert reversed_list.__class__ == normal_reversed_list.__class__ # reversed returns a list_reverseiterator by default

def test_reversed_returning_original_class():
    fake_list = MyClassWithExtraAttrs(["hello", "world"], extra_attr="fubar")
    result = reversed(fake_list)
    assert result == ["world", "hello"]
    assert result.__class__ == MyClassWithExtraAttrs # because the class has a _from_list method, it returns the original class

def test_reverse():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list.reverse()
    assert fake_list == ["world", "hello"]

def test_pop():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.pop() == "world"

def test_insert():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list.insert(fake_list.index("world"), "the")
    assert fake_list == ['hello', 'the', 'world']

def test_str():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert str(fake_list) == "['hello', 'world']"

def test_repr():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert repr(fake_list) == "MyClassThatLooksLikeAList(['hello', 'world'])"

def test_sort():
    fake_list = MyClassThatLooksLikeAList(["c", "a", "b"])
    fake_list.sort()
    assert fake_list == ["a", "b", "c"]

def test_in_uppercase():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.in_uppercase() == "HELLO WORLD"

def test_contains_both_hello_and_world():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.contains_both_hello_and_world() == True
    fake_list.pop()
    assert fake_list.contains_both_hello_and_world() == False

def test_class_and_class_name():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    assert fake_list.__class__.__name__ == "MyClassThatLooksLikeAList"
    assert fake_list.__class__ == MyClassThatLooksLikeAList

def test_add_with_class():
    fake_list1 = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list2 = MyClassThatLooksLikeAList(["foo", "bar"])
    result = fake_list1 + fake_list2
    assert result == ["hello", "world", "foo", "bar"]
    assert result.__class__ == list # because the class does not have a _from_list method, it returns a list

def test_add_with_list():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    result = fake_list + ["foo", "bar"]
    assert result == ["hello", "world", "foo", "bar"]
    assert result.__class__ == list # because the class does not have a _from_list method, it returns a list

def test_class_with_extra_attrs():
    fake_list = MyClassWithExtraAttrs(["hello", "world"], extra_attr="fubar")
    assert fake_list.extra_attr == "fubar" # extra_attr is set in the constructor, so it should be available on the instance

def test_class_with_extra_attrs_without_extra_attr():
    with pytest.raises(Exception):
        MyClassWithExtraAttrs(["hello", "world"]) # extra_attr is required in the constructor, so it should raise an exception

def test_add_with_list_returning_original_class():
    fake_list = MyClassWithExtraAttrs(["hello", "world"], extra_attr="fubar")
    result = fake_list + ["foo", "bar"]
    assert result == ["hello", "world", "foo", "bar"]
    assert result.__class__ == MyClassWithExtraAttrs # because the class has a _from_list method, it returns the original class

def test_add_with_class_returning_original_class():
    fake_list1 = MyClassWithExtraAttrs(["hello", "world"], extra_attr="fubar")
    fake_list2 = MyClassWithExtraAttrs(["foo", "bar"], extra_attr="fubar")
    result = fake_list1 + fake_list2
    assert result == ["hello", "world", "foo", "bar"]
    assert result.__class__ == MyClassWithExtraAttrs # because the class has a _from_list method, it returns the original class
