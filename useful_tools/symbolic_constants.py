"""
Usage:
from symbolic_constants import create_symbolic_constants_from_typealias, SymbolicConstantsDict
PipelineStageLiteral: TypeAlias = Literal[
    "upload",
    "pre-processing",
    "processing",
    "post-processing"
]
PipelineStage: SymbolicConstantsDict = create_symbolic_constants_from_typealias(PipelineStageLiteral)
"""

from typing import TypeAlias
from collections import UserDict

class SymbolicConstantsDict(UserDict):
    """
    A dictionary-like object that can be accessed with attribute notation.
    It's an actual constant - modification of the object after initialization will raise a TypeError.
    
    Example:
    ```
    my_constants = SymbolicConstantsDict({"FOO": "foo", "BAR": "bar"})
    print(my_constants.FOO)       # prints "foo"
    print(my_constants["BAR"])    # prints "bar"
    print(my_constants.get("BAR") # prints "bar"
    print(my_constants.BAZ)       # raises AttributeError
    print(my_constants.keys())    # prints dict_keys(["FOO", "BAR"])
    print(my_constants.values())  # prints dict_values(["foo", "bar"])
    print(my_constants.items())   # prints dict_items([("FOO", "foo"), ("BAR", "bar")])
    ```
    """
    def __init__(self, *args, **kwargs):
        self._initializing = True # set this to True to allow setting new values during initialization
        super().__init__(*args, **kwargs)
        self._initializing = False

    def keys(self):
        # return a proper list of the keys, just like a normal dictionary
        return self.data.keys()

    def values(self):
        # return a proper list of the values, just like a normal dictionary
        return self.data.values()

    def items(self):
        # return a proper list of the items, just like a normal dictionary
        return self.data.items()

    def _raise_exception(self):
        raise TypeError(f"Cannot modify SymbolicConstantsDict after initialization")

    # allow accessing values using the . operator
    def __getattr__(self, name):
        # only override the __getattr__ method if we are not initializing the object
        # otherwise we'll go into an infinite loop
        if not self._initializing:
            if name not in self.data: # the attribute is not in the dictionary
                if {self.__class__.__name__} == "SymbolicConstantsDict":
                    raise AttributeError(f"'SymbolicConstantsDict object has no attribute '{name}'")
                else: # the class is a subclass of SymbolicConstantsDict
                    raise AttributeError(f"'{self.__class__.__name__}' object (subclass of SymbolicConstantsDict) has no attribute '{name}'")
            return self.data[name]
        return super().__getattr__(name)

    # disable setting new values using the [] operator
    def __setitem__(self, key, value):
        if not self._initializing:
            self._raise_exception()
        super().__setitem__(key, value)

    # disable setting new values using the . operator
    def __setattr__(self, key, value):
        if not self._initializing:
            self._raise_exception()

    # disable updating values using the update method
    def update(self, *args, **kwargs):
        if not self._initializing:
            self._raise_exception()
        super().update(*args, **kwargs)

    # disable deleting values using the del operator
    def __delitem__(self, key):
        self._raise_exception()

    # disable deleting values using the del operator
    def __delattr__(self, name):
        self._raise_exception()

    # disable setting new values using the setdefault method
    def setdefault(self, *args, **kwargs):
        self._raise_exception()

    # disable setting new values using the pop method
    def pop(self, *args, **kwargs):
        self._raise_exception()

    # disable setting new values using the popitem method
    def popitem(self, *args, **kwargs):
        self._raise_exception()

    # disable clearing the dictionary
    def clear(self):
        self._raise_exception()

    # disable copying the dictionary
    def copy(self):
        self._raise_exception()

    # disable setting new values using the fromkeys method
    def fromkeys(self, *args, **kwargs):
        self._raise_exception()


def create_symbolic_constants_from_typealias(literal: TypeAlias) -> SymbolicConstantsDict:
    """
    Create a SymbolicConstantsDict object from a Literal TypeAlias.
    A SymbolicConstantsDict object is a dictionary-like object that can be accessed with attribute notation or like a dictionary, but cannot be modified.
    Dashes and spaces in the literals will be converted to underscores, as these won't work as attribute names.
    All literals will be converted to uppercase.
    Any literals that are still not valid Python identifiers will raise a ValueError.

    Parameters:
    literal (TypeAlias): A Literal TypeAlias object.

    Returns:
    SymbolicConstantsDict: A SymbolicConstantsDict object.

    Raises:
    ValueError: If any of the literals are not valid Python identifiers.

    Example:
    ```
    PipelineStageLiteral: TypeAlias = Literal[
        "upload",
        "pre-processing",
        "processing",
        "post-processing"
    ]
    PipelineStage = create_symbolic_constants_from_typealias(PipelineStageLiteral)
    print(PipelineStage.UPLOAD)  # prints "upload"
    print(PipelineStage.PRE_PROCESSING)  # prints "pre-processing"
    # you can also access the literals the same way you would access a dictionary, for example using the [] operator or .get() method
    # you can not, however, add or modify values, as this will raise a TypeError
    """
    # parse the string and return the literals as a list
    _str = str(literal)
    # remove everything before the first [ and everything after the last ], including the brackets themselves
    _str = _str[_str.find("[")+1:_str.rfind("]")]
    # split the string into a list of literals
    _literals = _str.split(", ")
    # strip the ' from the literals
    _literals = [literal.strip("'") for literal in _literals]
    # convert dashes and spaces to underscores, as these won't work as attribute names
    _literals = [literal.replace("-", "_").replace(" ", "_") for literal in _literals]
    # raise a ValueError if any of the literals are not valid Python identifiers
    for _literal in _literals:
        if not _literal.isidentifier():
            raise ValueError(f"Invalid literal '{_literal}', must be a valid Python identifier")
    # create a dictionary of the literals
    _literals_dict = {literal.upper(): literal for literal in _literals}
    # return a SymbolicConstantsDict object
    symbolic_constants: SymbolicConstantsDict = SymbolicConstantsDict(_literals_dict)
    return symbolic_constants
