# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_crawl_securities_newspaper.py
# Description: Crawl data from "四大证券报精华_163,
#              http://money.163.com/special/0025262F/sidbk.html
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

    def get_index_pages_links_list(self, soup, initial_index_page_link):
        page_links = soup.findAll(target = '_self')

        '''
        print soup.findAll('a')
        print "page_links length:", len(page_links)
        print "page_links[0]:", len(page_links[0])
        print "str(page_links[0]):", str(page_links[0])
        print "type(page_links[0]):", type(page_links[0])
        print "str(page_links[0]):", str(page_links[0])
        print "str(page_links[1]):", str(page_links[1])
        print "str(page_links[1]):", self.get_page_link(str(page_links[1]))
        '''

        pages_links_list = [initial_index_page_link]
        for page_link_idx in range(len(page_links)):
            if (page_link_idx == 0) or (page_link_idx == len(page_links)-1) or (page_link_idx == len(page_links)-2):
                continue

            page_link = str(page_links[page_link_idx])
            page_link_str = re.compile('a href="(.*)" ').findall(page_link)[0]
            pages_links_list.append(page_link_str)
        '''
        print "page_links_list:", page_links_list
        print "type(page_links_list):", type(page_links_list)
        print "type(page_links_list[0]):", type(page_links_list[0])
        print "len(page_links_list)", len(page_links_list)
        '''
        return pages_links_list



    def get_cur_page_essays_links_list(self, cur_page_link):
        essays_links_list = []

        try:
            request = urllib2.Request(cur_page_link)
            response = urllib2.urlopen(request, timeout=5)
            web_text = response.read()
            soup = BeautifulSoup(web_text, from_encoding="GBK")
        except:
            self.get_cur_page_essays_links_list(cur_page_link)

        labeled_links = soup.findAll('span', 'article')
        for labeled_link_idx in range(len(labeled_links)):
            labeled_link_str = str(labeled_links[labeled_link_idx])
            #link_str = re.compile('a href="(.*)"').findall(labeled_link_str)[0]
            link_str = re.compile('a href="(.*?)"').findall(labeled_link_str)
            #print "link_str:", link_str
            essays_links_list.append(link_str)
        essays_links_list = sum(essays_links_list, [])
        '''
        print "labeled_link_str_list:", essays_links_list
        print "type(labeled_link_str_list)", type(essays_links_list)
        print "type(labeled_link_str_list[0])", type(essays_links_list[0])
        print "len(labeled_link_str_list):", len(essays_links_list)
        '''
        return essays_links_list



    def get_163_all_essays_links_list(self, initial_link):
        all_essays_links_list = []

        request = urllib2.Request(initial_link)
        try:
            response = urllib2.urlopen(request, timeout=5)
            web_text = response.read()
            soup = BeautifulSoup(web_text, from_encoding="GBK")
        except:
            print "urllib2.urllibopen failed at %s." % initial_link
            print " Retrying......"
            self.get_163_all_essays_links_list(initial_link)

        index_pages_links_list = self.get_index_pages_links_list(soup=soup, initial_index_page_link=initial_link)
        for cur_page_idx in range(len(index_pages_links_list)):
            cur_page_link = index_pages_links_list[cur_page_idx]
            #print "cur_page_link:", cur_page_link
            cur_page_essays_links_list = self.get_cur_page_essays_links_list(cur_page_link)
            #print "cur_page_essay_links_list:", cur_page_essays_links_list
            all_essays_links_list.append(cur_page_essays_links_list)
            #print "all_essays_links_list:", all_essays_links_list
            #break
        all_essays_links_list = sum(all_essays_links_list, [])
        '''
        print "all_essays_links_list:", all_essays_links_list
        print "all_essays_links_list[0]:", all_essays_links_list[0]
        print "len(all_essays_links_list):", len(all_essays_links_list)
        '''
        return all_essays_links_list



    # Get information of current essay's page,
    # Information includes: newspaper_name, title, content, date, link, detailed_link
    def get_cur_essay_page_information_list(self, cur_page_link):

        print "Analysing cur_page_link:", cur_page_link
        try:
            request = urllib2.Request(cur_page_link)
            response = urllib2.urlopen(request, timeout=5)
        except:
            self.get_cur_essay_page_information_list(cur_page_link)
            return

        web_text = response.read()
        soup = BeautifulSoup(web_text, from_encoding="GBK")

        soup_str = str(soup)
        web_title = str(soup.title.get_text())
        try: date_time_str =  re.compile('<div class="left">(.*)　来源:').findall(soup_str)[0]
        except: date_time_str = ""
        try: part1_zgzqb_str = re.compile('中国证券报</b></p>(.*)<p><b>上海证券报').findall(soup_str)[0]
        except: part1_zgzqb_str = ""
        try: part2_shzqb_str = re.compile('上海证券报</b></p>(.*)<p><b>证券时报').findall(soup_str)[0]
        except: part2_shzqb_str = ""
        try: part3_zqsb_str = re.compile('证券时报</b></p>(.*)<br/><div class="gg200x300">').findall(soup_str)[0]
        except: part3_zqsb_str = ""
        try: part4_mrjjxw_str = re.compile('每日经济新闻</b></p>(.*)').findall(soup_str)[0]
        except: part4_mrjjxw_str = ""

        print
        print

        print "web_title:", web_title
        print "date_time_str:", date_time_str
        print "part1_zgzqb_str:", part1_zgzqb_str
        print "part2_shzqb_str:", part2_shzqb_str
        print "part3_zgsb_str:", part3_zqsb_str
        print "part4_mrjjxw_str:", part4_mrjjxw_str

        print
        print

        print "Method #1"
        part1_zgzqb_titles_str_list = BeautifulSoup(part1_zgzqb_str).findAll("a")
        print "part1_zgzqb_titles_str_list:", part1_zgzqb_titles_str_list

        part2_shzqb_str_list = BeautifulSoup(part2_shzqb_str).findAll("a")
        print "part2_shzqb_str_list:", part2_shzqb_str_list

        print "Method #2"
        #part1_zgzqb_titles_str_list = re.compile('html">(.*)</a></p>').findall(part1_zgzqb_str)
        part1_zgzqb_titles_str_list = re.compile('html">(.*?)</a></p>').findall(part1_zgzqb_str)
        print "part1_zgzqb_titles_str_list[0]:", part1_zgzqb_titles_str_list[0]
        print "len(part1_zgzqb_titles_str_list):", len(part1_zgzqb_titles_str_list)

        print
        print

        part1_zgzqb_title_str = re.compile('html">(.*?)</a></p>').findall(part1_zgzqb_str)
        print "part1_zgzqb_title_str:", part1_zgzqb_title_str
        print "len(part1_zgzqb_title_str):", len(part1_zgzqb_title_str)
        print "part1_zgzqb_title_str[0]:", part1_zgzqb_title_str[0]
        print "part1_zgzqb_title_str[1]:", part1_zgzqb_title_str[1]



initial_link = "http://money.163.com/special/0025262F/sidbk.html"
test = Crawl163SecuritiesNewspapers()

'''
all_essays_links_list = test.get_163_all_essays_links_list(initial_link)
print 'all_essays_links_list:', all_essays_links_list
print 'all_essays_links_list[0]:', all_essays_links_list[0]
print 'len(all_essays_links_list):', len(all_essays_links_list)
print 'type(all_essays_links_list):', type(all_essays_links_list)
print 'type(all_essays_links_list[0]):', type(all_essays_links_list[0])
'''

#test.get_cur_essay_page_information_list(cur_page_link="http://money.163.com/13/1216/06/9G6Q80170025262F.html")
test.get_163_all_essays_links_list(initial_link)