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
    '''
    Crawler = CrawlSecuritiesNewspapers()
    all_essays_links_list = Crawler.get_all_pages_essays_links_list()
    print "all_essays_links_list:", all_essays_links_list
    print "len(all_essays_links_list):", len(all_essays_links_list)
    result = map(lambda essay_link: Crawler.get_cur_essay_page_information_tuple(cur_page_link = essay_link))
    print "len(result):", len(result)
    print "result[0]:", result[0]
    print "type(result[0]):", type(result[0])
    '''

################################ PART4 EXECUTE ##################################
if __name__ == "__main__":
    main()