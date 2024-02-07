import os
import time
import pickle
import hashlib
from functools import wraps

# decorators to cache the result of a function
# this is used in order to avoid sending the same request multiple times
# cache_property works only for properties, while cache_to_memory and cache_to_disk works for any function

def make_hashable(obj):
    """make an object hashable, so it can be used as an identifier for the cache"""
    # recursively convert lists and dicts to tuples and frozensets
    if isinstance(obj, (tuple, list)):
        # the order og args is relevant, so the order of the items in the tuple should not be changed
        return tuple(make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        # sort the dict by key before converting to frozenset, as the order of kwargs (and keys in a dict) is not relevant, so the order of the keys should not affect the hash
        return frozenset((k, make_hashable(v)) for k, v in sorted(obj.items()))
    return obj

def make_arg_hash(args, kwargs):
    """make a hash of the arguments that can be used to check if the arguments are the same as something that was previously cached"""
    # preserve the order or args, so calling a function with the same arguments in a different order will NOT give the same hash
    # this is important for the cache, because the cache should not be used if the arguments are different
    # frozenset is used because it makes the args hashable
    # the arguments are put in a list of one item before being converted to a frozenset to preserve the order of the arguments
    hashable_args = make_hashable([args])
    hashable_kwargs = make_hashable(kwargs)
    encoded_arg_str = f"{hashable_args}_{hashable_kwargs}".encode()
    sha256hash = hashlib.sha256(encoded_arg_str).hexdigest()
    return sha256hash

def cache_property(func):
    """
Legacy decorator to cache the result of a property to memory. You can now use the @cache_to_memory decorator instead, as long as you define the property decorator before the cache_to_memory decorator, like this:
@property
@cache_to_memory
def my_property(self):
    return "my_property"
    """
    @wraps(func)
    def wrapper(self):
        attr_name = f"_{func.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper

def cache_to_memory(func):
    """
@cache_to_memory decorator to cache the result of a method to memory
If used in conjunction with @property, the property decorator must be defined before the cache_to_memory decorator, like this:

from useful_tools.cache_decorators import cache_to_memory
class MyClass:
    def __init__(self):
        self.counter = 0
    @property # you can of course skip the @property decorator and have a method that returns a value
    @cache_to_memory
    def my_property(self):
        self.counter += 1
        return f"my_property was called {self.counter} times"

my_object = MyClass()
print(my_object.my_property) # should show that my_property was called 1 time
print(my_object.my_property) # should show that my_property was called 1 time again, because it was cached
    """
    if isinstance(func, property):
        raise TypeError(f"Cannot cache a property. Apply @property above @cache_to_memory, not below.")
    
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        attr_name = func.__name__
        arg_hash = make_arg_hash(args, kwargs)
        if attr_name not in cache:
            cache[attr_name] = {}
        if arg_hash not in cache[attr_name]:
            cache[attr_name][arg_hash] = func(*args, **kwargs)
        return cache[attr_name][arg_hash]
    return wrapper

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
print(myclass.cache_status) # gives info about the use of cache in the previous call
print(myclass.my_property)  # prints "my_property called 1 times", as the result is cached
print(myclass.cache_status) # gives info about the use of cache in the previous call
    """
    # raise an error if the decorator is used on a property, as this will fail
    if isinstance(func, property):
        raise TypeError(f"Cannot cache a property. Apply @property above @cache_to_disk, not below.")
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # # give a useful error message if the class doesn't have the required attributes
        # required_attributes = ["cache_enabled", "cache_dir", "cache_expiration", "force_cache_expiration", "ignore_cache_expiration"]
        # for attr in required_attributes:
        #     if not hasattr(self, attr):
        #         raise AttributeError(f"{self.__class__.__name__} does not have the attribute '{attr}', required by the @cache_to_disk decorator.")

        result, self.last_saved_cache_file, cache_status = execute_with_instance_and_cache(self, func, args, kwargs)

        # update cache_status attribute
        if not hasattr(self, "cache_status"):
            self.cache_status = {}
        self.cache_status.update(cache_status)
        
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
            result, delete_last_saved_cache_file, cache_status = execute_with_instance_and_cache(None, func, args, kwargs, config=config)
            return result, delete_last_saved_cache_file, cache_status
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
                config_class_name = config.__name__
            config_class_name = config.__class__.__name__
            raise AttributeError(f"{config_class_name} does not have the attribute '{attr}', required by the @cache_to_disk decorator.")

    arg_hash = make_arg_hash(args, kwargs)

    last_saved_cache_file = None
    cache_status = {}
    cache_status_key = f"{func.__class__.__name__}.{func.__name__}_{arg_hash}"
    cache_status[cache_status_key] = []

    # If cache is disabled, call the function and return the result
    # when mocking requests, the cache is disabled
    # this is done in handle_request() in main.py
    if not config.cache_enabled:
        cache_status[cache_status_key].append("cache_disabled")
        cache_status[cache_status_key].append("method_called")
        return execute_func(func, instance, *args, **kwargs), None, cache_status
    
    # Create cache directory if it doesn't exist
    if not os.path.exists(config.cache_dir):
        os.makedirs(config.cache_dir)
    
    # Create a unique filename based on the class name, method name and arguments
    filename = f"{cache_status_key}.pkl"
    filepath = os.path.join(config.cache_dir, filename)

    read_from_cache = False
    if config.ignore_cache_expiration:
        if config.force_cache_expiration:
            cache_status[cache_status_key].append("ignore_cache_expiration and force_cache_expiration are both True - force_cache_expiration takes precedence")
        else:
            cache_status[cache_status_key].append("cache_expiration_ignored")
            read_from_cache = True

    if config.force_cache_expiration:
        cache_status[cache_status_key].append("cache_expiration_forced")
        read_from_cache = False
    else:
        if config.cache_expiration is not None:
            cache_status[cache_status_key].append(f"cache_expiration_set: {config.cache_expiration}s")
            read_from_cache = True
        else:
            cache_status[cache_status_key].append("cache_expiration_not_set")
            read_from_cache = False
        
    if read_from_cache:
        if not os.path.exists(filepath):
            cache_status[cache_status_key].append("cache_file_does_not_exist")
        else:
            cache_status[cache_status_key].append("cache_file_exists")
            with open(filepath, 'rb') as f:
                cache_time, result = pickle.load(f)
                time_since_cache = time.time() - cache_time
                if config.ignore_cache_expiration \
                or time_since_cache < config.cache_expiration:
                    cache_status[cache_status_key].append("cache_loaded")
                    return result, last_saved_cache_file, cache_status
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
                    cache_status[cache_status_key].append(f"cache_expired: {time_since_cache_formatted} passed")
    
    # call the function - this will happen if the cache_expiration is not set or the cache file doesn't exist or is expired
    result = execute_func(func, instance, *args, **kwargs)
    cache_status[cache_status_key].append("method_called")

    # If cache is enabled for the model (or cache is forced to expire), save the result to the cache
    if config.cache_expiration is not None or config.force_cache_expiration:
        with open(filepath, 'wb') as f:
            pickle.dump((time.time(), result), f)
            cache_status[cache_status_key].append("cache_saved")
        last_saved_cache_file = filepath
    
    return result, last_saved_cache_file, cache_status

def execute_func(func, instance, *args, **kwargs):
    if instance is not None:
        return func(instance, *args, **kwargs)
    else:
        return func(*args, **kwargs)

def delete_last_saved_cache_file(func):
    """
decorator to delete the cache file created by the cache_to_disk decorator
This is used when the response is invalid or the data is not usable,
in order to prevent the cache from being used in the next request

Usage:
from useful_tools.cache_decorators import cache_to_disk, delete_last_saved_cache_file
class MyClass:
    cache_enabled = True
    cache_dir = "cache"
    cache_expiration = 2 # seconds
    force_cache_expiration = False
    ignore_cache_expiration = False

    @cache_to_disk
    def my_method(self):
        return "my_method"
    
    @delete_last_saved_cache_file
    def delete_cache(self):
        pass # the deletion is done in the wrapper

myclass = MyClass()
print(myclass.my_method()) # prints "my_method"
print(myclass.cache_status) # gives info about the use of cache in the previous call
# determine if the response is valid
# let's pretend the response is invalid, and delete the cache file
myclass.delete_cache()
print(myclass.my_method()) # prints "my_method"
print(myclass.cache_status) # gives info about the use of cache in the previous call
print("You can see from the cache status that the cache file was deleted.")
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "last_saved_cache_file"):
            if os.path.exists(self.last_saved_cache_file):
                os.remove(self.last_saved_cache_file)
                return self.last_saved_cache_file
        return None
    return wrapper
