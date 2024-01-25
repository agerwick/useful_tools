import pytest
from useful_tools.cache_decorators import cache_to_memory

class MyClass:
    def __init__(self):
        self.number_of_calls = 0

    @cache_to_memory
    def my_method(self):
        self.number_of_calls += 1
        return "my_method"

def test_cache_to_memory_on_property():
    # this should generate an exception, as the property decorator must be defined before the cache_to_memory decorator
    # check the error message to see if it is the expected one
    with pytest.raises(TypeError) as error_info:
        class IncorrectUsageOfCacheToMemory:
            @cache_to_memory
            @property # this should fail, as the property decorator must be defined before the cache_to_memory decorator
            def my_property(self):
                pass
def test_cache_to_memory():
    my_class = MyClass()

    # Call the method for the first time
    result = my_class.my_method()
    assert result == "my_method"
    assert my_class.number_of_calls == 1

    # Call the method for the second time
    result = my_class.my_method()
    assert result == "my_method"
    assert my_class.number_of_calls == 1  # The number of calls should still be 1 because the result is cached
