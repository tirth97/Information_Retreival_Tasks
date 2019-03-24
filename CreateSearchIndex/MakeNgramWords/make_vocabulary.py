import os
import pickle
"""
In this class we would make the index from all the files that were fetched from the BFS crawl. 
The file names and locations are hardcoded here for running the file, we can change the initial directory location and 
change the docs for indexing.
"""


class MakeIndex:

    def __init__(self):
        pass

    def fetch_data_from_file_and_make_index(self, directory):
        """
        The function which fetches the data from the file, tokenizes the words and creates an index that is saved in a
        file as a pickle file in which the object is stored.
        :param directory: The directory where the crawled files are located.
        :return: None
        """
        dir_path = directory

        vocabulary = dict()
        vocabulary_positional_list = dict()

        try:
            dir_files = os.listdir(dir_path)

            for each_file in dir_files:
                print("file: " + each_file)
                print()

                with open(dir_path+each_file, 'r', encoding="utf-8") as token_file:
                    data = token_file.read()
                    words = data.split(", ")

                    try:
                        name_position_map = dict()
                        name_frequency_map = dict()
                        i = 0
                        for each_word in words:
                            if each_word in list(name_position_map):
                                name_position_map[each_word].append(i)
                                name_frequency_map[each_word] += 1
                            else:
                                name_position_map[each_word] = [i]
                                name_frequency_map[each_word] = 1
                            i += 1

                        for each_word in list(name_position_map):

                            if each_word in list(vocabulary):
                                vocabulary[each_word][each_file.split(".txt")[0]] = name_frequency_map[each_word]
                                vocabulary_positional_list[each_word][each_file.split(".txt")[0]] = name_position_map[each_word]
                            else:
                                vocabulary[each_word] \
                                    = dict({each_file.split(".txt")[0]: name_frequency_map[each_word]})
                                vocabulary_positional_list[each_word] \
                                    = dict({each_file.split(".txt")[0]: name_position_map[each_word]})

                    except Exception as e:
                        print("Words Exception: "+str(e))

        except Exception as e:
            print("Error while reading: "+str(e))

        self.write_inverted_index_to_file(vocabulary, "vocabulary_bfs_freq_new_ds.pkl")
        self.write_inverted_index_to_file(vocabulary_positional_list, "vocabulary_bfs_positional_new_ds.pkl")

    def write_inverted_index_to_file(self, index, file_name):
        """
        This method writes the index to the file. It takes the dictionary object and writes it using pickle.
        :param index: The index to be written on file.
        :param file_name: The name of the file with .pkl extension included.
        :return: None. It writes to the file.
        """
        pickle_object_dir = "./Vocabulary/"

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
    mv = MakeIndex()
    mv.fetch_data_from_file_and_make_index("./Unigram/BFS/")
