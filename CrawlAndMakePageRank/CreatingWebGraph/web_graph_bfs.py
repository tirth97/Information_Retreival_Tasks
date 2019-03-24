import os
import re
import requests
from bs4 import BeautifulSoup
from builtins import any as b_any

"""
This is the crawler, which fetches the data of the set of links given in BFS.txt, crawls and creates the Graph as shown 
in Problem 2.
"""


class WebGraph:

    def __init__(self):
        self.graph = dict()

    def parse_and_create_map(self, url):
        try:
            """
            The URL request is made here and the data is fetched using BeautifulSoup parser.
            """

            response = requests.get(url,  timeout=3)
            if response.status_code == 200:
                url_set = set()
                text = response.text
                soup = BeautifulSoup(text, features="html.parser")

                file_url_name = url.split("/")[-1].split("#")[0]

                """
                Get only Body text from Page, ignoring References, right navigation and URLS below images
                """
                if len(soup.find('ol', attrs={'class': 'references'}) or ()) > 1:
                    soup.find('ol', attrs={'class': 'references'}).decompose()
                if len(soup.find('div', attrs={'class': 'thumb tright'}) or ()) > 1:
                    soup.find('div', attrs={'class': 'thumb tright'}).decompose()
                if len(soup.find('div', attrs={'id': 'toc'}) or ()) > 1:
                    soup.find('div', attrs={'id': 'toc'}).decompose()
                if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}) or ()) > 1:
                    soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}).decompose()
                if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}) or ()) > 1:
                    soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}).decompose()

                data = soup.find('div', attrs={'id': 'mw-content-text'})

                for urls in data.find_all('a', attrs={'href': re.compile("^/wiki")}):
                    href_url = urls.get('href')
                    # to exclude the administrative URLs
                    if ':' not in href_url:
                        url_set.add(href_url.split('/')[2])

                self.graph[file_url_name] = url_set

        except Exception as e:
            print("Error Occurred " + str(e))

    def parse_file(self, filename):
        try:
            with open("./"+filename, 'r') as file:
                data = file.read()
                links = data.split("\n")
                for each_link in links:
                    # print(each_link)
                    print(each_link)
                    self.parse_and_create_map(each_link)

        except Exception as e:
            print("Error in directory formation: " + str(e))

    def create_graph_from_map(self):
        list_urls = list(self.graph)

        url_vs_incoming_links = dict()

        for each_url in list_urls:
            in_links = []
            for listed_url in list_urls:
                if b_any(each_url in x for x in self.graph[listed_url]):
                    in_links.append(listed_url)
            url_vs_incoming_links[each_url] = in_links

        print("--------------------Graph--------------------")
        print(url_vs_incoming_links)

        self.write_dictionary_to_file(url_vs_incoming_links)

    def write_dictionary_to_file(self, url_vs_incoming_links):

        list_files = list(url_vs_incoming_links)
        for each_file in list_files:

            file_path = "./LinksData/InLinks/" + each_file + ".txt"
            try:
                directory = os.path.dirname(file_path)

                if not os.path.exists(directory):
                    os.makedirs(directory)
            except Exception as e:
                print("Error in directory formation: " + str(e))

            try:
                with open(file_path, "w+", encoding="utf-8") as bfs_file:
                    for each_inlink in url_vs_incoming_links:
                        bfs_file.write(each_inlink+"\n")
            except Exception as e:
                print("File related exception: "+str(e))


if __name__ == "__main__":
    wg = WebGraph()
    wg.parse_file("BFS.txt")
    wg.create_graph_from_map()


