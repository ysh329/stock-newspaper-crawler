################################### PART0 DESCRIPTION #################################
# -*- coding: utf-8 -*-
# !/usr/bin/python

# Filename: class_create_databases.py
# Description: Create database and tables CLASS.
#              table structure according to data
#              source from "四大证券报精华_财经_新浪网,
#              http://finance.sina.com.cn/focus/zqbjh/"
#
#              Four Securities newspaper:
#              [1]China Securities Journal(zgzqb)
#              [2]Securities Daily(zqrb)
#              [3]Shanghai Securities News(shzqb)
#              [4]Securities Times(zqsb)

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-22
# Last: 2015-7-22 13:16:06
################################### PART1 IMPORT ######################################

import MySQLdb

################################### PART2 CLASS && FUNCTION ###########################
__author__ = 'yuens'


class CreateDatabaseClass(object):
    def __init__(self):
        try:
            self.con = MySQLdb.connect(host='localhost', user='root', passwd='931209', charset='utf8')
            print 'Success in connecting MySQL.'
        except MySQLdb.Error, e:
            print 'Fail in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

    def __del__(self):
        self.con.close()
        print 'Success in quiting MySQL.'

    def dbrollback(self):
        self.con.rollback()

    def dbcommit(self):
        self.con.commit()

    # Create database
    def create_database(self, database_name):
        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8', 'SELECT VERSION()', 'CREATE DATABASE %s' % database_name, 'USE %s' % database_name]
        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
                if sql_idx == 1:
                    result = cursor.fetchall()[0]
                    mysql_version = result[0]
                    print "MySQL VERSION: %s" % mysql_version
            self.dbcommit()
            print 'Success in creating database %s.' % database_name
        except MySQLdb.Error, e:
            self.dbrollback()
            print 'Fail in creating database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

    # create 4 tables
    #[1]'securities_newspaper_zqzqb_table', [2]'securities_newspaper_zqrb_table',
    #[3]'securities_newspaper_shzqb_table', [4]'securities_newspaper_zqsb_table']
    def create_table(self, database_name):
        self.con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '931209', db = database_name, charset = 'UTF8')
        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8']

        # Define table structure
        # Construct data table #1: securities_newspaper_zgzqb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zgzqb_table(
                                zgzqb_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                zgzqb_title TEXT NOT NULL,
                                zgzqb_content TEXT NOT NULL,
                                zgzqb_date VARCHAR(30) NOT NULL DEFAULT '',
                                zgzqb_link TEXT NOT NULL)""")
        sqls.append("CREATE INDEX zgzqb_id_idx ON securities_newspaper_zgzqb_table(zgzqb_id)")

        # Construct data table #2: securities_newspaper_zqrb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zqrb_table(
                                zqrb_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                zqrb_title TEXT NOT NULL,
                                zqrb_content TEXT NOT NULL,
                                zqrb_date VARCHAR(30) NOT NULL DEFAULT '',
                                zqrb_link TEXT NOT NULL)""")
        sqls.append("CREATE INDEX zqrb_id_idx ON securities_newspaper_zqrb_table(zqrb_id)")

        # Construct data table #3: securities_newspaper_shzqb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_shzqb_table(
                                shzqb_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                shzqb_title TEXT NOT NULL,
                                shzqb_content TEXT NOT NULL,
                                shzqb_date VARCHAR(30) NOT NULL DEFAULT '',
                                shzqb_link TEXT NOT NULL)""")
        sqls.append("CREATE INDEX shzqb_id_idx ON securities_newspaper_shzqb_table(shzqb_id)")

        # Construct data table #4: securities_newspaper_zqsb_table
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS securities_newspaper_zqsb_table(
                                zqsb_id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                zqsb_title TEXT NOT NULL,
                                zqsb_content TEXT NOT NULL,
                                zqsb_date VARCHAR(30) NOT NULL DEFAULT '',
                                zqsb_link TEXT NOT NULL)""")
        sqls.append("CREATE INDEX zqsb_id_idx ON securities_newspaper_zqsb_table(zqsb_id)")
        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
            self.dbcommit()
            print 'Success in creating 4 tables.'
        except MySQLdb.Error, e:
            self.dbrollback()
            print 'Fail in creating 4 table.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

################################### PART3 CLASS TEST ##################################
# initial parameters
database_name = "essayDB"

a = CreateDatabaseClass()
a.create_database(database_name)
a.create_table(database_name)