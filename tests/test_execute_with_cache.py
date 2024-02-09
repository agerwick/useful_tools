# these are not great tests, I just tested autogenerating the test cases with copilot after separating execute_with_cache into a separate function
# some were modified to actually work, others deleted as they didn't make sense
# more things are tested in the original test file (test_cache_to_disk.py)

import os
import pickle
import time
import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock
from useful_tools.cache_decorators import execute_with_cache

def _test_func(*args, **kwargs):
    return "result"

def test_execute_with_cache_disabled():
    config_obj = MagicMock()
    config_obj.cache_enabled = False

    args = ("test_execute_with_cache_disabled", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert cache_file is None

def test_execute_with_cache_enabled():
    config_obj = MagicMock()
    config_obj.cache_enabled = True
    config_obj.cache_dir = "test_cache"
    config_obj.cache_expiration = 60

    args = ("test_execute_with_cache_enabled", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert cache_file is not None
    assert os.path.exists(cache_file)

    # Clean up the cache file
    os.remove(cache_file)

def test_execute_with_cache_expired():
    config_obj = MagicMock()
    config_obj.cache_enabled = True
    config_obj.cache_dir = "test_cache"
    config_obj.cache_expiration = 1

    args = ("test_execute_with_cache_expired", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    cache_file = os.path.join(config_obj.cache_dir, "_test_func._test_func_arg1_arg2_kwarg1_value1_kwarg2_value2.pkl")
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired_result"), f)

    result, new_cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert new_cache_file is not None
    assert new_cache_file != cache_file
    assert os.path.exists(new_cache_file)

    # Clean up the cache files
    os.remove(cache_file)
    os.remove(new_cache_file)

def test_execute_with_cache_ignore_cache_expiration():
    config_obj = MagicMock()
    config_obj.cache_enabled = True
    config_obj.cache_dir = "test_cache"
    config_obj.cache_expiration = 60
    config_obj.ignore_cache_expiration = True

    args = ("test_execute_with_cache_ignore_cache_expiration", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file with an expired cache
    cache_file = os.path.join(config_obj.cache_dir, "_test_func._test_func_arg1_arg2_kwarg1_value1_kwarg2_value2.pkl")
    with open(cache_file, "wb") as f:
        pickle.dump((time.time() - 10, "expired_result"), f)

    result, new_cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert new_cache_file is not None
    assert new_cache_file != cache_file
    assert os.path.exists(new_cache_file)

    # Clean up the cache files
    os.remove(cache_file)
    os.remove(new_cache_file)

def test_execute_with_cache_cache_disabled():
    config_obj = MagicMock()
    config_obj.cache_enabled = False

    test_name = "test_execute_with_cache_cache_disabled_and_ignore_cache_expiration"
    args = (test_name, "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # execute, which should not generate a cache file
    result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert cache_file is None # cache was not saved

def test_execute_with_cache_force_cache_expiration():
    config_obj = MagicMock()
    config_obj.cache_enabled = True
    config_obj.cache_dir = "test_cache"
    config_obj.cache_expiration = 60
    config_obj.force_cache_expiration = True
    config_obj.ignore_cache_expiration = False

    args = ("arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # Create a cache file
    result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    # attempt to get result from cache, which should not generate a new cache file
    result, new_cache_file, new_cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "result"
    assert new_cache_file is not None
    assert new_cache_file == cache_file
    assert os.path.exists(new_cache_file)

    # Clean up the cache files
    os.remove(cache_file)

def test_execute_with_cache_cache_file_exists():
    config_obj = MagicMock()
    config_obj.cache_enabled = True
    config_obj.cache_dir = "test_cache"
    config_obj.cache_expiration = 60
    config_obj.force_cache_expiration = False
    config_obj.ignore_cache_expiration = False

    args = ("test_execute_with_cache_cache_file_exists", time.time(), "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}
    result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    # overwrite cache file
    with open(cache_file, "wb") as f:
        pickle.dump((time.time(), "cached_result"), f)

    # get result from cache
    result, new_cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj)

    assert result == "cached_result"
    assert new_cache_file is None # no new cache file created

    # Clean up the cache file
    os.remove(cache_file)

def test_execute_with_cache_with_invalid_cofig():
    config_obj = SimpleNamespace() # invalid config object

    args = ("test_execute_with_cache_with_invalid_cofig", "arg1", "arg2")
    kwargs = {"kwarg1": "value1", "kwarg2": "value2"}

    # make sure if it raises an exception
    with pytest.raises(ValueError) as error_info:
        result, cache_file, cache_status = execute_with_cache(_test_func, args, kwargs, config=config_obj) # pragma: no cover

