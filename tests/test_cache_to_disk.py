import pytest
import time
import shutil
import inspect
from useful_tools.cache_to_disk import cache_to_disk, make_arg_hash

def _test_name():
    """
    Get the test name (the function name, basically)
    IMPORTANT!
    As we're testing caching, we need to make sure that the parameters we send to my_method is different in each test, otherwise the method may have been called by another test and the result cached - then the method will not be called again, and the test will fail.
    If we include the test name in the parameters, we can be sure that the parameters are different in each test.
    """
    return str(inspect.stack()[1].function)

class MyClass:
    cache_enabled = True
    cache_dir = "test_cache"
    cache_expiration = 0.5 # seconds
    
    def __init__(self):
        self.number_of_property_calls = 0
        self.number_of_method_calls = {}
        self.number_of_method_calls_total = 0
        self.force_cache_expiration = False
        self.ignore_cache_expiration = False

    @property
    @cache_to_disk
    def my_property(self):
        self.number_of_property_calls += 1
        return "my_property"

    @cache_to_disk
    def my_method(self, *args, **kwargs):
        # make a hash of the arguments
        hash = make_arg_hash(args, kwargs)
        # count the number of calls to this method with these arguments
        if self.number_of_method_calls.get(hash) is None:
            self.number_of_method_calls[hash] = 0
        self.number_of_method_calls[hash] += 1
        self.number_of_method_calls_total += 1
        return "my_method with args: {}, kwargs: {}".format(args, kwargs)

def setup_module(module):
    # don't create the dir - the module should create it
    # if not os.path.exists(MyClass.cache_dir):
    #     os.makedirs(MyClass.cache_dir)
    pass

def teardown_module(module):
    try:
        shutil.rmtree(MyClass.cache_dir)
    except: # pragma: no cover
        pass # pragma: no cover

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

def test_cache_to_disk_on_property():
    # this should generate an exception, as the property decorator must be defined before the cache_to_disk decorator
    with pytest.raises(TypeError) as error_info:
        class IncorrectUsageOfCacheToDisk:
            @cache_to_disk
            @property # this should fail, as the property decorator must be defined before the cache_to_disk decorator
            def my_property(self):
                pass  # pragma: no cover

def test_method_cache_to_disk():
    my_class = MyClass()
    test = _test_name()

    # Call the method for the first time
    result = my_class.my_method("foo", bar=test)
    foo_baz_hash = make_arg_hash(("foo",), {"bar": _test_name()})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': '" + test + "'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar=_test_name())
    assert my_class.number_of_method_calls[foo_baz_hash] == 1  # The number of calls should still be 1 because the result is cached

    # Call the method with different arguments
    result = my_class.my_method("foo", bar="qux", x=_test_name())
    foo_qux_hash = make_arg_hash(("foo",), {"bar": "qux", "x": test})
    assert my_class.number_of_method_calls[foo_qux_hash] == 1  # The number of calls should be 1 because the arguments are different

    # Call the method again with the first set of arguments
    result = my_class.my_method("foo", bar=test)
    assert my_class.number_of_method_calls[foo_baz_hash] == 1 # The number of calls should still be 1 because the result is cached
    assert my_class.number_of_method_calls_total == 2 # The total number of calls should be 2 (one for each set of arguments)

    # Wait for cache to expire
    time.sleep(my_class.cache_expiration + 0.1)

    # Call the method after cache expiration
    result = my_class.my_method("foo", bar=_test_name())
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because the cache has expired, so the method is called again

def test_cache_to_disk_with_ignore_cache_expiration():
    my_class = MyClass()
    test = _test_name()

    fu_bar_hash = make_arg_hash((test,), {"bar": "bar"})

    # Call the method for the first time
    my_class.my_method(test, bar="bar")
    assert my_class.number_of_method_calls[fu_bar_hash] == 1 # The number of calls should be 1 because the result is not cached yet

    # Call the method for the second time (before cache expiration)
    my_class.my_method(test, bar="bar")
    assert fu_bar_hash in my_class.number_of_method_calls
    assert my_class.number_of_method_calls[fu_bar_hash] == 1  # The number of calls should still be 1 because the result is cached

    # Wait for cache to expire
    time.sleep(my_class.cache_expiration + 0.1)

    # Call the method with ignore_cache_expiration
    my_class.ignore_cache_expiration = True
    my_class.my_method(test, bar="bar")
    assert fu_bar_hash in my_class.number_of_method_calls
    assert my_class.number_of_method_calls[fu_bar_hash] == 1  # The number of calls should be 1 because even though the cache has expired, as ignore_cache_expiration is True, the method is not called

