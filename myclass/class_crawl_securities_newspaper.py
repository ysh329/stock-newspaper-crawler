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
            return

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
            return

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
            web_text = response.read()
        except:
            self.get_cur_essay_page_information_list(cur_page_link)
            return

        soup = BeautifulSoup(web_text, from_encoding="GBK")

        soup_str = str(soup)
        web_title = soup.title.string
        try: date_time_str =  re.compile('<div class="left">(.*?)　来源:').findall(soup_str)[0]
        except: date_time_str = ""
        try: part1_zgzqb_str = re.compile('中国证券报</b></p>(.*?)<p><b>上海证券报').findall(soup_str)[0]
        except: part1_zgzqb_str = ""
        try: part2_shzqb_str = re.compile('上海证券报</b></p>(.*?)<p><b>证券时报').findall(soup_str)[0]
        except: part2_shzqb_str = ""
        try: part3_zqsb_str = re.compile('证券时报</b></p>(.*?)<br/><div class="gg200x300">').findall(soup_str)[0]
        except: part3_zqsb_str = ""
        try: part4_mrjjxw_str = re.compile('每日经济新闻</b></p>(.*)</p>').findall(soup_str)[0] + '</p>'
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



        '''
        print "part1_zgzqb_titles_str_list:", part1_zgzqb_titles_str_list
        print "part1_zgzqb_titles_str_list[0]:", part1_zgzqb_titles_str_list[0]
        print "len(part1_zgzqb_titles_str_list):", len(part1_zgzqb_titles_str_list)
        print
        print "part2_shzqb_title_str_list:", part2_shzqb_title_str_list
        print "part2_shzqb_title_str_list[0]:", part2_shzqb_title_str_list[0]
        print "len(part2_shzqb_title_str_list):", len(part2_shzqb_title_str_list)
        print
        print "part3_zqsb_title_str_list:", part3_zqsb_title_str_list
        print "part3_zqsb_title_str_list[0]:", part3_zqsb_title_str_list[0]
        print "len(part3_zqsb_title_str_list):", len(part3_zqsb_title_str_list)
        print
        print "part4_mrjjxw_title_str_list", part4_mrjjxw_title_str_list
        print "part4_mrjjxw_title_str_list[0]", part4_mrjjxw_title_str_list[0]
        print "len(part4_mrjjxw_title_str_list)", len(part4_mrjjxw_title_str_list)
        '''
        print "part1"
        part1_zgzqb_titles_str_list = self.get_cur_newspaper_title_list(cur_newspaper_str = part1_zgzqb_str)
        part1_zgzqb_content_str_list = self.get_cur_newspaper_content_list(cur_newspaper_str = part1_zgzqb_str, newspaper_index=1)
        print "part1_zgzqb_content_str_list:", part1_zgzqb_content_str_list
        print "len(part1_zgzqb_content_str_list):", len(part1_zgzqb_content_str_list)
        print "part1_zgzqb_content_str_list[0]:", part1_zgzqb_content_str_list[0]
        print "part1_zgzqb_content_str_list[1]:", part1_zgzqb_content_str_list[1]
        print
        print "part1_zgzqb_titles_str_list:", part1_zgzqb_titles_str_list
        print "part1_zgzqb_titles_str_list[0]:", part1_zgzqb_titles_str_list[0]
        print "len(part1_zgzqb_titles_str_list):", len(part1_zgzqb_titles_str_list)

        print "part2"
        part2_shzqb_title_str_list = self.get_cur_newspaper_title_list(cur_newspaper_str = part2_shzqb_str)
        part2_shzqb_content_str_list = self.get_cur_newspaper_content_list(cur_newspaper_str = part2_shzqb_str, newspaper_index=2)
        print "part2_shzqb_title_str_list:", part2_shzqb_title_str_list
        print "part2_shzqb_title_str_list[0]:", part2_shzqb_title_str_list[0]
        print "len(part2_shzqb_title_str_list):", len(part2_shzqb_title_str_list)
        print
        print "part2_shzqb_content_str_list:", part2_shzqb_content_str_list
        print "part2_shzqb_content_str_list[0]:", part2_shzqb_content_str_list[0]
        print "len(part2_shzqb_content_str_list):", len(part2_shzqb_content_str_list)

        print "part3"
        part3_zqsb_title_str_list = self.get_cur_newspaper_title_list(cur_newspaper_str = part3_zqsb_str)
        part3_zqsb_content_str_list = self.get_cur_newspaper_content_list(cur_newspaper_str = part3_zqsb_str, newspaper_index=3)
        print "part3_zqsb_title_str_list:", part3_zqsb_title_str_list
        print "part3_zqsb_title_str_list[0]:", part3_zqsb_title_str_list[0]
        print "len(part3_zqsb_title_str_list):", len(part3_zqsb_title_str_list)
        print
        print "part3_zqsb_content_str_list:", part3_zqsb_content_str_list
        print "part3_zqsb_content_str_list[0]:", part3_zqsb_content_str_list[0]
        print "len(part3_zqsb_content_str_list):", len(part3_zqsb_content_str_list)


        print "part4"
        part4_mrjjxw_title_str_list = self.get_cur_newspaper_title_list(cur_newspaper_str = part4_mrjjxw_str)
        part4_mrjjxw_content_str_list = self.get_cur_newspaper_content_list(cur_page_link = part4_mrjjxw_str, newspaper_index=4)
        print "part4_mrjjxw_title_str_list", part4_mrjjxw_title_str_list
        print "part4_mrjjxw_title_str_list[0]", part4_mrjjxw_title_str_list[0]
        print "len(part4_mrjjxw_title_str_list)", len(part4_mrjjxw_title_str_list)
        print
        #print "part4_mrjjxw_content_str_list:", part4_mrjjxw_content_str_list
        #print "part4_mrjjxw_content_str_list[0]:", part4_mrjjxw_content_str_list[0]
        #print "len(part4_mrjjxw_content_str_list):", len(part4_mrjjxw_content_str_list)



    def get_cur_newspaper_title_list(self, cur_newspaper_str):
        try:
            cur_newspaper_title_list = self.get_unlabeled_list_or_string(re.compile('html">(.*?)</a></p>').findall(cur_newspaper_str))
        except:
            print "cur_newspaper_str can't match title's pattern and return a blank list."
            cur_newspaper_title_list = []
        return cur_newspaper_title_list



    def get_cur_newspaper_content_list(self, cur_newspaper_str, newspaper_index):
        try:
            cur_newspaper_content_list = self.get_unlabeled_list_or_string(re.compile('</a></p><p>(.*?)</p>').findall(cur_newspaper_str))
        except:
            print "cur_newspaper_str can't match content's pattern and return a blank list."
            cur_newspaper_content_list = []
        return cur_newspaper_content_list


    def get_unlabeled_list_or_string(self, str_or_list):
        print "preparing clean label(s) of string or list variable."

        if type(str_or_list) == str:
            unlabeled_str = re.sub('<[^>]+>','',str_or_list)
            return unlabeled_str
        elif type(str_or_list) == list:
            unlabeled_list = []
            for idx in range(len(str_or_list)):
                cur_str_in_list = str_or_list[idx]
                unlabeled_list.append(re.sub('<[^>]+>','',cur_str_in_list))
            return unlabeled_list
        else:
            print "variable of input's type is wrong and return a blank string."
            return ""



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

