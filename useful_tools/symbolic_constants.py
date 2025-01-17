"""
Usage:
from typing import Literal, TypeAlias
from useful_tools import SymbolicConstantsDict, create_symbolic_constants_from_typealias

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
    _initializing = True # set this to True to allow setting new values during initialization
    def __init__(self, *args, **kwargs):
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
        super().__setattr__(key, value)

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
    All literals will be converted to uppercase.
    Dashes, commas, dots, parenthesis and spaces in the literals will be converted to underscores, as these won't work as attribute names.
    We also translate the following characters:
    & to _AND_
    + to _PLUS_
    % to _PERCENT_
    / to _SLASH_
    >= to _GTE_ and <= to _LTE_
    <>=! to _LT_, _GT_, _EQ_, _NE_

    If the resulting attribute name ends up with more than one repeated underscore, it will be converted to a single underscore.
    Any literals that are still not valid Python identifiers will raise a ValueError.
    Any combination that results in two of the same literals will raise a ValueError.

    Parameters:
    literal (TypeAlias): A Literal TypeAlias object.

    Returns:
    SymbolicConstantsDict: A SymbolicConstantsDict object.

    Raises:
    ValueError: If any of the literals are not valid Python identifiers.

    Example:
    ```
    TestSymbolicConstantLiteral: TypeAlias = Literal[
        "test-this-thing",
        "95% done",
        "this & that",
        "a, b, c",
        "d.e.f",
        "voltage (mv)",
        "right/wrong",
        "10>9<11",
        "1=1!=2",
        "5>=4<=6",
    ]
    TestSymbolicConstant = create_symbolic_constants_from_typealias(TestSymbolicConstantLiteral)
    print(TestSymbolicConstant.TEST_THIS_THING)  # prints "test-this-thing"
    print(TestSymbolicConstant.THIS_AND_THAT)  # prints "this & that"
    print(TestSymbolicConstant._95_PERCENT_DONE)  # prints "95% done"
    print(TestSymbolicConstant.A_B_C)  # prints "a, b, c"
    print(TestSymbolicConstant.D_E_F)  # prints "d.e.f"
    print(TestSymbolicConstant.VOLTAGE_MV)  # prints "voltage (mv)"
    print(TestSymbolicConstant.RIGHT_SLASH_WRONG)  # prints "right/wrong"
    print(TestSymbolicConstant._10_LT_9_GT_11)  # prints "10>9<11"
    print(TestSymbolicConstant._1_EQ_1_NE_2)  # prints "1=1!=2"
    print(TestSymbolicConstant._5_GTE_4_LTE_6)  # prints "5>=4<=6"

    # you can also access the literals the same way you would access a dictionary, for example using the [] operator or .get() method
    # you can not, however, add or modify values, as this will raise a TypeError
    """
    # parse the string and return the literals as a list
    _str = str(literal) # convert the TypeAlias to a string, a bit hackish, but it does the trick

    # make sure there are no " in the string, as this will mess up the parsing. If there are, this is caused by one of the literals containing a ', so we'll raise a ValueError
    if '"' in _str:
        raise ValueError("Literals can not contain the ' (single quote) character. Major rework must be done to handle this case")

    # remove everything before the first [ and everything after the last ], including the brackets themselves
    _str = _str[_str.find("[")+1:_str.rfind("]")]

    # split the string into a list of literals
    _split_str = _str.split(", ")
    # example: ["'this & that'", "'95% done'", "'a, b, c'", "'d.e.f'", "'voltage (mv)'", "'right/wrong'", "'10>9<11'", "'1=1!=2'", "'5>=4<=6'"]

    # strip the ' from the literals
    _orig_literals_list = [literal.strip("'") for literal in _split_str]
    # example: ['this & that', '95% done', 'a, b, c', 'd.e.f', 'voltage (mv)', 'right/wrong', '10>9<11', '1=1!=2', '5>=4<=6']

    # convert to uppercase
    _literals_list = [literal.upper() for literal in _orig_literals_list]
    # example: ['THIS & THAT', '95% DONE', 'A, B, C', 'D.E.F', 'VOLTAGE (MV)', 'RIGHT/WRONG', '10>9<11', '1=1!=2', '5>=4<=6']

    # convert dashes, periods/dots/points, commas, parenthesis and spaces to underscores, as these won't work as attribute names, and convert to uppercase
    _literals_list = [literal.replace("-", "_").replace(",", "_").replace(".", "_").replace("(", "_").replace(")", "_").replace(" ", "_") for literal in _literals_list]
    # example: ['THIS_&_THAT', '95%_DONE', 'A__B__C', 'D_E_F', 'VOLTAGE__MV', 'RIGHT/WRONG', '10>9<11', '1=1!=2', '5>=4<=6']

    # convert & to AND
    _literals_list = [literal.replace("&", "_AND_") for literal in _literals_list]

    # convert + to PLUS
    _literals_list = [literal.replace("+", "_PLUS_") for literal in _literals_list]

    # convert % to PERCENT
    _literals_list = [literal.replace("%", "_PERCENT_") for literal in _literals_list]

    # convert / to SLASH
    _literals_list = [literal.replace("/", "_SLASH_") for literal in _literals_list]

    # convert >= to GTE / <= to LTE / != to NE -- NOTE: double char conversion must precede single chars
    _literals_list = [literal.replace(">=", "_GTE_").replace("<=", "_LTE_").replace("!=", "_NE_") for literal in _literals_list]

    # convert <>=! to LT, GT, EQ, NE
    _literals_list = [literal.replace("<", "_LT_").replace(">", "_GT_").replace("=", "_EQ_") for literal in _literals_list]

    # remove any leading and trailing underscores
    _literals_list = [literal.strip("_") for literal in _literals_list]

    # if the first character is a digit, prepend an underscore
    _literals_list = [f"_{literal}" if literal[0].isdigit() else literal for literal in _literals_list]

    # convert any number of repeated underscores to a single underscore
    while "__" in str(_literals_list): # I know, it's a bit hackish to convert the list to a string in order to search for dunders, but it works!
        _literals_list = [literal.replace("__", "_") for literal in _literals_list]

    # raise a ValueError if we end up with two of the same literals
    if len(_literals_list) != len(set(_literals_list)):
        # find the first repeated literal
        _repeated_literal = next(literal for literal in _literals_list if _literals_list.count(literal) > 1)
        raise ValueError(f"Duplicate Symbolic Constant '{_repeated_literal}' -- multiple literals can not result in the same attribute name")

    # raise a ValueError if any of the literals are not valid Python identifiers
    for _literal in _literals_list:
        if not _literal.isidentifier():
            raise ValueError(f"Invalid literal '{_literal}', must be a valid Python identifier")
    # create a dictionary of the literals with _literals_list as the key and the original _literal_list as the value
    _literals_dict = {key: value for key, value in zip(_literals_list, _orig_literals_list)}
    # example: {'UPLOAD': 'upload', 'PRE_PROCESSING': 'pre-processing', 'PROCESSING': 'processing', 'POST_PROCESSING': 'post-processing'}

    # return a SymbolicConstantsDict object
    symbolic_constants: SymbolicConstantsDict = SymbolicConstantsDict(_literals_dict)
    return symbolic_constants
