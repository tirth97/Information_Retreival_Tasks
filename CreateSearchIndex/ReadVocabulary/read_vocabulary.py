import pickle
"""
This class provides functionality to read the pickle file and restore the object. 
It would return the object that was stored in the pickle file.
"""


class ReadVocabulary:

    def __init__(self):
        pass

    def read_from_pickle_file(self, file_location_name):
        """
        It would read the .pkl file, and returns the object stored.
        :param file_location_name: The name of file with .pkl extension.
        :return: The object that was stored.
        """
        try:
            with open(file_location_name, 'rb') as pickle_file:
                vocabulary = pickle.load(pickle_file)

            return vocabulary

        except Exception as e:
            print("File reading exception: "+str(e))


"""
This is the example of using the class. 
"""
# if __name__ == "__main__":
#     rv = ReadVocabulary()
#     rv.read_from_pickle_file("./UniGram/Vocabulary/vocabulary_bfs.pkl")
