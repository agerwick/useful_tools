from functools import wraps
from useful_tools.hash_functions import make_arg_hash


# decorators to cache the result of a function to memory
# this is used in order to avoid sending the same request multiple times
# cache_property works only for properties, while cache_to_memory works for any method

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
