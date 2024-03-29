import dataclasses
from operator import attrgetter

class ModifiedDataclassTypeError(TypeError):
    pass

def modified_dataclass(replace_repr_with_attr={}, simplify_repr=[], exclude_from_repr=[], exclude_defaults_from_repr=False):
    """
    A decorator that modifies the string representation (__repr__) of a dataclass object.

    Args:
        replace_repr_with_attr (dict): A dictionary of attribute names and their replacements in the string representation.
            The key is the attribute of the decorated class (typically a complex object)
            The value is an attribute *of this object* that will be used in the string representation instead of the original attribute.
            Usage: If the decorated class has an attribute 'session' that is an instance of a complex object, and the string representation of this object is not useful, you can replace it with an attribute of the session object that is useful (or at least, shorter).
            Example: replace_repr_with_attr = {'session': 'session_id'} # this will use session.session_id in the string representation instead of session.__repr__
        simplify_repr (list): A list of attribute names to simplify in the string representation. By simplification I mean that the attribute will be replaced with a string repreensentation of its type.
        exclude_from_repr (list): A list of attribute names to exclude from the string representation.
        exclude_defaults_from_repr (bool): A flag indicating whether to exclude attributes with default values from the string representation.

    Returns:
        class: The modified dataclass.

    """
    def decorator(cls):
        """
        Decorator function to enhance the __repr__ method of a dataclass.

        Args:
            cls: The class to decorate.

        Returns:
            cls: The decorated class.

        """
        # check the types of the attributes
        if not isinstance(replace_repr_with_attr, dict):
            raise ModifiedDataclassTypeError(f"replace_repr_with_attr must be a dictionary, not {replace_repr_with_attr.__class__.__name__}")
        if not isinstance(simplify_repr, list):
            raise ModifiedDataclassTypeError(f"simplify_repr must be a list, not {simplify_repr.__class__.__name__}")
        if not isinstance(exclude_from_repr, list):
            raise ModifiedDataclassTypeError(f"exclude_from_repr must be a list, not {exclude_from_repr.__class__.__name__}")
        if not isinstance(exclude_defaults_from_repr, bool):
            raise ModifiedDataclassTypeError(f"exclude_defaults_from_repr must be a boolean, not {exclude_defaults_from_repr.__class__.__name__}")
        
        if not all(isinstance(attr, str) for attr in replace_repr_with_attr.keys()):
            raise ModifiedDataclassTypeError(f"All keys in replace_repr_with_attr must be strings. They represent the attributes of the class {cls.__class__.__name__} which value should be replaces.")
        if not all(isinstance(attr, str) for attr in replace_repr_with_attr.values()):
            raise ModifiedDataclassTypeError(f"All values in replace_repr_with_attr must be strings. They represent the attributes of the class {cls.__class__.__name__} which value should be used in the string representation instead of the original attribute.")
        if not all(isinstance(attr, str) for attr in simplify_repr):
            raise ModifiedDataclassTypeError(f"All elements in simplify_repr must be strings. They represent the attributes of the class {cls.__class__.__name__} which value should be simplified.")
        if not all(isinstance(attr, str) for attr in exclude_from_repr):
            raise ModifiedDataclassTypeError(f"All elements in exclude_from_repr must be strings. They represent the attributes of the class {cls.__class__.__name__} which value should be excluded from the string representation.")

        cls = dataclasses.dataclass(cls, repr=False)

        def new_repr(self):
            """
            Generate a string representation of the object, excluding certain attributes and simplifying others.

            Args:
                self: The object instance.

            Returns:
                str: The string representation of the object.

            """
            if exclude_defaults_from_repr:
                # get all non-default attributes
                attr_vals = (
                    (f.name, attrgetter(f.name)(self))
                    for f in dataclasses.fields(self)
                    if attrgetter(f.name)(self) != f.default
                )
            else:
                # get all attributes
                attr_vals = (
                    (f.name, attrgetter(f.name)(self))
                    for f in dataclasses.fields(self)
                )
            
            # modify the attributes in simplify to return just the type, not the entire value, as this drowns out the rest of the information
            attr_vals = [
                (name, type(value) if name in simplify_repr else value)
                for name, value in attr_vals
            ]

            # replace attributes in replace_repr_with_attr with the specified attribute
            attr_keys = [k for k,_ in attr_vals]
            for orig_attr, new_attr in replace_repr_with_attr.items():
                if orig_attr in attr_keys:
                    # make an object from the string passed as param, which should be defined on self.
                    try:
                        orig_attr_obj = getattr(self, orig_attr)
                    except AttributeError:
                        raise AttributeError(f"Attribute '{orig_attr}' does not exist on the {self.__class__.__name__} object. It is defined as a 'replace_repr_with_attr' argument to the modified_dataclass decorator on {self.__class__.__name__}.")
                    # get the attribute from the object
                    try:
                        new_attr_repr = getattr(orig_attr_obj, new_attr)
                    except AttributeError:
                        raise AttributeError(f"Attribute '{new_attr}' does not exist on the {orig_attr} object. It is defined as a 'replace_repr_with_attr' argument to the modified_dataclass decorator on {self.__class__.__name__}.")
                    attr_vals = [(name, new_attr_repr) if name == orig_attr else (name, attr) for name, attr in attr_vals]

            # remove attributes that are in the exclude list
            attr_vals = [val for val in attr_vals if val[0] not in exclude_from_repr]
            
            # create a string representation of the non-default attributes
            new_repr = ", ".join(f"{name}={value}" for name, value in attr_vals)
            return f"{self.__class__.__name__}({new_repr})"

        cls.__repr__ = new_repr

        return cls
    return decorator

"""
Usage:
@modified_dataclass(simplify_repr=['session'], exclude_from_repr=['other_field'], exclude_defaults_from_repr=True)
class Test:
    session: 'Session'
    other_field: int
    field_with_default: str = "default_value"
    important_field: str

t = Test(session="session", other_field=1, important_field="important")
print(t)
# Test(session=<class 'str'>, important_field=important)
# - session is replaced by its type
# - other_field is excluded
# - field_with_default is excluded because it has a default value
"""