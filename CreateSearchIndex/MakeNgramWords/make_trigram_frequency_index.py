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

    def make_trigram_index(self):
        dir_path = "./Unigram/BFS/"

        index_trigram = dict()

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

                    trigrams = list(ngrams(words, 3))

                    trigrams_list = [' '.join(w) for w in trigrams]

                    try:

                        for each_trigrams in trigrams_list:
                            if each_trigrams in list(index_trigram) and doc_name in list(index_trigram[each_trigrams]):
                                index_trigram[each_trigrams][doc_name] += 1
                            else:
                                index_trigram[each_trigrams] = dict({doc_name: 1})

                    except Exception as e:
                        print("Word indexing problem: "+str(e))
                i += 1
                if i > 10:
                    break
        except Exception as e:
            print("Error while reading: "+str(e))

        self.write_inverted_index_to_file(index_trigram, "vocabulary_trigrams_freq.pkl")

    def write_inverted_index_to_file(self, index, file_name):
        """
        This method writes the index to the file. It takes the dictionary object and writes it using pickle.
        :param index: The index to be written on file.
        :param file_name: The name of the file with .pkl extension included.
        :return: None. It writes to the file.
        """
        pickle_object_dir = "./Trigrams/Vocabulary/"

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
    mv.make_trigram_index()
