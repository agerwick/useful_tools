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

def test_add():
    fake_list1 = MyClassThatLooksLikeAList(["hello", "world"])
    fake_list2 = MyClassThatLooksLikeAList(["foo", "bar"])
    result = fake_list1 + fake_list2
    assert result == ["hello", "world", "foo", "bar"]

def test_add_with_list():
    fake_list = MyClassThatLooksLikeAList(["hello", "world"])
    result = fake_list + ["foo", "bar"]
    assert result == ["hello", "world", "foo", "bar"]

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
    assert list(reversed(fake_list)) == ["world", "hello"]

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
