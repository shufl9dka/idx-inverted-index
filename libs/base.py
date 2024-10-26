import os
import hashlib

from .index import InvertedIndex

import nltk
from nltk.corpus import stopwords
from nltk.stem.api import StemmerI
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from pyroaring import BitMap


nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")


class SearchBase:
    def __init__(self, index: InvertedIndex, folder: str = "."):
        os.makedirs(folder, exist_ok=True)
        self._folder = folder
        self._index = index

        self._stops: dict[str, set] = {}
        self._stemmer: dict[str, StemmerI] = {
            "english": PorterStemmer()
        }

    def preprocess_text(self, text, lang: str = "english") -> list[str]:
        if lang not in self._stops:
            self._stops[lang] = set(stopwords.words(lang))
        words = word_tokenize(text)
        stemmer = self._stemmer.get("english", PorterStemmer())
        return [
            stemmer.stem(word) for word in words if word.isalnum() and word.lower() not in self._stops[lang]
        ]

    def add(self, content: str, lang: str = "english") -> int:
        doc_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        doc_id = int(doc_hash, 16) & ((1 << 31) - 1)
        filepath = os.path.join(self._folder, f"{doc_id}.txt")

        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

        terms = self.preprocess_text(content, lang=lang)
        for term in terms:
            self._index.add(term, doc_id)
        self._index.save()
        return doc_id

    def query(self, word: str, lang: str = "english") -> BitMap:
        stemmed_word = self._stemmer.get(lang, PorterStemmer()).stem(word.lower())
        return self._index.const_get(stemmed_word, BitMap())

    def get_doc(self, doc_id: int) -> str | None:
        filepath = os.path.join(self._folder, f"{doc_id}.txt")
        if not os.path.isfile(filepath):
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
