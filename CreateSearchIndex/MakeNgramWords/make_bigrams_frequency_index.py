import os
import pickle
from nltk.util import ngrams
"""
In this class we would make the index from all the files that were fetched from the BFS crawl. 
The file names and locations are hardcoded here for running the file, we can change the initial directory location and 
change the docs for indexing.
"""


class MakeVocabulary:

    def __init__(self):
        pass

    def make_bigram_index(self):
        dir_path = "./Unigram/BFS/"

        index_bigram = dict()

        try:
            dir_files = os.listdir(dir_path)
            i = 0
            for each_file in dir_files:
                print("file: " + each_file)
                print()

                doc_name = each_file.split(".txt")[0]

                with open(dir_path+each_file, 'r', encoding="utf-8") as token_file:
                    data = token_file.read()
                    words = data.split(", ")

                    bigrams = list(ngrams(words, 2))

                    bigrams_list = [' '.join(w) for w in bigrams]

                    try:

                        for each_bigram in bigrams_list:
                            if each_bigram in list(index_bigram) and doc_name in list(index_bigram[each_bigram]):
                                index_bigram[each_bigram][doc_name] += 1
                            else:
                                index_bigram[each_bigram] = dict({doc_name: 1})

                    except Exception as e:
                        print("Word indexing problem: "+str(e))
                i+=1
                if i > 10:
                    break
        except Exception as e:
            print("Error while reading: "+str(e))

        self.write_inverted_index_to_file(index_bigram, "vocabulary_bigrams_freq.pkl")

    def write_inverted_index_to_file(self, index, file_name):
        """
        This method writes the index to the file. It takes the dictionary object and writes it using pickle.
        :param index: The index to be written on file.
        :param file_name: The name of the file with .pkl extension included.
        :return: None. It writes to the file.
        """
        pickle_object_dir = "./Bigrams/Vocabulary/"

        try:
            directory = os.path.dirname(pickle_object_dir)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("error in directory formation: " + str(e))

        try:
            with open(pickle_object_dir+file_name, 'wb') as pickle_file:
                pickle.dump(index, pickle_file, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("File Writing Exception: "+str(e))


if __name__ == "__main__":
    mv = MakeVocabulary()
    mv.make_bigram_index()