test.get_cur_essay_page_information_list(cur_page_link="http://money.163.com/13/1213/06/9FV2O87P0025262F.html")



'''
s = '<p><a href="http://money.163.com/13/1216/00/9G64G7P400253B0H.html">中央提出推进城镇化六大任务</a></p><p>会议要求，城镇化是一个自然历史过程，是我国发展必然要遇到的经济社会发展过程。推进城镇化必须从我国社会主义初级阶段基本国情出发，遵循规律，因势利导，使城镇化成为一个顺势而为、水到渠成的发展过程。确定城镇化目标必须实事求是、切实可行，不能靠行政命令层层加码、级级考核，不要急于求成、拔苗助长。推进城镇化既要积极、又要稳妥、更要扎实，方向要明，步子要稳，措施要实。</p><p><a href="http://money.163.com/13/1216/00/9G64G9H900253B0H.html">完善多层次市场助力创新驱动</a></p><p>新三板扩容大幕开启，多层次资本市场体系建设又向前迈进一大步。新三板这一新的全国性市场体系，在设计上体现了转变政府职能和完善市场机制的方向。作为资本市场改革实验田和<a href="http://quotes.money.163.com/1300005.html">探路者</a>，推动新股发行制度向注册制过渡，是新三板应有的历史使命。由于新三板着力于培育创新型、创业型、成长型中小微企业，扩围还有利于活化社会创新动力，培育经济增长新的<a href="http://quotes.money.163.com/0600405.html">动力源</a>。</p>'
print test.get_unlabeled_list_or_string(s)
'''