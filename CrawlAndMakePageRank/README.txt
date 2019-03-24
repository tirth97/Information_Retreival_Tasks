Here, I have provided the classification of files with folders, the separated folders would seperate the implementation of each task.
There are harcoded values in the files, which I have modified as per the folder structures provided.


Order of running of files for each task:

Task 1:
First run local_bfs_data.py before running tokenize_crawled_files.py

the order is because, I have seperated the crawling from tokenizing part.

Similarly for focused crawling, use local_focused_data.py before running tokenize_focus_crawled_files.py

The data would be stored in ./BFSDataCrawl/WebsiteData/* for the BFS crawl and ./FocusedDataCrawl/WebsiteData for
Focused crawl. While the Trigrams are stored in ./Trigrams/BFS for BFS and ./Trigrams/Focused for Focused.

Task 2:

run web_graph_bfs.py for BFS crawl and to get G1

run web_graph_focused.py to get the FOCUSED graph to get G2

Task 3:

run task page_rank_implementation.py for G1 ranks

run task page_rank_implementation_focused.py for G2 ranks

These ranks would be stored in ./RankingVector/G1 for G1 graph and ./RankingVector/G2 for G2 graph

Here, we take the Graph constructed in Task 2 to make the rankings. ./LinksData/InLinks contains data of G1 graph and
./LinksData/Focused for Focused Crawl results.

