# coding: utf-8
import mmh3
import doc2words
import docreader
from collections import defaultdict
import pickle
import varbyte
import query_tree


class Index:

    def __init__(self, files_list=[], compression='', from_doc_reader=0):

        if from_doc_reader:
            self.compression = compression
            self.index = defaultdict(list)

            reader = docreader.DocumentStreamReader(files_list)

            doc_id = 0
            self.urls = []

            for document in reader:

                url = document.url
                text = document.text

                self.urls.append(url)

                words = list(set(doc2words.extract_words(text)))

                for word in words:

                    key = Index.unicode_to_key(word)
                    self.index[key].append(doc_id)
                doc_id += 1

            self.compress()

        else:
            self.load()

    @staticmethod
    def unicode_to_key(word):
        return mmh3.hash(word.lower().encode('utf-8'))

    def compress(self):
        for term in self.index.keys():
            self.index[term] = self.compress_doc_ids(self.index[term])

    def compress_doc_ids(self, doc_ids):
        if self.compression == 'varbyte':
            return varbyte.compress(doc_ids)
        
    def decompress_doc_ids(self, doc_ids):
        if self.compression == 'varbyte':
            return varbyte.decompress(doc_ids)
        
    def doc_ids_by_term(self, term):
        return set(decompress_doc_ids(self.index[mmh3.hash(term)])))

    def urls_by_query(self, query):
        tokens = query_tree.tokenize_query(query.decode('utf-8').lower())
        tree = query_tree.build_query_tree(tokens)
        ids = list(query_tree.evaluate_query_tree(tree, self.index))
        ids.sort()
        return [self.urls[doc_id] for doc_id in ids]

    def dump(self):
        with open('index.pkl', 'w') as f:
            pickle.dump(self.index, f)

        with open('urls.pkl', 'w') as f:
            pickle.dump(self.urls, f)

        with open('compression.pkl', 'w') as f:
            pickle.dump(self.compression, f)

    def load(self):
        with open('index.pkl', 'r') as f:
            self.index = pickle.load(f)

        with open('urls.pkl', 'r') as f:
            self.urls = pickle.load(f)

        with open('compression.pkl', 'r') as f:
            self.compression = pickle.load(f)


if __name__ == '__main__':
    args = docreader.parse_command_line().files

    files = args[1:]
    compression = args[0]

    index = Index(files, compression, 1)

    index.dump()
