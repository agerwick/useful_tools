class PropertyFactory:
    """
    A descriptor class that creates properties dynamically.

    Args:
        getter (callable): The getter function for the property.

    Attributes:
        getter (callable): The getter function for the property.

    Methods:
        __get__(self, instance, owner): Retrieves the value of the property.

    Usage:
        To create a property using the PropertyFactory, pass a getter function to the constructor.
        The getter function should take an instance as an argument and return the value of the property.
    """

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.getter(instance)

"""
Usage:
from property_factory import PropertyFactory
if you're trying to dynamically add a property to the decorated instance from within a decorator, you can use this PropertyFactory class to create a property that is dynamically generated at runtime.
This method adds the property to an instance that is based on the instance's state at the time the property is added, rather than at the time the class is defined.
The drawback is it is not available until the decorator is called.
Example:
Lets say you have a decorator that adds a property to an instance based on some_dictionary:
Add this within the wrapper function of the decorator:
type(self).my_property = PropertyFactory(lambda self: self.some_dictionary.get("my_property"))
This will add a property to the instance that will return the value of some_dictionary["my_property"] when accessed.
Example:
class MyClass:
    @my_decorator
    def my_decorated_method(self):
        self.some_dictionary = {"my_property": "Hello World"}

def my_decorator(func):
    def wrapper(self, *args, **kwargs):
        type(self).my_property = PropertyFactory(lambda self: self.some_dictionary.get("my_property"))
        return func(self, *args, **kwargs)
    return wrapper
    
my_instance = MyClass()
my_instance.my_decorated_method()
print(my_instance.my_property)
This will print "Hello World" when my_decorated_method is called.
"""