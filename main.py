# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: main.py
# Description:

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-24 10:25:48
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
from myclass.class_create_databases import *
from myclass.class_crawl_securities_newspaper import *

################################ PART3 MAIN #####################################
def main():
    database_name = "essayDB"
    CrawlerDB = CreateDatabaseClass()
    CrawlerDB.create_database(database_name)
    CrawlerDB.create_table(database_name)

    initial_link = "http://money.163.com/special/0025262F/sidbk.html"



################################ PART4 EXECUTE ##################################
if __name__ == "__main__":
    main()

