import os
import unittest

from libs.base import SearchBase
from libs.index import InvertedIndex

from pyroaring import BitMap


class TestSearchBase(unittest.TestCase):
    def setUp(self) -> None:
        self.index_filepath = "./test_index.pkl"
        self.docs_folder = "./test_docs"
        self.index = InvertedIndex(self.index_filepath)
        self.search_base = SearchBase(self.index, folder=self.docs_folder)

    def tearDown(self) -> None:
        if os.path.exists(self.index_filepath):
            os.remove(self.index_filepath)

        if os.path.exists(self.docs_folder):
            for file in os.listdir(self.docs_folder):
                file_path = os.path.join(self.docs_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.docs_folder)

    def test_preprocess_text(self):
        text = "This is a simple testcase, with punctuation!"
        processed = self.search_base.preprocess_text(text)
        self.assertEqual(processed, ["simpl", "testcas", "punctuat"])

    def test_add_and_get_doc(self):
        text = "abacaba"
        doc_id = self.search_base.add(text)

        retrieved_content = self.search_base.get_doc(doc_id)
        self.assertEqual(retrieved_content, text)

    def test_query(self):
        doc1 = "Document of fun"
        doc2 = "Document of pain"
        doc_id1 = self.search_base.add(doc1)
        doc_id2 = self.search_base.add(doc2)

        result = self.search_base.query("document")
        self.assertEqual(result, BitMap({doc_id1, doc_id2}))

        result = self.search_base.query("fun")
        self.assertEqual(result, BitMap({doc_id1}))
    
    def test_complex_query(self):
        docs = [
            "The first funny document",
            "The second funny document",
            "The first serious document",
            "The second serious document",
        ]
        doc_id = [self.search_base.add(doc) for doc in docs]
        first = self.search_base.query("first")
        serious = self.search_base.query("serious")
        first_serious = first & serious

        self.assertEqual(first, BitMap({doc_id[0], doc_id[2]}))
        self.assertEqual(serious, BitMap({doc_id[2], doc_id[3]}))
        self.assertEqual(first_serious, BitMap({doc_id[2]}))

    def test_get_doc_nonexistent(self):
        content = self.search_base.get_doc(999999)
        self.assertIsNone(content)


if __name__ == "__main__":
    unittest.main()
