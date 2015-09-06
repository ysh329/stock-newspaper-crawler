# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_newspaper_metadata.py
# Description:
#


# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-9-3 11:06:43
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import logging
import MySQLdb
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os.path
#from matplotlib.ticker import FuncFormatter
#from compiler.ast import flatten
################################### PART2 CLASS && FUNCTION ###########################
class ComputeNewspaperMetaData(object):
    def __init__(self, database_name, result_save_directory):
        self.start = time.clock()

        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  filename = './main.log',
                  filemode = 'a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s')
        console.setFormatter(formatter)

        logging.getLogger('').addHandler(console)
        logging.info("START.")

        try:
            self.con = MySQLdb.connect(host='localhost', user='root', passwd='931209', db = database_name, charset='utf8')
            logging.info("Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.error("Fail in connecting MySQL.")
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))

        self.result_save_f = open(result_save_directory, "w")
        self.result_save_f.write("========= Report Information =========\n")
        self.result_save_f.write("Report Name:{name}\n".format(name = "Newspaper Metadata Information"))
        self.result_save_f.write("Author:{name}\n".format(name = __author__))
        self.result_save_f.write("Date:{date}\n\n".format( date =
                                                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                        )
                                 )



    def __del__(self):
        logging.info("")
        self.con.close()
        self.result_save_f.close()
        logging.info("Success in quiting MySQL.")
        logging.info("END.")

        self.end = time.clock()
        logging.info("The function run time is : %.03f seconds" % (self.end - self.start))



    def get_table_record_num_list(self, database_name, table_name_list):
        # sub-function
        def get_table_record_num(cursor, sql):
            try:
                cursor.execute(sql)
                record_num = int(cursor.fetchone()[0])
            except MySQLdb.Error, e:
                logging.error("Failed in attaining essay record number.")
                logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
            return record_num

        cursor = self.con.cursor()
        sql_list = map(lambda table_name: """SELECT COUNT(*) FROM %s.%s""" % (database_name, table_name), table_name_list)
        table_record_num_list = map(lambda sql: get_table_record_num(cursor = cursor,
                                                                     sql = sql),
                                    sql_list)
        # four newspaper num.
        shzqb_record_num = table_record_num_list[0]
        zgzqb_record_num = table_record_num_list[1]
        zqrb_record_num = table_record_num_list[2]
        zqsb_record_num = table_record_num_list[3]
        all_newspaper_record_num = sum(table_record_num_list)

        logging.info("上海证券报(shzqb_record_num):%s, %.2f" % (shzqb_record_num, shzqb_record_num/float(all_newspaper_record_num)))
        logging.info("中国证券报(zgzqb_record_num):%s, %.2f" % (zgzqb_record_num, zgzqb_record_num/float(all_newspaper_record_num)))
        logging.info("证券日报(zqrb_record_num):%s, %.2f" % (zqrb_record_num, zqrb_record_num/float(all_newspaper_record_num)))
        logging.info("证券时报(zqsb_record_num):%s, %.2f" % (zqsb_record_num, zqsb_record_num/float(all_newspaper_record_num)))
        logging.info("all_newspaper_record_num:%s" % all_newspaper_record_num)

        # save result
        self.result_save_f.write("========= General Information =========\n")
        self.result_save_f.write("上海证券报(shzqb_record_num):%s, %.2f\n" % (shzqb_record_num, shzqb_record_num/float(all_newspaper_record_num)))
        self.result_save_f.write("中国证券报(zgzqb_record_num):%s, %.2f\n" % (zgzqb_record_num, zgzqb_record_num/float(all_newspaper_record_num)))
        self.result_save_f.write("证券日报(zqrb_record_num):%s, %.2f\n" % (zqrb_record_num, zqrb_record_num/float(all_newspaper_record_num)))
        self.result_save_f.write("证券时报(zqsb_record_num):%s, %.2f\n" % (zqsb_record_num, zqsb_record_num/float(all_newspaper_record_num)))
        self.result_save_f.write("all_newspaper_record_num:%s\n" % all_newspaper_record_num)

        return  table_record_num_list



    def plot_pie_chart(self, table_name_list, table_record_num_list, result_plot_save_directory):
        # plot result
        logging.info("preparing plot pie chart according to the all table's record number.")
        table_name_dict = {"securities_newspaper_shzqb_table": u"Shanghai Securities News",
                           "securities_newspaper_zgzqb_table": u"China Securities Journal",
                           "securities_newspaper_zqrb_table": u"Securities Daily",
                           "securities_newspaper_zqsb_table": u"Securities Times",
                           "all kinds of newspapers": u"all newspapers"}
        # The slices will be ordered and plotted counter-clockwise.
        plt.figure(num = 1, figsize = (10, 6))
        labels = map(lambda key: table_name_dict[key], table_name_list)
        sizes = table_record_num_list
        colors = ["yellowgreen", "gold", "lightskyblue", "lightcoral"]
        explode = (0.1, 0.0, 0.0, 0.0) # only "explode" the 2nd slice (i.e. 'Hogs')
        try:
            plt.pie(sizes, explode = explode, labels = labels, colors = colors,
                    autopct = '%1.1f%%', shadow = True, startangle = 90)
            # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.axis("equal")
            plt.title("The proportion of four kinds of newspapers")
            plt.savefig(result_plot_save_directory, dpi = 78)
            logging.info("pie chart plot successfully.")
        except Exception as e:
            logging.error(e)



    def plot_bar_chart(self, table_name_list, table_record_num_list,
                       title_name, title_comment, xlabel_name, ylabel_name,
                       result_plot_save_directory):
        logging.info("preparing plot bar chart according to the all table's record number.")
        table_name_dict = {"securities_newspaper_shzqb_table": u"Shanghai Se. News",
                           "securities_newspaper_zgzqb_table": u"China Se. Journal",
                           "securities_newspaper_zqrb_table": u"Se. Daily",
                           "securities_newspaper_zqsb_table": u"Se. Times",
                           "all kinds of newspapers": u"4 Kinds of Sec. Newspapers",
                           "max.": u"max.",
                           "min.": u"min.",
                           "range": u"range",
                           "ave.": u"ave.",
                           "med.": u"med.",
                           "most freq.": u"most freq.",
                           "std.": u"std."}
        bar_name_list = map(lambda key: table_name_dict[key], table_name_list)
        x = np.arange(len(table_name_list))

        fig, ax = plt.subplots()
        plt.bar(x, table_record_num_list, color = "yellowgreen")
        plt.xticks(x + 0.5, bar_name_list)
        plt.title(title_name + " " + title_comment)
        plt.xlabel(xlabel_name)
        plt.ylabel(ylabel_name)
        plt.ylim(0.9 * min(table_record_num_list), 1.1 * max(table_record_num_list))
        map(lambda x, y, v:
                plt.text(x + 0.5/2,# + 0.5,
                         y + 1,# - 0.9*min(table_record_num_list),
                         str(v)),
                x, table_record_num_list, table_record_num_list)
        plt.savefig(result_plot_save_directory)


    def get_newspaper_length_information(self, database_name, table_name_list):
        # sub-function
        def get_title_list(cursor, sql):
            try:
                cursor.execute(sql)
                title_2d_tuple = cursor.fetchall()
                title_list = map(lambda title_tuple: title_tuple[0], title_2d_tuple)
            except MySQLdb.Error, e:
                logging.error("Failed in attaining essay record number.")
                logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
            return title_list
        # sub-function
        def get_content_list(cursor, sql):
            try:
                cursor.execute(sql)
                content_2d_tuple = cursor.fetchall()
                content_list = map(lambda title_tuple: title_tuple[0], content_2d_tuple)
            except MySQLdb.Error, e:
                logging.error("Failed in attaining essay record number.")
                logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
            return content_list

        cursor = self.con.cursor()

        # get title information
        sql_list = map(lambda table_name: """SELECT title FROM %s.%s""" % (database_name, table_name), table_name_list)
        title_2d_list = map(lambda sql: get_title_list(cursor = cursor,
                                                       sql = sql),
                            sql_list)
        shzqb_title_list = title_2d_list[0]
        zgzqb_title_list = title_2d_list[1]
        zqrb_title_list = title_2d_list[2]
        zqsb_title_list = title_2d_list[3]
        shzqb_title_len_list = map(len, shzqb_title_list)
        zgzqb_title_len_list = map(len, zgzqb_title_list)
        zqrb_title_len_list = map(len, zqrb_title_list)
        zqsb_title_len_list = map(len, zqsb_title_list)
        title_len_2d_list = [shzqb_title_len_list,
                             zgzqb_title_len_list,
                             zqrb_title_len_list,
                             zqsb_title_len_list]
        """
        logging.info("shzqb_title_len_list:%s" % shzqb_title_len_list)
        logging.info("zgzqb_title_len_list:%s" % zgzqb_title_len_list)
        logging.info("zqrb_title_len_list:%s" % zqrb_title_len_list)
        logging.info("zqsb_title_len_list:%s" % zqsb_title_len_list)
        """

        # get content information
        sql_list = map(lambda table_name: """SELECT content FROM %s.%s""" % (database_name, table_name), table_name_list)
        content_2d_list = map(lambda sql: get_content_list(cursor = cursor,
                                                           sql = sql),
                              sql_list)
        shzqb_content_list = content_2d_list[0]
        zgzqb_content_list = content_2d_list[1]
        zqrb_content_list = content_2d_list[2]
        zqsb_content_list = content_2d_list[3]
        shzqb_content_len_list = map(len, shzqb_content_list)
        zgzqb_content_len_list = map(len, zgzqb_content_list)
        zqrb_content_len_list = map(len, zqrb_content_list)
        zqsb_content_len_list = map(len, zqsb_content_list)
        content_len_2d_list = [shzqb_content_len_list,
                               zgzqb_content_len_list,
                               zqrb_content_len_list,
                               zqsb_content_len_list]
        """
        logging.info("shzqb_content_len_list:%s" % shzqb_content_len_list)
        logging.info("zgzqb_content_len_list:%s" % zgzqb_content_len_list)
        logging.info("zqrb_content_len_list:%s" % zqrb_content_len_list)
        logging.info("zqsb_content_len_list:%s" % zqsb_content_len_list)
        """
        return title_len_2d_list, content_len_2d_list



    def compute_median_in_list(self, demo_list):
        element_num = len(demo_list)
        demo_list = sorted(demo_list, reverse = False)
        if element_num % 2 == 0:
            median_value = (demo_list[element_num/2] + demo_list[element_num/2 + 1]) / 2
        else:
            median_value = demo_list[(element_num+1) / 2]
        return median_value



    def generate_list_key_value_dict(self, demo_list):
        demo_dict = dict()
        key_set = set(sorted(demo_list, reverse = True))
        for element in iter(key_set):
            demo_dict[element] = 0
        for element in iter(demo_list):
            demo_dict[element] += 1
        return demo_dict



    def compute_most_frequent_element_in_list(self, demo_list):
        demo_dict = self.generate_list_key_value_dict(demo_list = demo_list)
        key_value_tuple_list = demo_dict.items()
        sorted_key_value_tuple_list = sorted(key_value_tuple_list,
                                             key = lambda key_value_tuple: key_value_tuple[1],
                                             reverse = True)
        most_frequent_element = sorted_key_value_tuple_list[0][0]
        return most_frequent_element



    def compute_average_in_list(self, demo_list):
        return round(np.array(demo_list).mean(), 2)



    def compute_maximum_in_list(self, demo_list):
        return np.array(demo_list).max()



    def compute_minimal_in_list(self, demo_list):
        return np.array(demo_list).min()



    def compute_standard_deviation_in_list(self, demo_list):
        return round(np.array(demo_list).std(), 2)



    def compute_range_in_list(self, demo_list):
        return np.array(demo_list).max() - np.array(demo_list).min()



    def compute_basic_statistic_information(self, list_name, list_comment, demo_list, result_plot_save_base_dir):
        num = len(demo_list)
        maximum = self.compute_maximum_in_list(demo_list = demo_list)
        minimum = self.compute_minimal_in_list(demo_list = demo_list)
        min_max_range = self.compute_range_in_list(demo_list = demo_list)
        average = self.compute_average_in_list(demo_list = demo_list)
        median = self.compute_median_in_list(demo_list = demo_list)
        most_frequent_element = self.compute_most_frequent_element_in_list(demo_list = demo_list)
        standard_deviation = self.compute_standard_deviation_in_list(demo_list = demo_list)

        table_name_dict = {"securities_newspaper_shzqb_table": "上海证券报",
                           "securities_newspaper_zgzqb_table": "中国证券报",
                           "securities_newspaper_zqrb_table": "证券日报",
                           "securities_newspaper_zqsb_table": "证券时报",
                           "all kinds of newspapers": "all newspapers"}
        table_plot_name_dict = {"securities_newspaper_shzqb_table": u"Shanghai Se. News",
                           "securities_newspaper_zgzqb_table": u"China Se. Journal",
                           "securities_newspaper_zqrb_table": u"Se. Daily",
                           "securities_newspaper_zqsb_table": u"Se. Times",
                           "all kinds of newspapers": u"4 Kinds of Newspapers"}

        table_name_list = [u"max.", u"min.", u"range", u"ave.", u"med.", u"most freq.", u"std."]
        table_record_num_list = [maximum, minimum, min_max_range, average, median, most_frequent_element, standard_deviation]
        file_name = "_".join([table_plot_name_dict[list_name], list_comment])
        self.plot_bar_chart(table_name_list = table_name_list,
                            table_record_num_list = table_record_num_list,
                            title_name = table_plot_name_dict[list_name],
                            title_comment = list_comment,
                            xlabel_name = "statistic values",
                            ylabel_name = "length(words num.)",
                            result_plot_save_directory = os.path.join(result_plot_save_base_dir, file_name + ".png"))


        logging.info("Basic statistic information of {name} {comment}".
                     format(name = table_name_dict[list_name],
                            comment = list_comment))
        logging.info("{comment} num.:{number}".
                     format(comment = list_comment,
                            number = num))
        logging.info("{comment} length maximum:{max}".
                     format(comment = list_comment,
                            max = maximum))
        logging.info("{comment} length minimum:{min}".
                     format(comment = list_comment,
                            min = minimum))
        logging.info("{comment} length range:{range}".
                     format(comment = list_comment,
                            range = min_max_range))
        logging.info("{comment} length average:{ave}".
                     format(comment = list_comment,
                            ave = average))
        logging.info("{comment} length median:{med}".
                     format(comment = list_comment,
                            med = median))
        logging.info("{comment} most frequent length:{most_fre}".
                     format(comment = list_comment,
                            most_fre = most_frequent_element))
        logging.info("{comment} length standard deviation:{std}".
                     format(comment = list_comment,
                            std = standard_deviation))
        self.result_save_f.write("\n========= Detailed Information =========\n")
        self.result_save_f.write("Basic statistic information of {name} {comment}\n".
                                 format(name = table_name_dict[list_name],
                                        comment = list_comment))
        self.result_save_f.write("{comment} num.:{number}\n".
                                 format(comment = list_comment,
                                        number = num))
        self.result_save_f.write("{comment} length maximum:{max}\n".
                                 format(comment = list_comment,
                                        max = maximum))
        self.result_save_f.write("{comment} length minimum:{min}\n".
                                 format(comment = list_comment,
                                        min = minimum))
        self.result_save_f.write("{comment} length range:{range}\n".
                                 format(comment = list_comment,
                                        range = min_max_range))
        self.result_save_f.write("{comment} length average:{ave}\n".
                                 format(comment = list_comment,
                                        ave = average))
        self.result_save_f.write("{comment} length median:{med}\n".
                                 format(comment = list_comment,
                                        med = median))
        self.result_save_f.write("{comment} most frequent length:{most_fre}\n".
                                 format(comment = list_comment,
                                        most_fre = most_frequent_element))
        self.result_save_f.write("{comment} length standard deviation:{std}\n".
                                 format(comment = list_comment,
                                        std = standard_deviation))

