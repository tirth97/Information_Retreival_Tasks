import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
The class that would make a DFS type crawl starting at the given link. I have used BeautifulSoup API here for parsing 
the HTML type of document. urllib library for 
"""
class CrawlerDFS:

    def __init__(self, max_webpages, max_depth):
        """
        The Constructor of the Crawler class.
        :param max_webpages: The maximum number of webpages to be crawled.
        :param max_depth: The max depth of the crawl.
        """
        self.max_webpages = max_webpages
        self.max_depth = max_depth
        self.total_links_traversed = 0
        self.url_set = set()

    def crawl_and_fetch_data_and_urls_dfs(self, url, url_start, depth_tree):
        """
        This method would crawl over the website data, fetch the url and write it to the file. This DFS method would be
        a recursion call to the function.
        :param url: The base URL to start with
        :param url_start: the base webpage to start with. Can also put "" if we just want to use the
        URL. (Needs to be improved in terms of reliability)
        :param depth_tree: The Current depth of the tree.
        :return: void
        """
        """
        This part controls the depth and the number of URL coverage.
        """
        if depth_tree == self.max_depth or self.total_links_traversed > self.max_webpages \
                or ((url+url_start) in self.url_set):
            return

        if url_start is None:
            url_start = ""

        try:
            """
            The URL request is made here and the data is fetched using BeautifulSoup parser.
            """
            response = requests.get(url+url_start,  timeout=3)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, features="html.parser")

                self.write_urls_to_file(url+url_start)

                # print("Depth: "+str(depth_tree))
                # print("Link number: "+str(self.total_links_traversed))
                # print("url: "+url+url_start)

                self.total_links_traversed += 1
                for link in soup.find_all('a'):
                    href = link.get('href')

                    """
                    The IF statements help to filter the unwanted URLs from the queue.
                    """
                    if (href is not None) and (".gov" not in href) \
                            and (("www." in href) or ("https:" in href) or ("http:" in href)) \
                            and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):
                        response.close()
                        self.crawl_and_fetch_data_and_urls_dfs(href, "", depth_tree + 1)
                        self.url_set.add(href)

                    elif (href is not None) and (".gov" not in href) and (".jpg" not in href) and (".png" not in href) \
                            and ('#' not in href) \
                            and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):
                        response.close()
                        self.crawl_and_fetch_data_and_urls_dfs(urljoin(url, href).rstrip('/'), "", depth_tree + 1)
                        self.url_set.add(urljoin(url, href).rstrip('/'))

        except Exception as e:
            print("Error Occurred: " + str(e))
            pass

    def write_urls_to_file(self, url):
        """
        Method used to write the urls into the file named "dfs_links.txt"
        :param url: The url from the crawl, that would be recorded.
        :return: void
        """

        try:
            file_path = "./DataFiles/dfs_links.txt"
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: " + str(e))

        try:
            with open("./DataFiles/dfs_links.txt", "a+", encoding="utf-8") as dfs_file:
                dfs_file.write(url+"\n\n")
        except Exception as e:
            print("File related exception: "+str(e))


if __name__ == "__main__":
    dfs = CrawlerDFS(1000, 6)
    dfs.crawl_and_fetch_data_and_urls_dfs("https://en.wikipedia.org", "/wiki/Space_exploration", 0)
    dfs.url_set.clear()


