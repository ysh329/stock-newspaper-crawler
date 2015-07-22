# -*- coding: utf-8 -*-
# !/usr/bin/python

# Filename: class_create_databases.py
# Description: 导入char.txt文件到MySQL数据库。
#              导入后查重，并若有重复数据则删除，
#              并重新开始计算id值。

# Author: Shuai Yuan
# E-mail: ysh329@sina.com

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
            print 'Failure in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

    def __del__(self):
        self.con.close()
        print 'Success in quiting MySQL.'

    def dbrollback(self):
        self.con.rollback()

    def dbcommit(self):
        self.con.commit()

    def create_database(self):
        cursor = self.con.cursor()
        sqls = ["alter database charDB default character set 'utf8'"]
        try:
            for sql_idx in range(len(sqls)):
                print sqls[sql_idx]
        except MySQLdb.Error, e:
            print 'Failure in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

    def create_table(self):
        try:
            pass
        except:
            pass

a = CreateDatabasesClass()
a.create_database()