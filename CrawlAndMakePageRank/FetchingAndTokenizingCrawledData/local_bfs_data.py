import os
import requests
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner
import re
import io

"""
This would load the links from the BFS.txt file, crawl them and fetch the data to create the data for Task 1 
"""

class LocalBFSData:

    def __init__(self):
        self.links = []

    def fetch_bfs_links(self):
        with open("./BFS.txt", 'r') as file:
            data = file.read()
            self.links = data.split("\n")

            for each_link in self.links:
                print(each_link)
                self.fetch_data_from_links(each_link)

    def fetch_data_from_links(self, each_link):
        try:
            response = requests.get(each_link, timeout=3)
            if response.status_code == 200:
                text = response.text
                cleaned_text = self.clean_data(text)
                file_url_name = each_link.split("/")[-1].split("#")[0]
                self.write_data_to_file(cleaned_text, file_url_name)
        except Exception as e:
            print("Error: "+str(e))

    def clean_data(self, text):
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter

        lx = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(io.StringIO(text))))

        soup = BeautifulSoup(lx, features="html.parser")

        processed_text = soup.get_text().replace("\n", " ").strip()

        return re.sub(' +', ' ', processed_text)

    def write_data_to_file(self, data, file_name):

        file_path = "./BFSDataFiles/WebsiteData/" + file_name + ".txt"
        try:
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: " + str(e))

        try:
            with open(file_path, "w+", encoding="utf-8") as bfs_file:
                bfs_file.write(data)
        except Exception as e:
            print("File related exception: "+str(e))


if __name__ == "__main__":
    bfs_data = LocalBFSData()
    bfs_data.fetch_bfs_links()
