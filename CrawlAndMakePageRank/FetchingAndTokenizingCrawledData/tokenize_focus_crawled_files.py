import os
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import string

"""
Here we tokenize and prepare trigrams of the data obtained from the focused crawler.
"""
class TokenizeFocusCrawledData:

    def __init__(self):
        pass

    def read_data_and_load_data(self, type_data):
        """
        This function takes the type of data to be crawled as an argument which is essentially to mention if we would
        crawl Focused data or BFS data.
        :param type_data: input either "BFS" or "FOCUSED"
        :return: None. This method in its flow writes the data to the files.
        """
        dir_path = "./FocusedDataCrawl/WebsiteData/"
        try:
            dir_files = os.listdir(dir_path)

            stop_words = set(stopwords.words('english'))

            for each_file in dir_files:
                print("file: "+each_file)
                print()
                filtered_sentence = []
                with open(dir_path + each_file, 'r', encoding="utf-8") as file_data:
                    data = file_data.read()

                    # Conversion to lowercase
                    lower_data = data.lower()

                    word_tokens = word_tokenize(lower_data, 'english')

                    # Here, we remove stop words, punctuations ot any other symbols from the tokens that are formed
                    filtered_sentence = [w for w in word_tokens if not ((w in stop_words) or (w in string.punctuation)
                                                                        or (w in
                                                                            {'[','(',')',']','{','}',':','/','\\', '^'})
                                                                        or (len(w) < 2))]

                # We then send the data for trigram formation.
                trigrams = self.get_trigrams(filtered_sentence)

                new_dir_path = "./Trigrams/"+type_data+"/"

                # Here we write the data to files.
                try:
                    directory = os.path.dirname(new_dir_path)

                    if not os.path.exists(directory):
                        os.makedirs(directory)
                except Exception as e:
                    print("error in directory formation: "+str(e))

                try:
                    with open(new_dir_path+each_file, "w+", encoding="utf-8") as trigram_file:
                        trigram_file.write(str(trigrams))
                except Exception as e:
                    print("Error in file formation:"+str(e))

        except Exception as e:
            print("Error in directory formation: " + str(e))

    def get_trigrams(self, data):
        """
        Trigrams are generated here.
        :param tokens: the tokens
        :return: Trigrams of the given tokens
        """
        trigrams = [t for t in nltk.trigrams(data)]
        # print(trigrams)
        return trigrams

"""
The part from where we run the above functions. Though, I have put another file for Focused crawled results, we can also 
replace "BFS" to "FOCUSED".
"""
if __name__ == "__main__":
    nltk.download('words')
    tokenized_data = TokenizeFocusCrawledData()
    tokenized_data.read_data_and_load_data("FOCUSED")


