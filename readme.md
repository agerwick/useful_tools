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

fake_list = MyClassThatLooksLikeAList()
fake_list.append("hello")
fake_list.append("world")
print(fake_list.objects)  # prints ['hello', 'world']
print(fake_list)  # prints ['hello', 'world']
print(fake_list[0])  # prints 'hello'
print(fake_list.index("world"))  # prints 1
print(len(fake_list))  # prints 2
print(list(reversed(fake_list)))  # prints ['world', 'hello']
print(fake_list.contains_both_hello_and_world()) # prints True
print(fake_list.pop())  # prints 'world'
print(fake_list.contains_both_hello_and_world()) # prints False
```

In this code, MyClassThatLooksLikeAList behaves like a list, with the list-like behavior based on the `objects` attribute.
But, unlike a list, you can define your own methods and properties on this class.

### Adding @act_as_list objects with other @act_as_list objects or lists

When adding another list or list_like object to an @act_as_list object, it will return a list object by default.
The reason for this is that the decorator is not aware of the required attributes for the constructor method of the decorated class.
If you add a _from_list() method to the decorated class, the list will be passed to this method and it will return the result of that instead.
This method can then call the constructor method (__init__) with the correct arguments for the decorated class.
Example:

```python
@act_as_list('actual_list')
class MyClassWithExtraAttrs:
    def __init__(self, actual_list = [], extra_attr = None):
        if extra_attr == None:
            raise Exception("extra_attr is required")
        else:
            self.extra_attr = extra_attr
        self.actual_list = actual_list
    def _from_list(self, actual_list):
        # construct a new MyClassWithExtraAttrs using the list and required attributes
        return MyClassWithExtraAttrs(actual_list, extra_attr=self.extra_attr)

fake_list = MyClassWithExtraAttrs(["hello", "world"], extra_attr="fubar")
result = fake_list + ["foo", "bar"]
print(result) # ["hello", "world", "foo", "bar"]
print(result.__class__) # MyClassWithExtraAttrs # because the class has a _from_list method, it returns the original class
# if the _from_list class was not defined, the resulting class would be a list
```

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

### delete_last_saved_cache_file

The `delete_last_saved_cache_file` decorator is used to create a method on your class 
that can be used to delete the cache file created by the cache_to_disk decorator.
This is used when the response is invalid or the data is not usable,
in order to prevent the cache from being used in the next request

Usage:

```python
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
```

## modified_dataclass

A decorator that adds some extra features to @dataclass
example:

```python
@modified_dataclass(simplify_repr=['session'], exclude_from_repr=['other_field'], exclude_defaults_from_repr=True)
class Test:
    session: 'Session'
    other_field: int
    field_with_default: str = "default_value"
    important_field: str

t = Test(session="session", other_field=1, important_field="important")
print(t)
# Test(session=<class 'str'>, important_field=important)
```

Compared with the default repr:

- session is replaced by its type
- other_field is excluded
- field_with_default is excluded because it has a default value

## exit if already running

Function to check if the script is already running by checking the PID in the pid file.
If the script is already running, it will exit the script.

```python
from useful_tools import exit_if_already_running
# set pid file name to the name of this script with .pid extension
pid_file = os.path.basename(__file__).replace(".py", ".pid")
exit_if_already_running(pid_file)

# do stuff here

os.remove(pid_file) # Delete the PID file
```

Even if the script exists before the PID file is deleted, the function will still work, as it checks if the PID exists.

## redirect_stdout

Context manager to redirect the output of a function call.
Typically used when you call a function that outputs to the terminal and you want to avoid outputting to the terminal because it will make the logfile cluttered.

### Usage

```python
with redirect_stdout() as output:
    print("This is printed to the console")

# Now you can ignore the output if you want
# or you can get the output of the function call as a string
output_string = output.getvalue()
print("Output:", output_string)
```

## ip address functions

```python
is_public_ip_address('192.0.2.256') # returns False, as this is an invalid IP address (each section can only be 0-255)
is_public_ip_address('192.168.0.1') # returns False, as this is a reserved address (for internal use behind NAT)
is_public_ip_address('8.8.8.8') # returns True as this is a valid ip address that is addressable on the public net
is_reserved_ip_address('1.0.0.0') # returns False because it's not a reserved ip address
is_reserved_ip_address('10.0.0.1') # returns True because it's a reserved ip address
is_valid_ip_address('192.168.0.1') # returns True because it's a valid ip address (even if it's a reserved address)
is_valid_ip_address('192.168.0.256') # returns False because the last number is out of range
```

## generate test coverage report

This is a script that creates a test coverage report and, when run as a git pre-commit hook, can abort a commit if you accidentally try to commit to a restricted repo (typically main and test) or the test coverage is below a predetermined threshold.

### installation

Assumes:

- you have git installed and initialized in your project
- you have a virtual environment set up in .env/
- you are in the root folder of your project

```bash
pip install git+https://github.com/agerwick/useful_tools.git
source .venv/Lib/site-packages/useful_tools/generate_test_coverage_report_files/install.sh
```

Edit run_test_coverage_report.py to set the minimum_test_coverage_percentage, etc.
Edit .coveragerc to exclude irrelevant subdirectories (such as tests/) from the coverage report.

NOTE: run_test_coverage_report.py, .coveragerc and the .githooks folder should all be committed to the repository

Add these two lines of "must-do" instruction to your readme, so that other developers know how to set up the pre-commit hook:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### usage

- when committing, the pre-commit hook will run the test coverage report
- if the branch is restricted, the commit will be aborted - you will need to use pull requests instead
- if the branch is in branches_with_enforced_test_coverage, and the test coverage is below the threshold, the commit will be aborted
- otherwise the commit will proceed
- regardless of the outcome, the test coverage report will saved in `coverage_stats.txt`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

### Setting up a development environment

After cloning this repo, run:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

## Run tests and generate coverage report

This is done automatically on commit, assuming the development environment has been set up after pulling the repo (see the paragraph above).

Or you can run it manually like this:

```bash
python run_test_coverage_report
```

## Author

Ronny Ager-Wick

## License

[MIT](https://choosealicense.com/licenses/mit/)