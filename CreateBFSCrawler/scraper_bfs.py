import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import queue


class CrawlerBFS:
    """
    The class of
    """
    def __init__(self, max_webpages):
        self.urls_crawled = []
        self.max_webpages = max_webpages
        self.links_per_depth_counter = 0
        self.next_level_children = 0
        self.url_parsing_queue = SetQueue(1100)
        self.depth = 0
        self.total_links_traversed = 0

    def crawl_and_fetch_data_and_urls_bfs(self, url, url_start, write_url_or_data):
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

                """
                Parameter to decide, if we want to write the data and the url or just the URL to the file.
                """
                if write_url_or_data == 1:
                    self.write_data_to_file(url+url_start, text)
                else:
                    self.write_urls_to_file(url+url_start)

                self.total_links_traversed += 1
                for link in soup.find_all('a'):
                    href = link.get('href')

                    """
                    The IF statements help to filter the unwanted URLs from the queue.
                    """
                    if (href is not None) and (".gov" not in href) \
                            and (("www." in href) or ("https:" in href) or ("http:" in href)) \
                            and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):

                        self.next_level_children += 1
                        self.url_parsing_queue.put(href)

                    elif (href is not None) and (".gov" not in href)\
                            and (".jpg" not in href) and (".png" not in href) and \
                            ('#' not in href) and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):

                        self.next_level_children += 1
                        self.url_parsing_queue.put(urljoin(url, href).rstrip('/'))
                    response.close()
        except Exception as e:
            print("Error Occurred")
            pass

    def get_urls(self, depth_of_tree):

        """
        This method essentially helps in traversing the links and controlling the number of URL crawls and control on
        the depth that would be traversed.
        :param depth_of_tree: The max depth that would be traversed.
        :return:
        """
        self.links_per_depth_counter = self.next_level_children
        self.next_level_children = 0
        self.depth += 1
        while self.depth <= depth_of_tree and self.total_links_traversed < self.max_webpages:
            while self.links_per_depth_counter > 0 and self.total_links_traversed < self.max_webpages:
                print(self.links_per_depth_counter)
                self.links_per_depth_counter -= 1
                url = self.url_parsing_queue.get()
                print(url)
                self.crawl_and_fetch_data_and_urls_bfs(url, "", 0)
            self.links_per_depth_counter = self.next_level_children
            self.next_level_children = 0
            self.depth += 1

    def write_data_to_file(self, url, data):

        try:
            file_path = "./DataFiles/bfs.txt"
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: " + str(e))

        try:
            with open("./DataFiles/bfs.txt", "a+", encoding="utf-8") as bfs_file:
                bfs_file.write(url+"\n\n")
                bfs_file.write(data)
        except Exception as e:
            print("File related exception: "+str(e))

    def write_urls_to_file(self, url):

        try:
            file_path = "./DataFiles/bfs_links.txt"
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: " + str(e))

        try:
            with open("./DataFiles/bfs_links.txt", "a+", encoding="utf-8") as bfs_file:
                bfs_file.write(url+"\n\n")
        except Exception as e:
            print("File related exception: "+str(e))


class SetQueue(queue.Queue):
    """
    A class that overrides queue.Queue and makes a queue of type set instead of a list type.
    """
    def _init(self, maxsize):
        self.queue = set()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()


if __name__ == "__main__":
    bfs = CrawlerBFS(1000)
    bfs.crawl_and_fetch_data_and_urls_bfs("https://en.wikipedia.org", "/wiki/Space_exploration", 0)
    bfs.get_urls(6)


