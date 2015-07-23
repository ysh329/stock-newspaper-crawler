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

    def get_essay_link(self, labeled_link_str):
        return re.compile('a href="(.*)"').findall(labeled_link_str)[0]



    @property
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
        labeled_links = soup.findAll('span', 'article')
        '''
        print "labeled_links len:", len(labeled_links)
        print "labeled_links type:", type(labeled_links)
        print "labeled_links:", labeled_links
        print "str(labeled_links[0]):", str(labeled_links[0])
        '''
        labeled_link_str_list = []
        for labeled_link_idx in range(len(labeled_links)):
            labeled_link_str = str(labeled_links[labeled_link_idx])
            link_str = self.get_essay_link(labeled_link_str)
            labeled_link_str_list.append(link_str)

        print labeled_link_str_list
        print len(labeled_link_str_list)
        #print "link_str:", re.compile('a href="(.*)"').findall(str(labeled_links[0]))[0]



        print "labeled_links[0]:", labeled_links[0].findAll('a')
        print "labeled_links[1]:", labeled_links[1]

        print "++++++++++++++++++++++++"
        print "Parallize"
        print
        print
        '''
        print "labeled_links type:", type(labeled_links)
        print labeled_links
        print len(labeled_links)
        print labeled_links[0]
        unlabeled_links_list = re.compile('a href="(.*)"').findall(str(labeled_links))
        print unlabeled_links_list
        #print re.compile('a href="(.*)"').findall(labeled_links)
        '''
        return daily_newspaper_all_links

test = Crawl163SecuritiesNewspapers()
test.get_daily_newspaper_links_list