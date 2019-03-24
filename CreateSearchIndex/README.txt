Design explanation:


***Selecting Data Structure for the Indexes:***
-> For selecting the data structure, I have these formats:
For term -> docId -> frequency:
dictionary(term(string): dictionary(docId(nameOfFile): frequency(int)))

For term -> docId -> list(positions):
dictionary(term(string): dictionary(docId(nameOfFile): list_of_positions(int)))

The program here is divided into some parts and based on the parts the operations are performed inorder to attain the
desired operations.

Part 1) Indexing or Inverted Index creation

Here, we would parse all the files from the BFS crawl, get the tokens and then, we would create two inverted index.
One index is of type: term -> docId -> frequency
Another index is of type: term -> docId -> list(positions)

The indexes created here are stored in a .pkl file which stores the dict object of above two types in a file.
These indexes are then further used to create searches.

Files make_vocabulary.py, make_bigram_frequency_index.py, make_trigram_frequency_index.py are used for the index
creation purpose.

File read_vocabulary.py can be utilized to fetch the object stores in the .pkl file and utilized for further search
purpose.

Part 2) Searching:
For searching with query words, we would use file search_queries.py file, the file has directions given at the end of
each file.

The results are stored in a directory SearchResults and the file name format is:
<QueryWordsInCamelCase><k value>.txt

Part 3) Statistics of words and frequency portion:

File sort_and_create_table.py is used.

The index of term -> docId-> Frequency is used here to get term -> termFrequency.

They are sorted and the results are kept in files like:

t_d_f.txt contains term -> docId -> frequency type results
ttf.txt contains term -> frequency type results

The directions to use would be given at the end of the file.


Task wise seperation:
Task 1 files:
Term->docId->Frequency Index is at: vocabulary_bfs_freq_new_ds.pkl
Term->docId->list(positions) is at: vocabulary_bfs_positional_new_ds.pkl
You would need to run read_vocabulary.py to access it, the directions are provided at the end of the file with an
example.
Use appropriate location to read the file as shown in the example in read_vocabulary.py

Task 2 files:
These are stored in Task 2 folder

Task 3 files:
These are stored in Task 3 folder and the each file would have following format:
t_d_f.txt contains term -> docId -> frequency type results
ttf.txt contains term -> frequency type results



******Selecting Threshold for stopwords:******
-> Stopwords would be the words that have very high frequency and would generally make no  difference to our search
results.
-> Here, based on the results, we see that since our crawl is focused on space exploration, words like "space", "orbit",
"nasa" are really common and so if there is a bigger query with more number of words, we can ignore these words since
they are very frequent.
-> So, we are using 1000 documents for the crawl and each word, if it occurs more than 5 times, it might not be very
useful for the search of queries with more words.
-> However, they might be significant for queries like "earth orbit".
-> So, in my suggestion, stopwords should be removed with threshold of 5000 but only for queries having more than 5 to 6
words.




NOTE:
I could not complete the processing of the bigrams and trigrams and so, I am submitting only some stop words of bigrams
and trigrams category.


