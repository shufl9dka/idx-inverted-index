import os
import pickle

from pyroaring import BitMap


class InvertedIndex:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._mem: dict[str, BitMap] = {}
        self.load()

    def const_get(self, term: str, default: BitMap = None):
        return self._mem.get(term, default)

    def add(self, term: str, doc_id: int):
        if term not in self._mem:
            self._mem[term] = BitMap()
        self._mem[term].add(doc_id)

    def save(self):
        with open(self._filepath, "wb") as f:
            pickle.dump(self._mem, f)

    def load(self):
        if not os.path.isfile(self._filepath):
            return
        with open(self._filepath, "rb") as f:
            self._mem = pickle.load(f)
