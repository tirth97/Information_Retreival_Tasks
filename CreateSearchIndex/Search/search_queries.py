import os
from read_vocabulary import ReadVocabulary
"""
This class would help run the queries. We would be giving the query words and the distance k of the distance of words.
"""


class SearchQueries:

    def __init__(self):
        pass

    def make_search_query(self, query_string, k):
        """
        The method where, we pass the query and the distance, it would write the documents that have the words within k
        distance and stores it in a file.
        :param query_string: the query string
        :param k: the distance between the two successive words
        :return: None
        """
        query_words = query_string.split(" ")

        for i in range(len(query_words)):
            query_words[i] = query_words[i].lower()

        vocabulary = self.get_vocabulary("./Unigram/Vocabulary/vocabulary_bfs_positional_new_ds.pkl")

        search_results = self.proximate_search(vocabulary, query_words, k)

        self.write_search_results_to_file(search_results, query_string, k)

    def proximate_search(self, vocabulary, query_words, k):
        """
        The proximity search algorithm that would return the list of documents that follow the condition.
        :param vocabulary: the index to be searched.
        :param query_words: the words we are searching
        :param k: the proximity distance
        :return: The list of search results
        """
        search_results = []

        for i in range(len(query_words)-1):
            for each_location1 in list(vocabulary[query_words[i]]):
                if each_location1 in list(vocabulary[query_words[i+1]]):

                    if self.is_proximate(vocabulary[query_words[i]][each_location1],
                                         vocabulary[query_words[i+1]][each_location1], k):
                        search_results.append(each_location1)

        return search_results

    def is_proximate(self, word_list_1, word_list_2, k):
        """
        This method would return of the words are proximate within two lists or not.
        :param word_list_1: the list of word1
        :param word_list_2: the list of word2
        :param k: the distance
        :return: True i the words are within k distance
        """
        for i in range(len(word_list_1)):
            for j in range(len(word_list_2)):
                if abs(word_list_1[i] - word_list_2[j]) <= k:
                    return True

        return False

    def get_vocabulary(self, files_location):
        """
        The method that would help fetch the index that we will use to search.
        :param files_location: The location of the file.
        :return: The index reading from the file.
        """
        vocab_reader = ReadVocabulary()
        return vocab_reader.read_from_pickle_file(files_location)

    def write_search_results_to_file(self, search_results, query_words, k):
        """
        Writing the results in a file.
        :param search_results: the list of the search results
        :param query_words: the queries
        :param k: the distance that would be used to make file name
        :return: None
        """
        results_dir = "./SearchResults/" + ''.join(x for x in query_words.title() if not x.isspace()) + str(k) + ".txt"
        try:
            directory = os.path.dirname(results_dir)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("error in directory formation: " + str(e))

        try:
            with open(results_dir, 'w+') as search_results_file:
                for each_doc in search_results:
                    search_results_file.write(each_doc+"\n")
        except Exception as e:
            print("File Writing Exception: "+str(e))


"""
Example of use of class.
"""

if __name__ == "__main__":
    sq = SearchQueries()
    sq.make_search_query("space mission", 6)
    sq.make_search_query("space mission", 12)
    sq.make_search_query("earth orbit", 5)
    sq.make_search_query("earth orbit", 10)
