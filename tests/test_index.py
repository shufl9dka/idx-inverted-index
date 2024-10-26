import unittest
import os
from pyroaring import BitMap
from libs.index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.filepath = "./test_index.pkl"
        self.index = InvertedIndex(self.filepath)

    def tearDown(self) -> None:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_add_and_const_get(self):
        self.index.add("aba", 1)
        self.index.add("caba", 2)
        self.index.add("aba", 3)

        result = self.index.const_get("aba")
        self.assertEqual(result, BitMap({1, 3}))

        result = self.index.const_get("caba")
        self.assertEqual(result, BitMap({2}))

    def test_save_and_load(self):
        self.index.add("test", 42)
        self.index.save()

        other_index = InvertedIndex(self.filepath)
        result = other_index.const_get("test")
        self.assertEqual(result, BitMap({42}))

    def test_const_get_default(self):
        result = self.index.const_get("nonexistent", BitMap())
        self.assertEqual(result, BitMap())


if __name__ == "__main__":
    unittest.main()
