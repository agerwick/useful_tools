import pytest
import time
import os
import shutil
import hashlib
from useful_tools.cache_decorators import cache_to_disk

class MyClass:
    cache_enabled = True
    cache_dir = "test_cache"
    cache_expiration = 0.5 # seconds
    force_cache_expiration = False
    ignore_cache_expiration = False

    def __init__(self):
        self.number_of_property_calls = 0
        self.number_of_method_calls = {}

    @property
    @cache_to_disk
    def my_property(self):
        self.number_of_property_calls += 1
        return "my_property"

    @cache_to_disk
    def my_method(self, *args, **kwargs):
        # make a hash of the arguments
        hash = generate_hash(args, kwargs)
        # count the number of calls to this method with these arguments
        if self.number_of_method_calls.get(hash) is None:
            self.number_of_method_calls[hash] = 0
        self.number_of_method_calls[hash] += 1
        return "my_method with args: {}, kwargs: {}".format(args, kwargs)

def generate_hash(args, kwargs):
    """
    Generate a hash of the arguments
    """
    # convert args to a string
    args_string = str(args)
    # convert kwargs to a string
    kwargs_string = str(kwargs)
    # concatenate args_string and kwargs_string
    concatenated_string = f"ARGS:'{args_string}' KWARGS:'{kwargs_string}'"
    # convert concatenated_string to bytes
    concatenated_bytes = concatenated_string.encode()
    # generate a hash of concatenated_bytes
    hash = hashlib.sha256(concatenated_bytes).hexdigest()
    return hash

def setup_module(module):
    if not os.path.exists(MyClass.cache_dir):
        os.makedirs(MyClass.cache_dir)

def teardown_module(module):
    shutil.rmtree(MyClass.cache_dir)

def test_property_cache_to_disk():
    my_class = MyClass()

    # Call the property for the first time
    result = my_class.my_property
    assert result == "my_property"
    assert my_class.number_of_property_calls == 1

    # Call the property for the second time (before cache expiration)
    result = my_class.my_property
    assert result == "my_property"
    assert my_class.number_of_property_calls == 1  # The number of calls should still be 1 because the result is cached

    # Wait for cache to expire
    time.sleep(my_class.cache_expiration + 0.1)

    # Call the property after cache expiration
    result = my_class.my_property
    assert result == "my_property"
    assert my_class.number_of_property_calls == 2  # The number of calls should be 2 because the cache has expired

def test_method_cache_to_disk():
    my_class = MyClass()

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baz")
    foo_baz_hash = generate_hash(("foo",), {"bar": "baz"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1  # The number of calls should still be 1 because the result is cached

    # Call the method with different arguments
    result = my_class.my_method("foo", bar="qux")
    foo_qux_hash = generate_hash(("foo",), {"bar": "qux"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'qux'}"
    assert my_class.number_of_method_calls[foo_qux_hash] == 1  # The number of calls should be 1 because the arguments are different

    # Call the method again with the first set of arguments
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"

    # Wait for cache to expire
    time.sleep(my_class.cache_expiration + 0.1)

    # Call the method after cache expiration
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because the cache has expired, so the method is called again

def test_cache_to_disk_with_ignore_cache_expiration():
    my_class = MyClass()

    fu_bar_hash = generate_hash(("fu",), {"bar": "bar"})

    # Call the method for the first time
    result = my_class.my_method("fu", bar="bar")
    assert result == "my_method with args: ('fu',), kwargs: {'bar': 'bar'}"
    assert my_class.number_of_method_calls[fu_bar_hash] == 1 # The number of calls should be 1 because the result is not cached yet

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("fu", bar="bar")
    assert result == "my_method with args: ('fu',), kwargs: {'bar': 'bar'}"
    assert fu_bar_hash in my_class.number_of_method_calls
    assert my_class.number_of_method_calls[fu_bar_hash] == 1  # The number of calls should still be 1 because the result is cached

    # Wait for cache to expire
    time.sleep(my_class.cache_expiration + 0.1)

    # Call the method with ignore_cache_expiration
    my_class.ignore_cache_expiration = True
    result = my_class.my_method("fu", bar="bar")
    assert result == "my_method with args: ('fu',), kwargs: {'bar': 'bar'}"
    assert fu_bar_hash in my_class.number_of_method_calls
    assert my_class.number_of_method_calls[fu_bar_hash] == 1  # The number of calls should be 1 because even though the cache has expired, as ignore_cache_expiration is True, the method is not called

def test_cache_to_disk_with_force_cache_expiration():
    my_class = MyClass()
    my_class.force_cache_expiration = True

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baz")
    foo_baz_hash = generate_hash(("foo",), {"bar": "baz"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache would normally expire)
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as force_cache_expiration is True, the method is called again

def test_cache_to_disk_with_cache_disabled():
    my_class = MyClass()
    my_class.cache_enabled = False

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baz")
    foo_baz_hash = generate_hash(("foo",), {"bar": "baz"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as cache_enabled is False, the method is called again

def test_cache_to_disk_with_cache_disabled_and_ignore_cache_expiration():
    my_class = MyClass()
    my_class.cache_enabled = False
    my_class.ignore_cache_expiration = True

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baz")
    foo_baz_hash = generate_hash(("foo",), {"bar": "baz"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as cache_enabled is False, the method is called again

def test_cache_to_disk_with_ignore_cache_expiration_and_force_cache_expiration():
    my_class = MyClass()
    my_class.ignore_cache_expiration = True
    my_class.force_cache_expiration = True

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baz")
    foo_baz_hash = generate_hash(("foo",), {"bar": "baz"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar="baz")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baz'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as ignore_cache_expiration is True, the method is called again

def test_cache_to_disk_on_property():
    # this should generate an exception, as the property decorator must be defined before the cache_to_disk decorator
    with pytest.raises(TypeError) as error_info:
        class IncorrectUsageOfCacheToDisk:
            @cache_to_disk
            @property # this should fail, as the property decorator must be defined before the cache_to_disk decorator
            def my_property(self):
                pass

def test_cache_to_disk_when_force_is_off_and_cache_expiration_is_not_set():
    # this should result in no caching, as cache_expiration is not set
    my_class = MyClass()
    my_class.force_cache_expiration = False
    my_class.cache_expiration = None

    # Call the method for the first time
    result = my_class.my_method("foo", bar="baw")
    foo_baw_hash = generate_hash(("foo",), {"bar": "baw"})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baw'}"
    assert my_class.number_of_method_calls[foo_baw_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar="baw")
    assert result == "my_method with args: ('foo',), kwargs: {'bar': 'baw'}"
    assert my_class.number_of_method_calls[foo_baw_hash] == 2  # The number of calls should be 2 because it is not possible to cache when cache_expiration is not set
