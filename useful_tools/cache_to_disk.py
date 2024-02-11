import re
import os
import time
import pickle
import inspect
from functools import wraps
from useful_tools.property_factory import PropertyFactory
from useful_tools.hash_functions import make_arg_hash

# decorators to cache the result of a function to disk
# this is used in order to avoid sending the same request multiple times

class FormattedCacheStatusProperty:
    """
    Descriptor class that provides a formatted representation of the cache status.
    This is used to provide the cache_status property on the instance with a decorated method.
    """
    def __get__(self, instance, owner):
        if not hasattr(instance, "cache_status_dict") or not instance.cache_status_dict:
            # if the cache_status_dict is not set, or if it is empty, return an empty string
            # this can't happen as of now, as the cache_status_dict is set in the wrapper function
            # so if you call cache_status on an instance before running the wrapped method
            # it will throw an AttributeError
            # it would be great to set this default behaviour, but does it really matter?
            # just don't call it before the method is run...
            return "" # pragma: no cover
        else:
            newline = "\n"
            # first split the dict into a list of strings, then join the list with newline
            # then join the list of strings with newline if it is a list, otherwise just return the string
            # the result is that you get the cache_status_dict_key on one line, followed by all the log entries for that key
            return newline.join(list(f"{k}: \n{newline.join([log_item for log_item in v]) if isinstance(v, list) else v}\n" for k, v in instance.cache_status_dict.items()))

def cache_to_disk(func):
    """
@cache_to_disk decorator to cache the result of a method to disk
uses pickle to save the result to disk
this decorator can only be used in classes that have the following attributes:
- cache_enabled           (True or False)
- cache_dir               (path to the cache directory)
- cache_expiration        (number of seconds to keep the cache file)
- force_cache_expiration  (True or False)
- ignore_cache_expiration (True or False)

If used in conjunction with @property, the property decorator must be defined before the cache_to_disk decorator, like this:

from useful_tools.cache_decorators import cache_to_disk
class MyClass:
    cache_enabled = True
    cache_dir = "cache"
    cache_expiration = 30 # seconds
    force_cache_expiration = False
    ignore_cache_expiration = False
    number_of_calls = 0
    
    @property
    @cache_to_disk
    def my_property(self):
        self.number_of_calls += 1
        return f"my_property called {self.number_of_calls} times"

myclass = MyClass()
print(myclass.my_property)  # prints "my_property called 1 times"
print(myclass.cache_status_dict) # gives info about the use of cache in the previous call
print(myclass.my_property)  # prints "my_property called 1 times", as the result is cached
print(myclass.cache_status_dict) # gives info about the use of cache in the previous call
    """
    # raise an error if the decorator is used on a property, as this will fail
    if isinstance(func, property):
        raise TypeError(f"Cannot cache a property. Apply @property above @cache_to_disk, not below.")

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # method to delete the last saved cache file
        def delete_last_saved_cache_file(self):
            if hasattr(self, "cache_status_dict") and "last_saved_cache_file" in self.cache_status_dict:
                file = self.cache_status_dict["last_saved_cache_file"]
                key  = self.cache_status_dict.get("last_saved_cache_file_key")
                if os.path.exists(file):
                    os.remove(file) # delete the file
                    del(self.cache_status_dict["last_saved_cache_file"]) # remove the key from the cache_status_dict
                    if key in self.cache_status_dict:
                        self.cache_status_dict[key].append("cache_file_deleted")
                    return file
            return None

        # Attach properties and methods to the instance
        type(self).cache_status = FormattedCacheStatusProperty()
        type(self).last_saved_cache_file = PropertyFactory(lambda self: self.cache_status_dict.get("last_saved_cache_file"))
        type(self).last_saved_cache_file_key = PropertyFactory(lambda self: self.cache_status_dict.get("last_saved_cache_file_key"))
        type(self).delete_last_saved_cache_file = delete_last_saved_cache_file

        result, cache_status_dict = execute_with_instance_and_cache(self, func, args, kwargs)

        # update cache_status_dict attribute
        if not hasattr(self, "cache_status_dict"):
            self.cache_status_dict = {}
        self.cache_status_dict.update(cache_status_dict)
        
        return result

    return wrapper

