import unittest
from typing import Literal, TypeAlias
from useful_tools import SymbolicConstantsDict, create_symbolic_constants_from_typealias

PipelineStageLiteral: TypeAlias = Literal[
    "upload",
    "pre-processing",
    "processing",
    "post-processing"
]
PipelineStage: SymbolicConstantsDict = create_symbolic_constants_from_typealias(PipelineStageLiteral)

class TestSymbolicConstantsDics(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()

