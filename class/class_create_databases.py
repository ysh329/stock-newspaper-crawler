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
################################### PART1 IMPORT ################################

import MySQLdb

################################### PART2 CLASS && FUNCTION ###########################
__author__ = 'yuens'


class CreateDatabasesClass(object):
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

    def create_newspaper_table(self, table_name):
        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8', "ALTER DATABASE charDB DEFAULT CHARACTER SET 'utf8'"]

        # Define table structure
        sqls.append("""CREATE TABLE IF NOT EXIST

        """ % table_name)


        try:
            for sql_idx in range(len(sqls)):
                sql = sqls[sql_idx]
                cursor.execute(sql)
            self.dbcommit()
            print 'Success in creating table %s.' % table_name
        except MySQLdb.Error, e:
            self.dbrollback()
            print 'Fail in creating table %s.' % table_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

a = CreateDatabasesClass()
a.create_database(database_name='essayDB')
a.create_newspaper_table(table_name='securities_newspaper_zgzqb_table')
a.create_newspaper_table(table_name='securities_newspaper_zqrb_table')
a.create_newspaper_table(table_name='securities_newspaper_zgzqb_table')
a.create_newspaper_table(table_name='securities_newspaper_zgzqb_table')
