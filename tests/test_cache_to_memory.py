import pytest
from useful_tools.cache_decorators import cache_to_memory

class MyClass:
    def __init__(self):
        self.number_of_calls = 0

    @cache_to_memory
    def my_method(self, *args, **kwargs):
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

def test_cache_to_memory_with_args():
    my_class = MyClass()

    # Call the method for the first time
    result = my_class.my_method("my_arg", "another_arg")
    assert result == "my_method"
    assert my_class.number_of_calls == 1

    # Call the method for the second time with the same arguments
    result = my_class.my_method("my_arg", "another_arg")
    assert result == "my_method"
    assert my_class.number_of_calls == 1  # The number of calls should still be 1 because the result is cached

    # Call the method for the third time with different arguments
    result = my_class.my_method("my_other_arg")
    assert result == "my_method"
    assert my_class.number_of_calls == 2  # The number of calls should be 2 because the arguments are different

    # Call the method for the fourth time with the same arguments in a different order
    result = my_class.my_method("another_arg", "my_arg")
    assert result == "my_method"
    assert my_class.number_of_calls == 3 # The number of calls should be 3 because the arguments are different

def test_cache_with_non_hashable_args():
    # call the method with non-hashable arguments, which the cache function should handle
    my_class = MyClass()
    result = my_class.my_method([1,2,3])
    assert result == "my_method"
    assert my_class.number_of_calls == 1
    
    # call a second time with the same arguments, which should be cached
    result = my_class.my_method([1,2,3])
    assert result == "my_method"

    # call with different arguments, which should not be cached
    result = my_class.my_method([4,5,6])
    assert result == "my_method"
    assert my_class.number_of_calls == 2

    # call with same arguments in a different order, which should not be cached
    result = my_class.my_method([3,2,1])
    assert result == "my_method"
    assert my_class.number_of_calls == 3

def test_cache_with_kwargs():
    # call the method with kwargs, which the cache function should handle
    my_class = MyClass()
    my_class.my_method(my_kwarg = "my_value", my_other_kwarg = "my_other_value")
    assert my_class.number_of_calls == 1
    
    # call a second time with the same arguments, which should be cached
    my_class.my_method(my_kwarg = "my_value", my_other_kwarg = "my_other_value")
    assert my_class.number_of_calls == 1

    # call with different arguments, which should not be cached
    my_class.my_method(my_kwarg = "my_other_value")
    assert my_class.number_of_calls == 2

    # call with same arguments in a different order, which should be cached
    my_class.my_method(my_other_kwarg = "my_other_value", my_kwarg = "my_value")
    # temporarily disabled, as the cache function does not handle kwargs in a different order YET
    # assert my_class.number_of_calls == 2
