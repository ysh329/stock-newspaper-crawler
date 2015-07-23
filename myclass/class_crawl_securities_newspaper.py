# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_crawl_securities_newspaper.py
# Description: Crawl data from "四大证券报精华_163,
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
import re
from bs4 import BeautifulSoup

################################### PART2 CLASS && FUNCTION ###########################
class Crawl163SecuritiesNewspapers(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_daily_newspaper_links_list(self):
        initial_link = "http://money.163.com/special/0025262F/sidbk.html"
        daily_newspaper_all_links = []
        request = urllib2.Request(initial_link)
        response = urllib2.urlopen(request, timeout=None)
        web_text = response.read()
        #print type(web_text)
        '''
        web_charset = re.compile('charset=(.*)"').findall('tml; charset=gb2312" />')[0]
        web_charset = re.compile('charset=(.*)').findall(web_text)
        print "charset of current page: ", web_charset
        print len(web_charset)
        '''
        print "length of current page: ", len(web_text)
        soup = BeautifulSoup(web_text, from_encoding="GBK")
        print soup

        return daily_newspaper_all_links

test = CrawlSinaSecuritiesNewspapers()
test.get_daily_newspaper_links_list()