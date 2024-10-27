import unittest
from useful_tools.dict_tools import get_dict_slice

class TestGetDictSlice(unittest.TestCase):
    def test_get_dict_slice_single_item(self):
        self.assertEqual(get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 1), {'b': 2})
    def test_get_dict_slice_first_item(self):
        self.assertEqual(get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 0), {'a': 1})
    def test_get_dict_slice_last_item(self):
        self.assertEqual(get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 2), {'c': 3})
    def test_get_dict_slice_multiple_items(self):
        self.assertEqual(get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 1, 2), {'b': 2, 'c': 3})
    def test_get_dict_slice_empty_dict(self):
        self.assertEqual(get_dict_slice({}, 0), {})
    def test_get_dict_slice_single_item_dict(self):
        self.assertEqual(get_dict_slice({'a': 1}, 0), {'a': 1})

class TestGetDictSliceErrors(unittest.TestCase):
    def test_get_dict_slice_out_of_range(self):
        with self.assertRaises(IndexError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 3)
    def test_get_dict_slice_out_of_range_end_position(self):
        with self.assertRaises(IndexError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 0, 3)
    def test_get_dict_slice_negative_position(self):
        with self.assertRaises(IndexError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, -1)
    def test_get_dict_slice_negative_end_position(self):
        with self.assertRaises(IndexError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 0, -1)
    def test_get_dict_slice_not_dict(self):
        with self.assertRaises(TypeError):
            get_dict_slice('a', 0)
    def test_get_dict_slice_position_not_int(self):
        with self.assertRaises(TypeError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 'a')
    def test_get_dict_slice_end_position_not_int(self):
        with self.assertRaises(TypeError):
            get_dict_slice({'a': 1, 'b': 2, 'c': 3}, 0, 'a')
