# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_crawl_securities_newspaper.py
# Description: Crawl data from "四大证券报精华_财经_新浪网,
#              http://finance.sina.com.cn/focus/zqbjh/"
#              And then show result of crawler in the command.
#              Four Securities newspaper:
#              [1]China Securities Journal(zgzqb)
#              [2]Securities Daily(zqrb)
#              [3]Shanghai Securities News(shzqb)
#              [4]Securities Times(zqsb)

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-22 17:03:18
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import urllib2

################################### PART2 CLASS && FUNCTION ###########################
class CrawlSinaSecuritiesNewspapers(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_daily_newspaper_links_list(self):
        initial_link = "http://finance.sina.com.cn/focus/zqbjh/"
        daily_newspaper_all_links = []
        request = urllib2.Request(initial_link)
        response = urllib2.urlopen(request, timeout = None)
        print response.read()


test = CrawlSinaSecuritiesNewspapers()
test.get_daily_newspaper_links_list()