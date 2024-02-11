import os
import pickle
import time
import pytest
import shutil
import inspect
from types import SimpleNamespace
from useful_tools.cache_to_disk import execute_with_cache


def _test_name():
    """
    Get the test name (the function name, basically)
    IMPORTANT!
    As we're testing caching, we need to make sure that the parameters we send to my_method is different in each test, otherwise the function may have been called by another test and the result cached - then the method will not be called again, and the test will fail.
    If we include the test name in the parameters, we can be sure that the parameters are different in each test.
    """
    return str(inspect.stack()[1].function)

class MockConfig:
    cache_dir = "test_cache"
    def __init__(self):
        self.cache_enabled = True
        self.cache_expiration = 2
        self.ignore_cache_expiration = False
        self.force_cache_expiration = False

def setup_module(module):
    # don't create the dir - the module should create it
    # if not os.path.exists(MyClass.cache_dir):
    #     os.makedirs(MyClass.cache_dir)
    pass

def teardown_module(module):
    try:
        shutil.rmtree(MockConfig.cache_dir)
    except: # pragma: no cover
        pass # pragma: no cover

def _test_func(*args, **kwargs):
    # this is the function we want to cache
    return "result"

def test_execute_with_cache_disabled():
    config_obj = MockConfig()
    config_obj.cache_enabled = False

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert config_obj.last_saved_cache_file is None

def test_execute_with_cache_enabled():
    config_obj = MockConfig()

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert config_obj.last_saved_cache_file is not None
    assert os.path.exists(config_obj.last_saved_cache_file)

    # Clean up the cache file
    os.remove(config_obj.last_saved_cache_file)

def test_execute_with_cache_expired():
    config_obj = MockConfig()
    config_obj.cache_expiration = 1

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    cache_file = config_obj.last_saved_cache_file
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired_result"), f)

    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    new_cache_file = config_obj.last_saved_cache_file

    assert result == "result" # the function was called again
    assert new_cache_file is not None # a new cache file was created
    assert new_cache_file == cache_file # the new cache file is the same as the old one
    assert os.path.exists(new_cache_file) # the new cache file exists

def test_execute_with_cache_ignore_cache_expiration():
    config_obj = MockConfig()
    config_obj.ignore_cache_expiration = True

    args = ("test_execute_with_cache_ignore_cache_expiration", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    cache_file = config_obj.last_saved_cache_file
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired_result"), f)

    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    new_cache_file = config_obj.last_saved_cache_file

    assert result == "expired_result" # the function was not called again because we ignore the cache expiration

def test_execute_with_cache_cache_disabled():
    config_obj = MockConfig()
    config_obj.cache_enabled = False

    test_name = "test_execute_with_cache_cache_disabled_and_ignore_cache_expiration"
    args = (test_name, "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # execute, which should not generate a cache file
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert config_obj.last_saved_cache_file is None # cache was not saved

def test_execute_with_cache_force_cache_expiration():
    config_obj = MockConfig()
    config_obj.force_cache_expiration = True

    args = ("arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    first_cache_file = config_obj.last_saved_cache_file

    # attempt to get result from cache, which should not generate a new cache file
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert config_obj.last_saved_cache_file is not None
    assert config_obj.last_saved_cache_file == first_cache_file
    assert os.path.exists(config_obj.last_saved_cache_file)

    # Clean up the cache files
    os.remove(config_obj.last_saved_cache_file)

def test_execute_with_cache_cache_file_exists():
    config_obj = MockConfig()
    config_obj.cache_expiration = 600 # helps when debugging the test

    args = (_test_name(), time.time(), "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    # overwrite cache file
    with open(config_obj.last_saved_cache_file, "wb") as f:
        pickle.dump((time.time(), "cached_result"), f)

    # get result from cache
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "cached_result"
    assert config_obj.last_saved_cache_file is None # no new cache file created

def test_execute_with_cache_with_invalid_cofig():
    config_obj = SimpleNamespace() # invalid config object

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # make sure if it raises an exception
    with pytest.raises(ValueError) as error_info:
        result = execute_with_cache(_test_func, args, kwargs, config=config_obj) # pragma: no cover

def test_execute_with_cache_with_no_cofig():
    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # make sure if it raises an exception
    with pytest.raises(ValueError) as error_info:
        result = execute_with_cache(_test_func, args, kwargs) # pragma: no cover

def test_with_non_existing_attrs():
    required_attributes = [("cache_enabled", ValueError), ("cache_expiration", AttributeError), ("force_cache_expiration", AttributeError), ("ignore_cache_expiration", AttributeError)] # cache_dir is set on the class, so it's not included here

    for attr, errClass in required_attributes:    
        config_obj = MockConfig() # make a new instance
        delattr(config_obj, attr)

        args = (_test_name(), attr)
        kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

        # check that it raises AttributeError or ValueError:
        with pytest.raises(errClass):
            result = execute_with_cache(_test_func, args, kwargs, config=config_obj) # pragma: no cover

def test_with_0byte_cache_file():
    config_obj = MockConfig()

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with 0 bytes
    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    cache_file = config_obj.last_saved_cache_file
    with open(cache_file, "wb") as f:
        pass

    result = execute_with_cache(_test_func, args, kwargs, config=config_obj)
    new_cache_file = config_obj.last_saved_cache_file

    assert result == "result" # the function was called again
