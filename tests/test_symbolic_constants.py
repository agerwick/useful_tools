import unittest
from typing import Literal, TypeAlias, TypedDict
from useful_tools import SymbolicConstantsDict, create_symbolic_constants_from_typealias

PipelineStageLiteral: TypeAlias = Literal[
    "upload",
    "pre-processing",
    "processing",
    "post-processing"
]
class _PipelineStage(TypedDict):
    UPLOAD: str
    PRE_PROCESSING: str
    PROCESSING: str
    POST_PROCESSING: str
PipelineStage: _PipelineStage = create_symbolic_constants_from_typealias(PipelineStageLiteral)

class TestSymbolicConstantsDict(unittest.TestCase):
    def test_access_via_attributes(self):
        self.assertEqual(PipelineStage.UPLOAD, "upload")
    def test_access_via_keys(self):
        self.assertEqual(PipelineStage["UPLOAD"], "upload")
    def test_access_via_get(self):
        self.assertEqual(PipelineStage.get("UPLOAD"), "upload")
    def test_access_non_existent_attribute(self):
        with self.assertRaises(AttributeError):
            PipelineStage.BAZ
    def test_keys(self):
        self.assertEqual(list(PipelineStage.keys()), ["UPLOAD", "PRE_PROCESSING", "PROCESSING", "POST_PROCESSING"])
    def test_values(self):
        self.assertEqual(list(PipelineStage.values()), ["upload", "pre-processing", "processing", "post-processing"])
    def test_items(self):
        self.assertEqual(list(PipelineStage.items()), [("UPLOAD", "upload"), ("PRE_PROCESSING", "pre-processing"), ("PROCESSING", "processing"), ("POST_PROCESSING", "post-processing")])
    def test_modify_after_initialization(self):
        with self.assertRaises(TypeError):
            PipelineStage["BAZ"] = "baz"

class TestWeirdCharacters(unittest.TestCase):
    """
    Dashes, commas, dots, parenthesis and spaces in the literals will be converted to underscores
    We also translate the following characters:
    & to _AND_
    + to _PLUS_
    % to _PERCENT_
    / to _SLASH_
    >= to _GTE_ and <= to _LTE_
    <>=! to _LT_, _GT_, _EQ_, _NE_
    """
    def test_dashes(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo-bar"]).FOO_BAR, "foo-bar")
    def test_commas(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo,bar"]).FOO_BAR, "foo,bar")
    def test_dots(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo.bar"]).FOO_BAR, "foo.bar")
    def test_parenthesis(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo(bar)"]).FOO_BAR, "foo(bar)")
    def test_spaces(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo bar"]).FOO_BAR, "foo bar")
    def test_ampersand(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo&bar"]).FOO_AND_BAR, "foo&bar")
    def test_plus(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo+bar"]).FOO_PLUS_BAR, "foo+bar")
    def test_percent(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo%bar"]).FOO_PERCENT_BAR, "foo%bar")
    def test_slash(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo/bar"]).FOO_SLASH_BAR, "foo/bar")
    def test_gte(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo>=bar"]).FOO_GTE_BAR, "foo>=bar")
    def test_lte(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo<=bar"]).FOO_LTE_BAR, "foo<=bar")
    def test_lt(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo<bar"]).FOO_LT_BAR, "foo<bar")
    def test_gt(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo>bar"]).FOO_GT_BAR, "foo>bar")
    def test_eq(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo=bar"]).FOO_EQ_BAR, "foo=bar")
    def test_ne(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo!=bar"]).FOO_NE_BAR, "foo!=bar")
    def test_lt_and_lte(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo<bar<=baz"]).FOO_LT_BAR_LTE_BAZ, "foo<bar<=baz")
    def test_removal_of_leading_or_trailing_underscores(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["-foo-"]).FOO, "-foo-")
    def test_prepending_underscore_to_numbers(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["1foo"])._1FOO, "1foo")
    def test_spaces_around_special_characters(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo & bar"]).FOO_AND_BAR, "foo & bar")
    def test_no_spaces_around_special_characters(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo&bar"]).FOO_AND_BAR, "foo&bar")
    def test_multiple_special_characters_repeated(self):
        self.assertEqual(create_symbolic_constants_from_typealias(Literal["foo & bar _-.,(baz)"]).FOO_AND_BAR_BAZ, "foo & bar _-.,(baz)")
    # raise a ValueError if one of the literals contains a ' (single quote)
    def test_single_quote(self):
        with self.assertRaises(ValueError):
            create_symbolic_constants_from_typealias(Literal["foo'bar"])
    # raise a ValueError if we end up with two of the same literals
    def test_duplicate_literals(self):
        with self.assertRaises(ValueError):
            create_symbolic_constants_from_typealias(Literal["foo & bar", "foo&bar"]) # they will both resolve to FOO_AND_BAR
    # raise a ValueError if any of the literals are not valid Python identifiers
    def test_invalid_identifier(self):
        with self.assertRaises(ValueError):
            create_symbolic_constants_from_typealias(Literal["snafu!"])

if __name__ == '__main__':
    unittest.main()

