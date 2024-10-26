from libs.index import InvertedIndex
from libs.base import SearchBase

from pyroaring import BitMap


def main():
    index = InvertedIndex("./data/index.pkl")
    base = SearchBase(index, "./data/docs")

    while True:
        prompt = input("Prompt: ")
        a = prompt.split(maxsplit=1)
        if len(a) != 2:
            continue
        if a[0].lower() == "add":
            doc_id = base.add(a[1])
            print(f"Added, Doc ID: {doc_id}")
        elif a[0].lower() == "find":
            or_queries = ''.join(a[1].split()).split("|")
            result = BitMap()
            for or_q in or_queries:
                subr = None
                for and_q in or_q.split("&"):
                    resp = base.query(and_q)
                    subr = subr & resp if subr is not None else resp.copy()
                if subr:
                    result |= subr
            print(result)
        elif a[0].lower() == "get":
            print(base.get_doc(a[1]))


if __name__ == "__main__":
    main()
