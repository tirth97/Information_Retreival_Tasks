import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import queue


"""
With implementation much similar to CrawlerBFS class in scraper_bfs file. The only difference here is that we only crawl
those sites that have some keyword as entered in the query.
"""


class CawlerWithAnchor:

    def __init__(self, max_webpages):
        self.urls_crawled = []
        self.max_webpages = max_webpages
        self.links_per_depth_counter = 0
        self.next_level_children = 0
        self.url_parsing_queue = queue.Queue()
        self.depth = 0
        self.total_links_traversed = 0
        self.unique_url_crawls = 0

    def crawl_and_fetch_data_and_urls_bfs(self, url, url_start, write_url_or_data, anchor_text):
        """
        The function that would take stsrting url and use anchor text to search for the text in the links of the
        webpage.
        :param url: The starting URL.
        :param url_start:  The starting subpage, can be put as "" as well.
        :param write_url_or_data: Flag that mentions if we want to just write url or url and data.
        :param anchor_text: the text to be searched in the webpages.
        :return: void
        """
        if url_start is None:
            url_start = ""

        try:
            response = requests.get(url+url_start,  timeout=3)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, features="html.parser")

                # if write_url_or_data == 1:
                #     self.write_data_to_file(url+url_start, text)
                # else:
                #     self.write_urls_to_file(url+url_start)


                self.total_links_traversed += 1
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if (href is not None) and (".gov" not in href) \
                            and (("www." in href) or ("https:" in href) or ("http:" in href)) \
                            and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):

                        if self.check_text_inclusion(href, anchor_text):
                            self.next_level_children += 1
                            self.url_parsing_queue.put(href)
                            # print(self.next_level_children)
                            # print(url)
                            self.write_urls_to_file(url)

                    elif (href is not None) and (".gov" not in href)\
                            and (".jpg" not in href) and (".png" not in href) and \
                            ('#' not in href) and (("%D" not in href) and ("%B" not in href) and ("%E" not in href)):
                        if self.check_text_inclusion(urljoin(url, href).rstrip('/'), anchor_text):
                            self.next_level_children += 1
                            self.url_parsing_queue.put(urljoin(url, href).rstrip('/'))
                            # print(self.next_level_children)
                            # print(urljoin(url, href).rstrip('/'))
                            self.write_urls_to_file(urljoin(url, href).rstrip('/'))
            response.close()
        except Exception as e:
            print("Error Occurred" + str(e))
            pass

    def check_text_inclusion(self, url, anchor_text):
        """
        This function checks if the given text is present in the page of given url or not.
        :param url: The url for checking
        :param anchor_text: the text that would be the key for searching
        :return: True if it is found in the page with given URL link else False.
        """
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            text = response.text
            response.close()
            return anchor_text in text

    def get_urls(self, depth_of_tree, anchor_text):
        """
        The function that controls the depth and the max urls that would be crawled.
        :param depth_of_tree: the max depth of the crawl.
        :param anchor_text: the text used in the crawl.
        :return: void
        """
        self.links_per_depth_counter = self.next_level_children
        self.next_level_children = 0
        self.depth += 1
        while self.depth <= depth_of_tree and self.total_links_traversed < self.max_webpages:
            while self.links_per_depth_counter > 0 and self.total_links_traversed < self.max_webpages:
                self.links_per_depth_counter -= 1
                url = self.url_parsing_queue.get()
                self.crawl_and_fetch_data_and_urls_bfs(url, "", 0, anchor_text)
            self.links_per_depth_counter = self.next_level_children
            self.next_level_children = 0
            self.depth += 1

    def write_urls_to_file(self, url):
        """
        Function to write URLs into a given file.
        :param url: The URL to be written.
        :return: void
        """
        try:
            file_path = "./DataFiles/bfs_anchor.txt"
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: "+str(e))
        try:
            with open("./DataFiles/bfs_anchor.txt", "a+", encoding="utf-8") as bfs_file:
                bfs_file.write(url+"\n\n")
        except Exception as e:
            print("File related exception: "+str(e))


if __name__ == "__main__":
    anc = CawlerWithAnchor(1000)
    anc.crawl_and_fetch_data_and_urls_bfs("https://en.wikipedia.org", "/wiki/Space_exploration", 0, "Rover")
    anc.get_urls(6, "Rover")


