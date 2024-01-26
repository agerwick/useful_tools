import os
import time
import pickle
from functools import wraps

# decorators to cache the result of a function
# this is used in order to avoid sending the same request multiple times
# cache_property works only for properties, while cache_result works for any function

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
@property
@cache_to_memory
def my_property(self):
    return "my_property"
    """
    if isinstance(func, property):
        raise TypeError(f"Cannot cache a property. Apply @property above @cache_to_memory, not below.")
    
    cache = {}
    @wraps(func)
    def wrapper(*args):
        attr_name = func.__name__
        if attr_name not in cache:
            cache[attr_name] = {}
        if args not in cache[attr_name]:
            cache[attr_name][args] = func(*args)
        return cache[attr_name][args]
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

from cache_decorators import cache_to_disk
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
        # give a useful error message if the class doesn't have the required attributes
        required_attributes = ["cache_enabled", "cache_dir", "cache_expiration", "force_cache_expiration", "ignore_cache_expiration"]
        for attr in required_attributes:
            if not hasattr(self, attr):
                raise AttributeError(f"{self.__class__.__name__} does not have the attribute '{attr}', required by the @cache_to_disk decorator.")

        # make a hash of the arguments
        arg_hash = f"{hash(args)}_{hash(frozenset(kwargs.items()))}"

        # create a dictionary to store the cache status for each function
        if not hasattr(self, "cache_status"):
            self.cache_status = {}
        cache_status_key = f"{self.__class__.__name__}.{func.__name__}_{arg_hash}"
        self.cache_status[cache_status_key] = []

        # If cache is disabled, call the function and return the result
        # when mocking requests, the cache is disabled
        # this is done in handle_request() in main.py
        if not self.cache_enabled:
            self.cache_status[cache_status_key].append("cache_disabled")
            self.cache_status[cache_status_key].append("method_called")
            return func(self, *args, **kwargs)
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # Create a unique filename based on the class name, method name and arguments
        filename = f"{cache_status_key}.pkl"
        filepath = os.path.join(self.cache_dir, filename)

        read_from_cache = False
        if self.ignore_cache_expiration:
            if self.force_cache_expiration:
                self.cache_status[cache_status_key].append("ignore_cache_expiration and force_cache_expiration are both True - force_cache_expiration takes precedence")
            else:
                self.cache_status[cache_status_key].append("cache_expiration_ignored")
                read_from_cache = True

        if self.force_cache_expiration:
            self.cache_status[cache_status_key].append("cache_expiration_forced")
            read_from_cache = False
        else:
            if self.cache_expiration is not None:
                self.cache_status[cache_status_key].append(f"cache_expiration_set: {self.cache_expiration}s")
                read_from_cache = True
            else:
                self.cache_status[cache_status_key].append("cache_expiration_not_set")
                read_from_cache = False
            
        if read_from_cache:
            if not os.path.exists(filepath):
                self.cache_status[cache_status_key].append("cache_file_does_not_exist")
            else:
                self.cache_status[cache_status_key].append("cache_file_exists")
                with open(filepath, 'rb') as f:
                    cache_time, result = pickle.load(f)
                    time_since_cache = time.time() - cache_time
                    if self.ignore_cache_expiration \
                    or time_since_cache < self.cache_expiration:
                        self.cache_status[cache_status_key].append("cache_loaded")
                        return result
                    else:
                        if time_since_cache < 10:
                            time_since_cache_formatted = f"{time_since_cache:.3f}s"
                        elif time_since_cache < 60:
                            time_since_cache_formatted = f"{time_since_cache:.1f}s"
                        elif time_since_cache < 3600:
                            time_since_cache_formatted = f"{time_since_cache/60:.1f}m"
                        else:
                            time_since_cache_formatted = f"{time_since_cache/3600:.1f}h"
                        self.cache_status[cache_status_key].append(f"cache_expired: {time_since_cache_formatted} passed")
        
        # call the function - this will happen if the cache_expiration is not set or the cache file doesn't exist or is expired
        result = func(self, *args, **kwargs)
        self.cache_status[cache_status_key].append("method_called")

        # If cache is enabled for the model (or cache is forced to expire), save the result to the cache
        if self.cache_expiration is not None or self.force_cache_expiration:
            with open(filepath, 'wb') as f:
                pickle.dump((time.time(), result), f)
                self.cache_status[cache_status_key].append("cache_saved")
        return result
    return wrapper
