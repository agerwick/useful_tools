# Useful Tools

`useful_tools` is a Python module that provides a collection of useful decorators and other tools, including `act_as_list`, `cache_to_memory` and `cache_to_disk`.

## Installation

You can install Useful Tools directly from GitHub using pip:

```bash
pip install git+https://github.com/agerwick/useful_tools.git
```

## acts_as_list decorator

Here's how you can use the act_as_list decorator:

```python
from useful_tools import act_as_list

# 'objects' refers to the propery on the class which is used as a list.
# In this case it's an attribute called 'objects', but it could be any list.
@act_as_list('objects') 
class MyClassThatLooksLikeAList:
    def __init__(self, objects = []):
        self.objects = objects
    def contains_both_hello_and_world(self):
        return "hello" in self and "world" in self

myclass = MyClassThatLooksLikeAList()
myclass.append("hello")
myclass.append("world")
print(myclass.objects)  # prints ['hello', 'world']
print(myclass)  # prints ['hello', 'world']
print(myclass[0])  # prints 'hello'
print(myclass.index("world"))  # prints 1
print(len(myclass))  # prints 2
print(list(reversed(myclass)))  # prints ['world', 'hello']
print(fake_list.contains_both_hello_and_world()) # prints True
print(myclass.pop())  # prints 'world'
print(fake_list.contains_both_hello_and_world()) # prints False
```

In this code, MyClassThatLooksLikeAList behaves like a list, with the list-like behavior based on the `objects` attribute.
But, unlike a list, you can define your own methods and properties on this class.

## Cache Decorators

The `cache_decorators.py` module provides decorators to cache the result of a function or property. This is useful to avoid sending the same request multiple times.

### cache_to_memory
The `cache_to_memory` decorator caches the result of a method to memory. Here's an example of how to use it:

```python
from useful_tools import cache_to_memory

@cache_to_memory
def my_method(self):
    return "my_method"
```

In this code, the result of `my_method` is cached the first time it's called. Subsequent calls with the same arguments will return the cached result.

If you want to use cache_to_memory with a property, you should define the property decorator before the cache_to_memory decorator, like this:

```python
from useful_tools import cache_to_memory

@property
@cache_to_memory
def my_property(self):
    return "my_property"
```

In this code, the result of `my_property` is cached the first time it's accessed. Subsequent accesses will return the cached result.

### cache_to_disk

The `cache_to_disk` decorator caches the result of a method to disk. It uses pickle to save the result to disk. This decorator can only be used in classes that have the following attributes:

- `cache_enabled`: True or False
- `cache_dir`: path to the cache directory
- `cache_expiration`: number of seconds to keep the cache file
- `force_cache_expiration`: True or False
- `ignore_cache_expiration`: True or False

If used in conjunction with `@property`, the property decorator must be defined before the `cache_to_disk` decorator, like this:

```python
from useful_tools import cache_to_disk

class MyClass:
    cache_enabled = True
    cache_dir = "cache"
    cache_expiration = 30  # seconds - can be a float or int
    cache_status = {}
    force_cache_expiration = False
    ignore_cache_expiration = False
    
    def __init__(self):
        self.number_of_calls = 0
    
    @property
    @cache_to_disk
    def my_property(self):
        self.number_of_calls += 1
        return f"my_property has been called {self.number_of_calls} times."
```

In this code, the result of `my_property` is cached to disk the first time it's accessed. Subsequent accesses will return the cached result, unless the cache has expired.

You can test it like this:
```python
obj = MyClass()
obj.my_property
# returns 'my_property has been called 1 times.'
obj.my_property
# returns 'my_property has been called 1 times.'
# now wait 30 seconds
obj.my_property
# returns 'my_property has been called 2 times.'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Run tests and generate coverage report

```
coverage run -m pytest ; coverage xml
```

## Author

Ronny Ager-Wick

## License

[MIT](https://choosealicense.com/licenses/mit/)