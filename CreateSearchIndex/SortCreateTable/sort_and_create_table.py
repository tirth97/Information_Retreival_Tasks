import os
from read_vocabulary import ReadVocabulary
"""
Here we create a table, a sort of data structure that shows the statistics. We would use the statistics to filter out 
stop words and other such operations would be performed.
"""


class CreateTable:

    def __init__(self):
        pass

    def create_word_frequency_corpus_map(self, read_from_file, to_be_written_location, threshold):
        index = self.read_index_from_file(read_from_file)

        word_corpus_frequency = dict()

        for each_word in list(index):
            total_frequency = 0
            for each_document in list(index[each_word]):
                total_frequency += index[each_word][each_document]

            word_corpus_frequency[each_word] = total_frequency

        sorted_corpus_frequency = self.sort_by_values(word_corpus_frequency)

        sorted_term_doc_frequency = self.sort_by_keys(index)

        self.stop_lists(sorted_corpus_frequency, to_be_written_location+"stop_list.txt", threshold)

        self.write_sorted_term_frequency_to_file(sorted_corpus_frequency,
                                                 to_be_written_location + "ttf.txt")

        self.write_sorted_term_frequency_to_file(sorted_term_doc_frequency,
                                                 to_be_written_location + "t_d_f.txt")


    def read_index_from_file(self, read_from_file):
        return ReadVocabulary().read_from_pickle_file(read_from_file)

    def sort_by_values(self, word_corpus_frequency):

        sorted_by_values = sorted(word_corpus_frequency.items(), key=lambda kv: kv[1], reverse=True)

        return sorted_by_values

    def sort_by_keys(self, index):
        sorted_by_key = []
        for key in sorted(index):
            sorted_by_key.append((key, index[key]))

        return sorted_by_key

    def write_sorted_term_frequency_to_file(self, sorted_tuples, file_name):
        try:
            directory = os.path.dirname(file_name)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("error in directory formation: " + str(e))

        try:
            with open(file_name, 'w+', encoding='utf-8') as tf_file:
                for each_term in sorted_tuples:
                    tf_file.write(str(each_term)+"\n")
        except Exception as e:
            print("File writing exception: "+str(e))

    def stop_lists(self, index, file_name, threshold):

        stop_words_list = []

        for each_term in index:
            if each_term[1] > threshold:
                stop_words_list.append(each_term)
            else:
                break

        self.write_sorted_term_frequency_to_file(stop_words_list, file_name)


if __name__ == "__main__":
    ct = CreateTable()
    ct.create_word_frequency_corpus_map("./Unigram/Vocabulary/vocabulary_bfs_freq_new_ds.pkl",
                                        "./Unigram/TermFrequencyComparision/", 5000)
    ct.create_word_frequency_corpus_map("./Trigrams/Vocabulary/vocabulary_trigrams_freq.pkl",
                                        "./Trigrams/TermFrequencyComparision/", 45)
    ct.create_word_frequency_corpus_map("./Bigrams/Vocabulary/vocabulary_bigrams_freq.pkl",
                                        "./Bigrams/TermFrequencyComparision/", 45)
