import pytest
from useful_tools.cache_to_memory import cache_property

class MyClass:
    number_of_calls = 0

    @property
    @cache_property
    def my_property(self):
        self.number_of_calls += 1
        return "my_property"

def test_cache_property():
    my_class = MyClass()

    # Call the property for the first time
    result = my_class.my_property
    assert result == "my_property"
    assert my_class.number_of_calls == 1

    # Call the property for the second time
    result = my_class.my_property
    assert result == "my_property"
    assert my_class.number_of_calls == 1  # The number of calls should still be 1 because the result is cached