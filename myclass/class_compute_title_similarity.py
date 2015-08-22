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
        def remove_stopword_in_title(title, stopword_list):
            stopword_removed_title = filter(lambda char: char not in stopword_list, title)
            return title

        stopword_list = [" ", ",", ".", "/", "<", ">", "?",\
                        ";", ":", "'", '"', \
                        "[", "{", "]", "}", "|", "\\",\
                        "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=",\
                        "《", "》", "，", "。", "？", "、", "“", "：", "”", "’", "；", "：", "、", "】",\
                        "【", "~", "！", "（", "￥", "）",\
                        " ",\
                        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",\
                        "一", "不", "与", "且", "为", "乃", "么", "之", "呜", "乌", "乎", "呼",\
                        "所", "也", "了", "什", "从", "以", "们", "但", "何", "倘", "假", "兮",\
                        "其", "再", "别", "即", "及", "另", "可", "吗", "吧", "嗒", "吱", "呀",\
                        "呃", "呕", "呗", "呢", "呵", "呸", "哧", "咋", "咚", "咦", "咳", "哇",\
                        "哈", "哉", "哎", "哟", "哗", "哦", "哩", "哪", "哼", "唷", "唉", "啊",\
                        "啐", "啥", "啦", "啪", "喏", "喔", "唷", "嗡", "嗯", "嗳", "嘎", "嘘",\
                        "嘛", "嘻", "嘿", "因", "如", "宁", "就", "怎", "此", "某", "每", "这",\
                        "那", "兮", "嗳", "嗬", "的"]
        stopword_list = map(lambda stopword: unicode(stopword, "utf8"), stopword_list)
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



        word_string = "".join(title_list)
        word_set = set(word_string)
        word_set_len_xrange = xrange(len(word_set))
        word_map_tuple_list = map(lambda id, word: (id, word), word_set_len_xrange, word_set)

        logging.info("len(word_string):%s" % len(word_string))
        logging.info("len(word_set):%s" % len(word_set))
        logging.info("len(word_set_len_xrange):%s" % len(word_set_len_xrange))
        return word_map_tuple_list



    def title_list_2_id_list(self, title_list, word_map_tuple_list):
        # sub-function
        def title_2_id_list(title, word_map_tuple_list):
            title_vector = map(lambda char: char_2_id(char = char, word_map_tuple_list = word_map_tuple_list), title)
            return title_vector
        # sub-function
        def char_2_id(char, word_map_tuple_list):
            id = filter(lambda (id, word): char == word, word_map_tuple_list)[0][0]
            return id

        title_vector = map(lambda title: title_2_id_list(title = title, word_map_tuple_list = word_map_tuple_list), title_list)
        return title_vector



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


    def compute_title_similarity(self, id_title_tuple_2d_list):
        # sub-function
        def compute_cosine(t1, t2):
            t1_word = map(lambda record: record[0], t1)
            t2_word = map(lambda record: record[0], t2)

            return cosine_similarity

        similarity_matrix = []
        for t1_idx in xrange(len(id_title_tuple_2d_list)):
            t1_title_tuple_list = id_title_tuple_2d_list[t1_idx]
            for t2_idx in xrange(len(id_title_tuple_2d_list)):
                t2_title_tuple_list = id_title_tuple_2d_list[t2_idx]
                similarity_matrix.append((t1_title_tuple_list, t2_title_tuple_list))
        similarity_matrix = map(lambda record: (record[0], record[1], compute_cosine(t1 = record[0], t2=record[1])), similarity_matrix)
        return similarity_matrix


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

id_title_list = Computer.title_list_2_id_list(title_list = stopword_removed_title_list, word_map_tuple_list = word_map_tuple_list)
logging.info("id_title_vector[0:10]:%s" % id_title_list[0:10])
logging.info("id_title_vector[0][0]:%s" % id_title_list[0][0])

id_title_tuple_2d_list = Computer.id_title_list_2_id_title_tuple_2d_list(id_title_list = id_title_list)
logging.info("id_title_tuple_2d_list[0]:%s" % str(id_title_tuple_2d_list[0]))
logging.info("id_title_tuple_2d_list[0:5]:%s" % str(id_title_tuple_2d_list[0:5]))
logging.info("id_title_tuple_2d_list[0][0]:%s" % str(id_title_tuple_2d_list[0][0]))

similarity_matrix = Computer.compute_title_similarity(id_title_tuple_2d_list = id_title_tuple_2d_list)