################################### PART3 CLASS TEST ##################################
"""
# Initial parameters and construct variables.
database_name = "essayDB"
table_name_list = ["securities_newspaper_shzqb_table",
                   "securities_newspaper_zgzqb_table",
                   "securities_newspaper_zqrb_table",
                   "securities_newspaper_zqsb_table"]
result_save_directory = "./data/newspaper_metadata.txt"

MetaData = ComputeNewspaperMetaData(database_name = database_name)
table_record_num_list = MetaData.get_table_record_num_list(database_name = database_name,
                                                           table_name_list = table_name_list)
title_len_2d_list, content_len_2d_list = MetaData.get_newspaper_length_information(database_name = database_name,
                                                                           table_name_list = table_name_list)



map(lambda list_name, title_list:
    MetaData.compute_basic_statistic_information(list_name = list_name,
                                                 list_comment = "title",
                                                 demo_list = title_list),
    table_name_list, title_len_2d_list)
map(lambda list_name, content_list:
    MetaData.compute_basic_statistic_information(list_name = list_name,
                                                 list_comment = "content",
                                                 demo_list = content_list),
    table_name_list, content_len_2d_list)



title_len_list = flatten(title_len_2d_list)
content_len_list = flatten(content_len_2d_list)
MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                             list_comment = "title",
                                             demo_list = title_len_list)
MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                             list_comment = "content",
                                             demo_list = content_len_list)
title_and_content_len_list = map(lambda title_len, content_len:
                                 title_len + content_len,
                                 title_len_list, content_len_list)
MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                             list_comment = "title and content",
                                             demo_list = title_and_content_len_list)
"""