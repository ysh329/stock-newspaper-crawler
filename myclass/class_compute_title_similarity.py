# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_compute_title_similarity.py
# Description:
#


# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-8-21
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import logging
import MySQLdb
import time
import os
import math
import numpy as np
from compiler.ast import flatten
################################### PART2 CLASS && FUNCTION ###########################
class ComputeTitleSimilarity(object):
    def __init__(self, database_name):
        self.start = time.clock()

        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(levelname)5s %(filename)19s[line:%(lineno)3d] %(funcName)s %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  filename = '../main.log',
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

    def __del__(self):
        logging.info("")
        self.con.close()
        logging.info("Success in quiting MySQL.")
        logging.info("END.")

        self.end = time.clock()
        logging.info("The function run time is : %.03f seconds" % (self.end - self.start))



    def count_essay_num(self, database_name):
        # sub function
        def count_record(cursor, database_name, table_name):
            try:
                cursor.execute("""SELECT COUNT(*) FROM %s.%s""" % (database_name, table_name))
                return  int(cursor.fetchone()[0])
            except:
                logging.error("Failed in selecting record num. of table %s in database %s" % (table_name, database_name))
                return "None"
        # sub function
        def print_name_num(record):
            logging.info("table name:%s, record num: %s" % (record[0], record[1]))

    #def count_essay_num(self, database_name):
        try:
            con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            cursor = con.cursor()
            logging.info("Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.info("Fail in connecting MySQL.")
            logging.info("MySQL Error %d: %s." % (e.args[0], e.args[1]))

        try:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            table_name_list = map(lambda essay_tuple: essay_tuple[0],cursor.fetchall())
            table_record_num_list = map(lambda table_name: count_record(cursor = cursor, database_name = database_name, table_name = table_name), table_name_list)
        except MySQLdb.Error, e:
            logging.error("Failed in counting tables in database %s." % database_name)
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()

        table_tuple_list = map(lambda name, num: (name, num), table_name_list, table_record_num_list)
        map(print_name_num, table_tuple_list)
        logging.info("table sum num.: %s, sum record num:%s" % (len(table_name_list), sum(table_record_num_list)))
        return table_name_list



    def get_title_list_in_db(self, database_name, table_name_list):
        all_essay_title_2d_list = map(self.get_title_list, table_name_list)
        all_essay_title_list = flatten(all_essay_title_2d_list)
        return all_essay_title_list



    def get_title_list(self, table_name):
        cursor = self.con.cursor()
        sql = """SELECT title FROM %s""" % table_name
        try:
            cursor.execute(sql)
            title_list = map(lambda title: title[0], cursor.fetchall())
        except MySQLdb.Error, e:
            logging.error("Failed in attaining essay's titles in table %s." % table_name)
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()
        return title_list



    def remove_stopword_in_title_list(self, title_list):
        # sub-function
        def filter_and_unicode(ch):
            if ch == '\n':
                ch = " "
            return unicode(ch, "utf8").replace("\n", "")

        # sub-function
        def remove_stopword_in_title(title, stopword_list):
            stopword_removed_title = filter(lambda char: char not in stopword_list, title)
            return title

        file_name = "stopword.txt"
        file_path = "../data/"
        file_path_name = os.path.join(file_path, file_name)
        try:
            f = open(file_path_name)
            lines = f.readlines()
            stopword_list = map(filter_and_unicode, lines)
        except Exception as e:
            logging.error(e)
        finally:
            f.close()

        logging.info("type(stopword_list):%s" % type(stopword_list))
        logging.info("len(stopword_list):%s" % len(stopword_list))
        logging.info("type(stopword_list[0]):%s" % type(stopword_list[0]))
        logging.info("stopword_list[0:10]:%s" % stopword_list[0:10])

        stopword_removed_title_list = map(lambda title: remove_stopword_in_title(title = title, stopword_list = stopword_list), title_list)
        logging.info("type(stopword_removed_title_list):%s" % type(stopword_removed_title_list))
        logging.info("len(stopword_removed_title_list):%s" % len(stopword_removed_title_list))
        logging.info("type(stopword_removed_title_list[0]):%s" % type(stopword_removed_title_list[0]))
        logging.info("stopword_removed_title_list[0:10]:%s" % stopword_removed_title_list[0:10])

        return stopword_removed_title_list



    def get_word_map_tuple_list(self, title_list):
        # sub-function
        def save_word_map(word_map_tuple_list):
            try: os.mkdir("data")
            except Exception as e: logging.info(e)

            word_map_file_name = "../data/wordmap.txt"
            f = open(word_map_file_name, "w")
            for idx in xrange(len(word_map_tuple_list)):
                word_map_tuple = word_map_tuple_list[idx]
                id = str(word_map_tuple[0])
                word = word_map_tuple[1].encode("utf8")
                f.write(id + " " + word + "\n")
            f.close()

        word_string = "".join(title_list)
        word_set = set(word_string)
        word_set_len_xrange = xrange(len(word_set))
        word_map_tuple_list = map(lambda id, word: (id, word), word_set_len_xrange, word_set)
        save_word_map(word_map_tuple_list = word_map_tuple_list)

        logging.info("len(word_string):%s" % len(word_string))
        logging.info("len(word_set):%s" % len(word_set))
        logging.info("len(word_set_len_xrange):%s" % len(word_set_len_xrange))
        return word_map_tuple_list



    def title_list_2_id_list(self, title_list, word_map_tuple_list):
        # sub-function
        def title_2_id_list(title, word_map_tuple_list):
            title_id_vector = map(lambda char: char_2_id(char = char, word_map_tuple_list = word_map_tuple_list), title)
            return title_id_vector
        # sub-function
        def save_title_and_id_2_file(title_list, title_id_2d_list):
            title_list = map(lambda title: title.encode("utf8"), title_list)
            #id_2d_list = map(lambda title_id_list: map(lambda id: id, title_id_list), title_id_2d_list)
            id_2d_list = title_id_2d_list
            f = open("../data/title_id.txt", "w")
            count = xrange(len(title_list))
            map(lambda title, id_list, counter: f.write(str(counter) + " " + title + " " + str(id_list) + "\n"), title_list, id_2d_list, count)
            f.close()
        # sub-function
        def char_2_id(char, word_map_tuple_list):
            id = filter(lambda (id, word): char == word, word_map_tuple_list)[0][0]
            return id

        title_and_id_3d_list = map(lambda title: title_2_id_list(title = title, word_map_tuple_list = word_map_tuple_list), title_list)
        save_title_and_id_2_file(title_list = title_list, title_id_2d_list = title_and_id_3d_list)
        return title_and_id_3d_list



    def id_title_list_2_id_title_tuple_2d_list(self, id_title_list):
        # sub-function
        def title_2_word_id_frequency_statistic_tuple(id_title):
            id_frequency_tuple_list = map(lambda word_id: (word_id, 1), id_title)
            id_frequency_tuple_list = reduceByKey(id_frequency_tuple_list)
            return id_frequency_tuple_list
        # sub-function
        def reduceByKey(tuple_list_obj):
            kv_dict = {}
            key_set = set(map(lambda record: record[0], tuple_list_obj))
            for key in key_set: kv_dict[key] = 0
            for tup in iter(tuple_list_obj): kv_dict[tup[0]] += 1
            tuple_list = map(lambda key, value: (key, value), kv_dict.keys(), kv_dict.values())
            return tuple_list

        id_title_tuple_2d_list = map(lambda title: title_2_word_id_frequency_statistic_tuple(title), id_title_list)
        return id_title_tuple_2d_list



    def compute_title_similarity(self, id_title_2d_list, id_title_tuple_2d_list):
        # sub-function
        def compute_cosine(t1, t2):
            #print "t1:%s" % t1
            #print "t2:%s" % t2
            t1_word_list = map(lambda record: record[0], t1)
            t2_word_list = map(lambda record: record[0], t2)
            #print "t1_word_list:", t1_word_list
            #print "t2_word_list:", t2_word_list
            common_word_list = list(set(t1_word_list) & set(t2_word_list))
            all_word_list = list(set(t1_word_list) | set(t2_word_list))
            #print "common_word_list:%s" % common_word_list
            #print "len(common_word_list):%s" % len(common_word_list)
            if common_word_list == 0:
                #print "len(common_word_list):" % len(common_word_list)
                cosine_similarity = 0
            else:
                numerator = 0
                denominator = 1
                t1_common_word_vector_list = []
                t2_common_word_vector_list = []
                for idx in xrange(len(common_word_list)):
                    common_word = common_word_list[idx]
                    t1_common_word_frequency = filter(lambda record: record[0] == common_word, t1)[0][1]
                    t2_common_word_frequency = filter(lambda record: record[0] == common_word, t2)[0][1]
                    #print "t1_common_word_frequency:%s" % t1_common_word_frequency
                    #print "t2_common_word_frequency:%s" % t2_common_word_frequency
                    t1_common_word_vector_list.append(t1_common_word_frequency)
                    t2_common_word_vector_list.append(t2_common_word_frequency)
                t1_common_word_vector_array = np.array(t1_common_word_vector_list)
                t2_common_word_vector_array = np.array(t2_common_word_vector_list)

                t1_all_word_vector_list = []
                t2_all_word_vector_list = []
                for idx in xrange(len(all_word_list)):
                    general_word = all_word_list[idx]
                    try: t1_all_word_frequency = filter(lambda record: record[0] == general_word, t1)[0][1]
                    except: t1_all_word_frequency = 0
                    try: t2_all_word_frequency = filter(lambda record: record[0] == general_word, t2)[0][1]
                    except: t2_all_word_frequency = 0
                    #print "t1_all_word_frequency:%s" % t1_all_word_frequency
                    #print "t2_all_word_frequency:%s" % t2_all_word_frequency
                    t1_all_word_vector_list.append(t1_all_word_frequency)
                    t2_all_word_vector_list.append(t2_all_word_frequency)
                t1_all_word_vector_array = np.array(t1_all_word_vector_list)
                t2_all_word_vector_array = np.array(t2_all_word_vector_list)

                numerator = sum(t1_common_word_vector_array.__mul__(t2_common_word_vector_array))
                denominator = math.sqrt(sum(t1_all_word_vector_array.__mul__(t1_all_word_vector_array)) * sum(t2_all_word_vector_array.__mul__(t2_all_word_vector_array)))
                cosine_similarity = numerator / float(denominator)
                #print "cosine_similarity:%s" % cosine_similarity
            return cosine_similarity

        similarity_matrix = []
        for t1_idx in xrange(len(id_title_tuple_2d_list)):
            t1_title_tuple_list = id_title_tuple_2d_list[t1_idx]
            for t2_idx in xrange(len(id_title_tuple_2d_list)):
                t2_title_tuple_list = id_title_tuple_2d_list[t2_idx]
                if t1_title_tuple_list == t2_title_tuple_list: break
                similarity_matrix.append((t1_title_tuple_list, t2_title_tuple_list))

        logging.info("len(similarity_matrix):%s" % len(similarity_matrix))
        similarity_trigram_tuple_list = map(lambda record: (record[0], record[1], compute_cosine(t1 = record[0], t2=record[1])), similarity_matrix)
        return similarity_trigram_tuple_list


################################### PART3 CLASS TEST ##################################
# initial parameters
database_name = "essayDB"

Computer = ComputeTitleSimilarity(database_name = database_name)
table_name_list = Computer.count_essay_num(database_name = database_name)
logging.info("table_name_list:%s" % table_name_list)

title_list = Computer.get_title_list_in_db(database_name = database_name,table_name_list = table_name_list)
logging.info("title_list[1:4]:%s" % str(title_list[1:4]))
logging.info("title_list[0]:%s" % title_list[0])
logging.info("type(title_list[0]):%s" % type(title_list[0]))
logging.info("len(title_list):%s" % len(title_list))
logging.info("type(title_list):%s" % type(title_list))

word_map_tuple_list = Computer.get_word_map_tuple_list(title_list = title_list)
logging.info("word_map_tuple_list[:10]: %s" % word_map_tuple_list[:10])

stopword_removed_title_list = Computer.remove_stopword_in_title_list(title_list = title_list)

id_title_2d_list = Computer.title_list_2_id_list(title_list = stopword_removed_title_list, word_map_tuple_list = word_map_tuple_list)
logging.info("id_title_2d_list[0:10]:%s" % id_title_2d_list[0:10])
logging.info("id_title_2d_list[0][0]:%s" % id_title_2d_list[0][0])

id_title_tuple_2d_list = Computer.id_title_list_2_id_title_tuple_2d_list(id_title_list = id_title_2d_list)
logging.info("id_title_tuple_2d_list[0]:%s" % str(id_title_tuple_2d_list[0]))
logging.info("id_title_tuple_2d_list[0:5]:%s" % str(id_title_tuple_2d_list[0:5]))
logging.info("id_title_tuple_2d_list[0][0]:%s" % str(id_title_tuple_2d_list[0][0]))

similarity_trigram_tuple_list = Computer.compute_title_similarity(id_title_2d_list = id_title_2d_list, id_title_tuple_2d_list = id_title_tuple_2d_list)
logging.info("len(similarity_trigram_tuple_list):%s" % len(similarity_trigram_tuple_list))