# TODO for v.1.00: rewrite this to use a more generic function that takes a config object as an argument in addition to the (optional) instance and function/method
# the input params for config_obj and instance should be separate, and only config_obj should be required
# it should return only the result and the cache status, and the last_saved_cache_file should be set as an attribute on the config object
# as it is not, it has become messy, as the origin of the decorator was to be used on a method.

def execute_with_cache(func, args, kwargs, config=None):
    """
    Executes a function with caching based on the provided configuration. 
    This is meant to be used on a function, rather than a method.

    Args:
        func: The function to be executed.
        args: The positional arguments to be passed to the function.
        kwargs: The keyword arguments to be passed to the function.
        config: The configuration object that determines how caching is handled.

    Returns:
        The result of the function execution.

    Raises:
        ValueError: If the config object is not provided or if cache is not enabled in the config.
    """
    if config is not None:
        # check if cache_enabled is defined in the config
        if hasattr(config, "cache_enabled"):
            result, cache_status_dict = execute_with_instance_and_cache(None, func, args, kwargs, config=config)
            if not hasattr(config, "cache_status_dict"):
                config.cache_status_dict = {}
            config.cache_status_dict.update(cache_status_dict)

            # TODO: Gotta find a better way of doing this, as these properties are duplicates of what is set in the wrapper function, and I don't like dupliation!
            # I'm sure there's a simple solution, but I don't have time to find it now.
            type(config).cache_status = FormattedCacheStatusProperty()
            type(config).last_saved_cache_file = PropertyFactory(lambda self: self.cache_status_dict.get("last_saved_cache_file"))
            type(config).last_saved_cache_file_key = PropertyFactory(lambda self: self.cache_status_dict.get("last_saved_cache_file_key"))
            
            return result
        else:
            raise ValueError("cache_enabled is not in the config -- is this a config object?")
    else:
        raise ValueError("config is required when using the execute_with_cache function")

