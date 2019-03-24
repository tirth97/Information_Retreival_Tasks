import os
from builtins import any as b_any
import copy

"""
Here, we would create the 
"""


class PageRank:

    def __init__(self):
        self.graph_bfs = dict()

    def read_data_from_file_bfs(self):
        """
        Here, we read the data from the bsf files that we download using many
        :return:
        """
        dir_path = "./LinksData/InLinks/"
        try:
            dir_files = os.listdir(dir_path)

            for each_file in dir_files:
                with open(dir_path + each_file, 'r', encoding="utf-8") as file_data:
                    in_links = file_data.read()

                    list_inlinks = in_links.split("\n")

                    del list_inlinks[-1]

                    self.graph_bfs[each_file.split(".")[0]] = list_inlinks

        except Exception as e:
            print("File reading exception: "+str(e))

    def create_page_rank(self, lambda_value):
        i_vector = dict()
        r_vector = dict()

        list_websites = list(self.graph_bfs)
        # print(list_websites)

        for each_website in list_websites:
            i_vector[each_website] = (1/len(list_websites))

        diff = 1
        iteration_count = 1
        while diff > 0.0005 and iteration_count <= 4:
            print("here")
            diffsum = 0
            for each_website in list_websites:
                r_vector[each_website] = lambda_value / len(list_websites)

            for each_website in list_websites:
                list_inlinks = self.graph_bfs[each_website]
                q = []
                for each_link in list_inlinks:
                    if b_any(each_link in x for x in list_websites) \
                            and b_any(each_website in x for x in self.graph_bfs[each_link]):
                        q.append(each_link)

                if len(q) > 0:
                    for each_outlink in q:
                        r_vector[each_outlink] = r_vector[each_outlink] \
                                                 + ((1 - lambda_value)*(i_vector[each_website]/len(q)))
                else:
                    for each_website_inner in list_websites:
                        r_vector[each_website_inner] = r_vector[each_website_inner] \
                                                 + ((1 - lambda_value)*(i_vector[each_website_inner]/len(list_websites)))

            for each_website in list(r_vector):
                diffsum += ((r_vector[each_website] - i_vector[each_website])**2)

            i_vector = copy.deepcopy(r_vector)
            diff = diffsum**0.5

            iteration_count += 1

        return r_vector

    def write_rank_vector_to_file(self, r_vec, graph_type):
        # list_files = list(r_vector)

        file_path = "./RankingVector/"+graph_type+".txt"
        try:
            directory = os.path.dirname(file_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print("Error in directory formation: " + str(e))

        try:
            with open(file_path, "w+", encoding="utf-8") as bfs_file:
                for list_websites in list(r_vec):
                    bfs_file.write(list_websites + "," + str(r_vec[list_websites])+"\n")
        except Exception as e:
            print("File related exception: " + str(e))


if __name__ == "__main__":
    pg = PageRank()

    pg.read_data_from_file_bfs()
    r_vector = pg.create_page_rank(0.5)

    print("------------------------------R----------------------------------")
    print(r_vector)

    # pg.write_rank_vector_to_file(r_vector, "G1")