def test_cache_to_disk_with_force_cache_expiration():
    my_class = MyClass()
    my_class.force_cache_expiration = True

    # Call the method for the first time
    result = my_class.my_method("FOO", bar="BAR")
    foo_baz_hash = make_arg_hash(("FOO",), {"bar": "BAR"})
    assert result == "my_method with args: ('FOO',), kwargs: {'bar': 'BAR'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache would normally expire)
    result = my_class.my_method("FOO", bar="BAR")
    assert result == "my_method with args: ('FOO',), kwargs: {'bar': 'BAR'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as force_cache_expiration is True, the method is called again

def test_cache_to_disk_with_cache_disabled():
    my_class = MyClass()
    my_class.cache_enabled = False
    test = _test_name()

    # Call the method for the first time
    my_class.my_method(test, kwarg="hey!")
    foo_baz_hash = make_arg_hash((test,), {"kwarg": "hey!"})
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    my_class.my_method(test, kwarg="hey!")
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as cache_enabled is False, the method is called again

def test_cache_to_disk_with_cache_disabled_and_ignore_cache_expiration():
    my_class = MyClass()
    my_class.cache_enabled = False
    my_class.ignore_cache_expiration = True
    test = _test_name()

    # Call the method for the first time
    result = my_class.my_method("fu", bar=test)
    foo_baz_hash = make_arg_hash(("fu",), {"bar": test})
    assert result == "my_method with args: ('fu',), kwargs: {'bar': '" + test + "'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("fu", bar=test)
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as cache_enabled is False, the method is called again

def test_cache_to_disk_with_ignore_cache_expiration_and_force_cache_expiration():
    my_class = MyClass()
    my_class.ignore_cache_expiration = True
    my_class.force_cache_expiration = True
    test = _test_name()

    # Call the method for the first time
    result = my_class.my_method("foo", bar=test)
    foo_baz_hash = make_arg_hash(("foo",), {"bar": test})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': '" + test + "'}"
    assert my_class.number_of_method_calls[foo_baz_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar=test)
    assert my_class.number_of_method_calls[foo_baz_hash] == 2  # The number of calls should be 2 because even though the result is cached and the cache has not expired, as ignore_cache_expiration is True, the method is called again

def test_cache_to_disk_when_force_is_off_and_cache_expiration_is_not_set():
    # this should result in no caching, as cache_expiration is not set
    my_class = MyClass()
    my_class.force_cache_expiration = False
    my_class.cache_expiration = None
    test = _test_name()

    # Call the method for the first time
    result = my_class.my_method("foo", bar=test)
    foo_bar_hash = make_arg_hash(("foo",), {"bar": test})
    assert result == "my_method with args: ('foo',), kwargs: {'bar': '" + test + "'}"
    assert my_class.number_of_method_calls[foo_bar_hash] == 1

    # Call the method for the second time (before cache expiration)
    result = my_class.my_method("foo", bar=test)
    assert my_class.number_of_method_calls[foo_bar_hash] == 2  # The number of calls should be 2 because it is not possible to cache when cache_expiration is not set


#### rewrite these tests below, they're not good at all
#### find a different way to test the number of method calls as it's getting too complex to have to make a hash of the arguments
#### maybe just use a global variable that is incremented each time the method is called, and then check that variable instead, like on the cache_to_memory tests
#### or maybe both
    
def test_cache_to_disk_with_args():
    my_class = MyClass()
    test = _test_name()
    the_first_args = ("my_arg", "another_arg", test)
    the_first_hash = make_arg_hash(the_first_args, {})

    # Call the method for the first time
    my_class.my_method(*the_first_args) # * unpack the list of arguments

    # Call the method for the second time with the same arguments
    the_second_args = tuple(list(the_first_args)) # make a copy of the tuple
    the_second_hash = make_arg_hash(the_second_args, {})
    my_class.my_method(*the_second_args)
    assert the_first_hash == the_second_hash # the hashes should be the same because the arguments are the same
    assert my_class.number_of_method_calls[the_first_hash] == 1  # The number of calls should still be 1 because the result is cached

    my_class.force_cache_expiration = True

    my_class.my_method(*the_first_args)
    assert my_class.number_of_method_calls[the_first_hash] == 2  # The number of calls should be 2 because cache has expired

    # Call the method for the third time with different arguments
    the_third_args = ("my_third_arg", test)
    the_third_hash = make_arg_hash(the_third_args, {})
    my_class.my_method(*the_third_args)
    assert my_class.number_of_method_calls[the_third_hash] == 1 # first call with these arguments
    assert my_class.number_of_method_calls[the_first_hash] == 2 # second call with the first set of arguments

    my_class.force_cache_expiration = False

    # Call the method for the fourth time with the same arguments in a different order
    the_first_args_reversed = tuple(list(tuple(reversed(the_first_args))))
    the_first_args_reversed_hash = make_arg_hash(the_first_args_reversed, {})
    my_class.my_method(*the_first_args_reversed)
    assert my_class.number_of_method_calls[the_first_args_reversed_hash] == 1 # The number of calls should be 1 because the arguments are different

