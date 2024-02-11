import os
import pickle
import time
import shutil
import inspect
import pytest
from unittest.mock import MagicMock
from useful_tools.cache_to_disk import execute_with_instance_and_cache

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


def test_execute_with_instance_and_cache_disabled():
    config_obj = MockConfig()
    config_obj.cache_enabled = False

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)

    assert result == "result"
    assert cache_log.get("last_saved_cache_file") is None

def test_execute_with_instance_and_cache_enabled():
    config_obj = MockConfig()
    config_obj.cache_enabled = True

    args = (_test_name, "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)

    assert result == "result"
    assert cache_log.get("last_saved_cache_file") is not None
    assert os.path.exists(cache_log.get("last_saved_cache_file"))

def test_execute_with_instance_and_cache_expired():
    config_obj = MockConfig()
    config_obj.cache_expiration = 1

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    cache_file = cache_log.get("last_saved_cache_file")
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired_result"), f)

    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    new_cache_file = cache_log.get("last_saved_cache_file")

    assert result == "result"
    assert new_cache_file is not None
    assert new_cache_file == cache_file
    assert os.path.exists(new_cache_file)

def test_execute_with_instance_and_cache_ignore_cache_expiration():
    config_obj = MockConfig()
    config_obj.ignore_cache_expiration = True

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    cache_file = cache_log.get("last_saved_cache_file")
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired result"), f)

    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    new_cache_file = cache_log.get("last_saved_cache_file")
    assert result == "expired result" # cache expiration was ignored and the technically expired result was returned

def test_execute_with_instance_and_cache_cache_disabled():
    config_obj = MockConfig()
    config_obj.cache_enabled = False

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # execute, which should not generate a cache file
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)

    assert result == "result"
    assert cache_log.get("last_saved_cache_file") is None # cache was not saved

def test_execute_with_instance_and_cache_force_cache_expiration():
    config_obj = MockConfig()
    config_obj.force_cache_expiration = True

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    cache_file = cache_log.get("last_saved_cache_file")
    assert cache_file is not None
    
    # overwrite cache file with a different result
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "the first result"), f)

    # attempt to get result from cache, which should result in the function being called again
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    new_cache_file = cache_log.get("last_saved_cache_file")
    assert result == "result"
    assert new_cache_file is not None
    assert new_cache_file == cache_file

def test_execute_with_instance_and_cache_cache_file_exists():
    config_obj = MockConfig()

    args = (_test_name(), time.time(), "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}
    result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    cache_file = cache_log.get("last_saved_cache_file")

    # overwrite cache file
    with open(cache_file, "wb") as f:
        pickle.dump((time.time(), "cached_result"), f)

    # get result from cache
    result, new_cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs)
    new_cache_file = new_cache_log.get("last_saved_cache_file")

    assert result == "cached_result"
    assert new_cache_file is None # no new cache file created

def test_with_config_with_invalid_cache_dir():
    config_obj = MockConfig()
    config_obj.cache_dir = None

    args = (_test_name(), "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # check that it raises a TypeError:
    with pytest.raises(TypeError):
        result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs) # pragma: no cover

def test_with_config_that_lacks_cache_settings():

    required_attributes = ["cache_enabled", "cache_expiration", "force_cache_expiration", "ignore_cache_expiration"] # cache_dir is set on the class, so it's not included here

    for attr in required_attributes:    
        config_obj = MockConfig() # make a new instance
        delattr(config_obj, attr)

        args = (_test_name(), attr, "arg2")
        kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

        # check that it raises an AttributeError:
        with pytest.raises(AttributeError):
            result, cache_log = execute_with_instance_and_cache(config_obj, _test_func, args, kwargs) # pragma: no cover
