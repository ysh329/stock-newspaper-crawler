# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_create_databases.py
# Description: Create database and tables CLASS.
#              database_name="essayDB"
#              4 tables' name:
#              table structure according to data
#              source from 四大证券报头条 - 中国资本证券网
#              http://www.ccstock.cn/meiribidu/sidazhengquanbaotoutiao/
#
    #[1]'securities_newspaper_zqzqb_table', [2]'securities_newspaper_zqrb_table',
    #[3]'securities_newspaper_shzqb_table', [4]'securities_newspaper_zqsb_table']
#              Four Securities newspaper:
#              [1]China Securities Journal(zgzqb)
#              [2]Securities Daily(zqrb)
#              [3]Shanghai Securities News(shzqb)
#              [4]Securities Times(zqsb)

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-22
# Last: 2015-7-22 17:03:18
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import logging
import MySQLdb
import time
################################### PART2 CLASS && FUNCTION ###########################
class CreateDatabaseClass(object):
    def __init__(self):
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
            self.con = MySQLdb.connect(host='localhost', user='root', passwd='931209', charset='utf8')
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



    def dbrollback(self):
        logging.info("[dbrollback]")
        self.con.rollback()



    def dbcommit(self):
        logging.info("")
        self.con.commit()



    # Create database
    def create_database(self, database_name):
        logging.info("database name:%s" % database_name)

        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8', 'SELECT VERSION()', 'CREATE DATABASE %s' % database_name]
        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
                if sql_idx == 1:
                    result = cursor.fetchall()[0]
                    mysql_version = result[0]
                    logging.info("MySQL VERSION: %s" % mysql_version)
            self.dbcommit()
            logging.info("Success in creating database %s." % database_name)
        except MySQLdb.Error, e:
            self.dbrollback()
            logging.error("Fail in creating database %s." % database_name)
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()



    # create 4 tables
    #[1]'securities_newspaper_zqzqb_table', [2]'securities_newspaper_zqrb_table',
    #[3]'securities_newspaper_shzqb_table', [4]'securities_newspaper_zqsb_table']
    def create_table(self, database_name):
        logging.info("")

        cursor = self.con.cursor()
        sqls = ['USE %s' % database_name, 'SET NAMES UTF8']

        # Define table structure
        # Construct data table #1: securities_newspaper_zgzqb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zgzqb_table(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                title CHAR(100),
                                content TEXT NOT NULL,
                                date VARCHAR(30) NOT NULL DEFAULT '',
                                page_link TEXT NOT NULL,
                                essay_link TEXT NOT NULL,
                                UNIQUE (title))""")
        sqls.append("CREATE INDEX id_idx ON securities_newspaper_zgzqb_table(id)")

        # Construct data table #2: securities_newspaper_zqrb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zqrb_table(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                title CHAR(100),
                                content TEXT NOT NULL,
                                date VARCHAR(30) NOT NULL DEFAULT '',
                                page_link TEXT NOT NULL,
                                essay_link TEXT NOT NULL,
                                UNIQUE (title))""")
        sqls.append("CREATE INDEX id_idx ON securities_newspaper_zqrb_table(id)")

        # Construct data table #3: securities_newspaper_shzqb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_shzqb_table(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                title CHAR(100),
                                content TEXT NOT NULL,
                                date VARCHAR(30) NOT NULL DEFAULT '',
                                page_link TEXT NOT NULL,
                                essay_link TEXT NOT NULL,
                                UNIQUE (title))""")
        sqls.append("CREATE INDEX id_idx ON securities_newspaper_shzqb_table(id)")

        # Construct data table #4: securities_newspaper_zqsb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zqsb_table(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                title CHAR(100),
                                content TEXT NOT NULL,
                                date VARCHAR(30) NOT NULL DEFAULT '',
                                page_link TEXT NOT NULL,
                                essay_link TEXT NOT NULL,
                                UNIQUE (title))""")
        sqls.append("CREATE INDEX id_idx ON securities_newspaper_zqsb_table(id)")
        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
            self.dbcommit()
            logging.info("Success in creating 4 tables.")
        except MySQLdb.Error, e:
            self.dbrollback()
            logging.error("Fail in creating 4 table.")
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()



    def insert_title_content_date_link_list_2_db(self, table_name, title_list, content_list, date, page_link, link_list):
        logging.info("table_name:%s,date:%s,page_link:%s" % (table_name, date, page_link))

        cursor = self.con.cursor()
        sqls = ["SET NAMES UTF8"]

        for list_idx in range(len(content_list)):
            title = title_list[list_idx]
            content = content_list[list_idx]
            date = date
            page_link = page_link
            essay_link = link_list[list_idx]
            sqls.append("""INSERT INTO %s(title, content, date, page_link, essay_link) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (table_name, title, content, date, page_link, essay_link))

        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
            self.dbcommit()
        except MySQLdb.Error, e:
            self.dbrollback()
            logging.error("MySQL Error %d: %s." % (e.args[0], e.args[1]))
        finally:
            cursor.close()

################################### PART3 CLASS TEST ##################################
# initial parameters
'''
database_name = "essayDB"

a = CreateDatabaseClass()
a.create_database(database_name)
a.create_table(database_name)

a.insert_title_content_date_link_list_2_db(table_name="securities_newspaper_shzqb_table", title_list = ['a', 'b', 'c'], \
                                           content_list=['aa', 'bb', 'cc'], date = "now", page_link = "www.page_link.com", link_list = ["www"] * 3)
'''