def execute_with_instance_and_cache(instance, func, args, kwargs, config=None):
    """
    Execute the function and cache the result to disk.

    Parameters:
    instance (object): The instance of the class that the function belongs to. If the function is not a method, this should be None.
    func (function): The function to be executed and cached.
    args (tuple): The positional arguments to be passed to the function.
    kwargs (dict): The keyword arguments to be passed to the function.
    config (object, optional): The configuration object that determines the caching behavior. Defaults to None. If not provided, the cache_enabled attribute must be set on the instance.

    Returns:
    tuple: A tuple containing the result of the function execution, the path of the last saved cache file, and the cache status dictionary.
    """
    if config is None:
        config = instance

    # give a useful error message if the class doesn't have the required attributes
    required_attributes = ["cache_enabled", "cache_dir", "cache_expiration", "force_cache_expiration", "ignore_cache_expiration"]
    for attr in required_attributes:
        if not hasattr(config, attr):
            if config == instance: # the function is a method, and the config is set on the instance
                config_class_name = instance.__class__.__name__
            else:
                config_class_name = config.__module__ + '.' + config.__class__.__name__
            config_class_name = config.__class__.__name__
            raise AttributeError(f"{config_class_name} does not have the attribute '{attr}', required by the @cache_to_disk decorator.")

    arg_hash = make_arg_hash(args, kwargs)

    cache_status_dict = {}

    cache_status_dict_key = f"{inspect.getmodule(func).__name__}.{func.__qualname__}.{arg_hash}"
    # remove invalid characters from the key (as it's also used as a filename)
    cache_status_dict_key = re.sub(r'[<>:"/\\|?*]', '', cache_status_dict_key)
    # Note: for a function defined inside another function, __qualname__ may look like this: 'test_execute_with_instance_and_cache_disabled.<locals>.test_func'
    # it is therefore crucial to remove the invalid characters from the key, as it is used as a filename

    cache_status_dict[cache_status_dict_key] = []
    cache_status_dict["last_saved_cache_file"] = None
    cache_status_dict["last_saved_cache_file_key"] = None

    # If cache is disabled, call the function and return the result
    # when mocking requests, the cache is disabled
    # this is done in handle_request() in main.py
    if not config.cache_enabled:
        cache_status_dict[cache_status_dict_key].append("cache_disabled")
        cache_status_dict[cache_status_dict_key].append("method_called")
        return execute_func(func, instance, *args, **kwargs), cache_status_dict
    
    # Create cache directory if it doesn't exist
    if not os.path.exists(config.cache_dir):
        os.makedirs(config.cache_dir)
    
    # Create a unique filename based on the class name, method name and arguments
    filename = f"{cache_status_dict_key}.pkl"
    filepath = os.path.join(config.cache_dir, filename)

    read_from_cache = False
    if config.ignore_cache_expiration:
        if config.force_cache_expiration:
            cache_status_dict[cache_status_dict_key].append("ignore_cache_expiration and force_cache_expiration are both True - force_cache_expiration takes precedence")
        else:
            cache_status_dict[cache_status_dict_key].append("cache_expiration_ignored")
            read_from_cache = True

    if config.force_cache_expiration:
        cache_status_dict[cache_status_dict_key].append("cache_expiration_forced")
        read_from_cache = False
    else:
        if config.cache_expiration is not None:
            cache_status_dict[cache_status_dict_key].append(f"cache_expiration_set: {config.cache_expiration}s")
            read_from_cache = True
        else:
            cache_status_dict[cache_status_dict_key].append("cache_expiration_not_set")
            read_from_cache = False
        
    if read_from_cache:
        if not os.path.exists(filepath):
            cache_status_dict[cache_status_dict_key].append("cache_file_does_not_exist")
        else:
            cache_status_dict[cache_status_dict_key].append("cache_file_exists")
            with open(filepath, 'rb') as f:
                try:
                    cache_time, result = pickle.load(f)
                    time_since_cache = time.time() - cache_time
                    skip_cache_file = False
                except EOFError:
                    cache_status_dict[cache_status_dict_key].append("cache_file_corrupted")
                    skip_cache_file = True
                if not skip_cache_file:
                    if config.ignore_cache_expiration \
                    or time_since_cache < config.cache_expiration:
                        cache_status_dict[cache_status_dict_key].append("cache_loaded")
                        return result, cache_status_dict
                    else:
                        if time_since_cache < 10:
                            time_since_cache_formatted = f"{time_since_cache:.3f}s"
                        # the following lines are not covered by tests, as it is not possible to mock time.time()
                        elif time_since_cache < 60:                                         #  pragma: no cover
                            time_since_cache_formatted = f"{time_since_cache:.1f}s"         #  pragma: no cover
                        elif time_since_cache < 3600:                                       #  pragma: no cover
                            time_since_cache_formatted = f"{time_since_cache/60:.1f}m"      #  pragma: no cover
                        else:                                                               #  pragma: no cover
                            time_since_cache_formatted = f"{time_since_cache/3600:.1f}h"    #  pragma: no cover
                        cache_status_dict[cache_status_dict_key].append(f"cache_expired: {time_since_cache_formatted} passed")
    
    # call the function - this will happen if the cache_expiration is not set or the cache file doesn't exist or is expired
    result = execute_func(func, instance, *args, **kwargs)
    cache_status_dict[cache_status_dict_key].append("method_called")

    # If cache is enabled for the model (or cache is forced to expire), save the result to the cache
    if config.cache_expiration is not None or config.force_cache_expiration:
        with open(filepath, 'wb') as f:
            pickle.dump((time.time(), result), f)
            cache_status_dict[cache_status_dict_key].append("cache_saved")
        cache_status_dict["last_saved_cache_file"] = filepath
        cache_status_dict["last_saved_cache_file_key"] = cache_status_dict_key
    
    return result, cache_status_dict

def execute_func(func, instance, *args, **kwargs):
    if instance is not None:
        return func(instance, *args, **kwargs)
    else:
        return func(*args, **kwargs)