def test_cache_with_non_hashable_args():
    my_class = MyClass()
    test = _test_name()

    # call the method with non-hashable arguments, which the cache function should handle
    result = my_class.my_method([1,2,3,test])
    assert result == "my_method with args: ([1, 2, 3, '" + test + "'],), kwargs: {}"
    assert my_class.number_of_method_calls_total == 1
    
    # call a second time with the same arguments, which should be cached
    result = my_class.my_method([1,2,3,test]) # does not increase total calls
    assert my_class.number_of_method_calls_total == 1

    # call with different arguments, which should not be cached
    result = my_class.my_method([4,5,6,test]) # increases total calls to 2
    assert my_class.number_of_method_calls_total == 2 

    # call with same argument as the first one, but in a different order, which should *not* be cached
    result = my_class.my_method([test,3,2,1]) # should increase total num of calls to 3
    assert result == "my_method with args: (['" + test + "', 3, 2, 1],), kwargs: {}"
    assert my_class.number_of_method_calls_total == 3

def test_cache_with_kwargs():
    my_class = MyClass()
    test = _test_name()
    # call the method with kwargs, which the cache function should handle
    my_class.my_method(my_kwarg = "my_value", my_other_kwarg = test) # call#1
    # call a second time with the same arguments, which should be cached
    my_class.my_method(my_kwarg = "my_value", my_other_kwarg = test) # still just one call
    assert my_class.number_of_method_calls_total == 1
    # call with different arguments, which should *not* be cached
    my_class.my_method(my_kwarg = test) # call#2
    assert my_class.number_of_method_calls_total == 2

def test_cache_with_kwargs_in_different_order():
    my_class = MyClass()
    test = _test_name()
    my_class.my_method(my_kwarg = "1", my_other_kwarg = test)
    # call with same arguments in a different order, which should be cached, as the order or kwargs should not matter
    my_class.my_method(my_other_kwarg = test, my_kwarg = "1")
    assert my_class.number_of_method_calls_total == 1

def test_cache_with_kwargs_in_different_order_with_other_random_calls_between_them():
    my_class = MyClass()
    test = _test_name()
    my_class.my_method(do_you_speak = "hablas", spanish = "español", test = test) # call#1
    assert my_class.number_of_method_calls_total == 1
    # make some other random calls between the two calls
    my_class.my_method(kwarg1 = "!") #call#2
    my_class.my_method(kwarg1 = "!!") #call#3
    my_class.my_method("I", "have", "lots", "of", "arguments") #call#4
    assert my_class.number_of_method_calls_total == 4
    # call with same arguments in a different order, which should be cached
    my_class.my_method(spanish = "español", do_you_speak = "hablas", test = test) # should be cached, so no new call
    assert my_class.number_of_method_calls_total == 4

def test_cache_to_disk_with_corrupt_cache_file():
    my_class = MyClass()
    my_class.force_cache_expiration = True
    test = _test_name()
    # call the method with some arguments, generating a new cache file
    my_class.my_method("foo", bar=test) # call#1
    # corrupt the cache file
    with open(my_class.cache_status_dict["last_saved_cache_file"], "w") as f:
        f.write("")
    # call the method again, which should result in a new call
    my_class.my_method("foo", bar=test) # call#2
    assert my_class.number_of_method_calls_total == 2

def test_formatted_cache_status():
    my_class = MyClass()
    test = _test_name()
    # call the method with some arguments, generating a new cache file
    my_class.my_method(test) # call#1
    # make sure the result of cache_status is a string
    assert my_class.cache_status.__class__ == str
    assert my_class.cache_status_dict.__class__ == dict

def test_if_we_get_empty_cache_status_when_called_before_method():
    class MyOtherClass: 
        # we're using a different class here, because we want to test the cache_status property before the method has been called, and we don't want the other tests to interfere with this one
        @cache_to_disk
        def my_method(self, *args, **kwargs): # pragma: no cover
            pass # pragma: no cover
    my_class = MyOtherClass()
    # check that we get an AttributeError when calling cache_status before the method has been called
    with pytest.raises(AttributeError):
        my_class.cache_status
    # this would be ideal:
    # assert my_class.cache_status == ""
    # but it's not possible, because the cache_status property is set when the decorated method is called, so it doesn't exist at this point.
