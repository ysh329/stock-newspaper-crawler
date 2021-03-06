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
from myclass.class_newspaper_metadata import *
import os.path
################################ PART3 MAIN ###########################################
def main():
    base_url = "http://www.ccstock.cn/meiribidu/sidazhengquanbaotoutiao/"
    database_name = "essayDB"
    CrawlerDB = CreateDatabaseClass()
    CrawlerDB.create_database(database_name)
    CrawlerDB.create_table(database_name)

    Crawler = CrawlSecuritiesNewspapers()
    # Get all pages' links
    # Reverse all the link elements in list(Time series), last element is today's news link.
    all_essays_links_list = Crawler.get_all_pages_essays_links_list(base_url = base_url)
    all_essays_links_list = all_essays_links_list[::-1]
    logging.info("len(all_essays_links_list):%s" % len(all_essays_links_list))

    success_insert_record_num = all_insert_record_num = 0
    for essay_idx in xrange(len(all_essays_links_list)):
        essay_link = all_essays_links_list[essay_idx]
        logging.info("[%3s]essay_link:%s" % ((essay_idx+1), essay_link))
        logging.info("[%3s]essay_link:%s" % (essay_idx, essay_link))
        part1, part2, part3, part4 = Crawler.get_cur_essay_page_information_tuple(cur_page_link = essay_link)

        # part1 - zqrb
        # part1 = (part1_zqrb_titles_list, part1_zqrb_content_list, date, cur_page_link, part1_zqrb_links_list)
        part1_table_name = "securities_newspaper_zqrb_table"
        part1_title_list = part1[0]
        part1_content_list = part1[1]
        part1_date_str = part1[2]
        part1_cur_page_str = part1[3]
        part1_links_list = part1[4]
        all_insert_record_num += max(len(part1_title_list), len(part1_content_list), len(part1_links_list))
        if len(part1_title_list) == len(part1_links_list) == len(part1_content_list):
            CrawlerDB.insert_title_content_date_link_list_2_db(table_name = part1_table_name,\
                                                               title_list = part1_title_list,\
                                                               content_list = part1_content_list,\
                                                               date = part1_date_str,\
                                                               page_link = part1_cur_page_str,\
                                                               link_list = part1_links_list)
            logging.info("%d/%d part1 insert task has been finished." % (essay_idx+1, len(all_essays_links_list)))
            success_insert_record_num += len(part1_title_list)
        else:
            logging.error("%d/%d part1 insert task failed." % (essay_idx+1, len(all_essays_links_list)))


        # part2 - zgzqb
        # part2 = (part2_zgzqb_titles_list, part2_zgzqb_content_list, date, cur_page_link, part2_zgzqb_links_list)
        part2_table_name = "securities_newspaper_zgzqb_table"
        part2_title_list = part2[0]
        part2_content_list = part2[1]
        part2_date_str = part2[2]
        part2_cur_page_str = part2[3]
        part2_links_list = part2[4]
        all_insert_record_num += max(len(part1_title_list), len(part1_content_list), len(part1_links_list))
        if len(part2_title_list) == len(part2_links_list) == len(part2_content_list):
            CrawlerDB.insert_title_content_date_link_list_2_db(table_name = part2_table_name,\
                                                               title_list = part2_title_list,\
                                                               content_list = part2_content_list,\
                                                               date = part2_date_str,\
                                                               page_link = part2_cur_page_str,\
                                                               link_list = part2_links_list)
            logging.info("%d/%d part2 insert task has been finished." % (essay_idx+1, len(all_essays_links_list)))
            success_insert_record_num += len(part1_title_list)
        else:
            logging.error("%d/%d part2 insert task failed." % (essay_idx+1, len(all_essays_links_list)))

        # part3 - shzqb
        # part3 = (part3_shzqb_titles_list, part3_shzqb_content_list, date, cur_page_link, part3_shzqb_links_list)
        part3_table_name = "securities_newspaper_shzqb_table"
        part3_title_list = part3[0]
        part3_content_list = part3[1]
        part3_date_str = part3[2]
        part3_cur_page_str = part3[3]
        part3_links_list = part3[4]
        all_insert_record_num += max(len(part1_title_list), len(part1_content_list), len(part1_links_list))
        if len(part3_title_list) == len(part3_links_list) == len(part3_content_list):
            CrawlerDB.insert_title_content_date_link_list_2_db(table_name = part3_table_name,\
                                                               title_list = part3_title_list,\
                                                               content_list = part3_content_list,\
                                                               date = part3_date_str,\
                                                               page_link = part3_cur_page_str,\
                                                               link_list = part3_links_list)
            logging.info("%d/%d part3 insert task has been finished." % (essay_idx+1, len(all_essays_links_list)))
            success_insert_record_num += len(part1_title_list)
        else:
            logging.error("%d/%d part3 insert task failed." % (essay_idx+1, len(all_essays_links_list)))

        # part4 - zqsb
        # part4 = (part4_zqsb_titles_list, part4_zqsb_content_list, date, cur_page_link, part4_zqsb_links_list)
        part4_table_name = "securities_newspaper_zqsb_table"
        part4_title_list = part4[0]
        part4_content_list = part4[1]
        part4_date_str = part4[2]
        part4_cur_page_str = part4[3]
        part4_links_list = part4[4]
        all_insert_record_num += max(len(part1_title_list), len(part1_content_list), len(part1_links_list))
        if len(part4_title_list) == len(part4_links_list) == len(part4_content_list):
            CrawlerDB.insert_title_content_date_link_list_2_db(table_name = part4_table_name,\
                                                               title_list = part4_title_list,\
                                                               content_list = part4_content_list,\
                                                               date = part4_date_str,\
                                                               page_link = part4_cur_page_str,\
                                                               link_list = part4_links_list)
            logging.info("%d/%d part4 insert task has been finished." % (essay_idx+1, len(all_essays_links_list)))
            success_insert_record_num += len(part1_title_list)
        else:
            logging.error("%d/%d part4 insert task failed." % (essay_idx+1, len(all_essays_links_list)))

    logging.info("%d record insert task finished successfully." % success_insert_record_num)
    logging.info("%d record insert task failed." % (all_insert_record_num - success_insert_record_num))
    logging.info("%d record insert task totally(success task num. plus failed task num.)." % all_insert_record_num)
    logging.info("insert success rate:%f." % (success_insert_record_num/float(all_insert_record_num)))


    # Meta data analysis
    # Initial parameters and construct variables.
    database_name = "essayDB"
    table_name_list = ["securities_newspaper_shzqb_table",
                       "securities_newspaper_zgzqb_table",
                       "securities_newspaper_zqrb_table",
                       "securities_newspaper_zqsb_table"]
    result_text_save_directory = "./data/output/newspaper_metadata.txt"
    result_pie_chart_plot_save_directory = os.path.join(".", "data", "output", "newspaper_metadata_pie_chart.png")
    result_bar_chart_plot_save_directory = os.path.join(".", "data", "output", "newspaper_metadata_bar_chart.png")
    result_plot_save_base_dir = os.path.join(".", "data", "output")

    MetaData = ComputeNewspaperMetaData(database_name = database_name,
                                        result_save_directory = result_text_save_directory)
    table_record_num_list = MetaData.get_table_record_num_list(database_name = database_name,
                                                               table_name_list = table_name_list)
    MetaData.plot_pie_chart(table_name_list= table_name_list,
                            table_record_num_list = table_record_num_list,
                            result_plot_save_directory = result_pie_chart_plot_save_directory)
    MetaData.plot_bar_chart(table_name_list= table_name_list,
                            table_record_num_list = table_record_num_list,
                            title_name = "The number of four kinds of newspapers",
                            title_comment = "",
                            xlabel_name = "Newspaper's Name",
                            ylabel_name = "Num.",
                            result_plot_save_directory = result_bar_chart_plot_save_directory)

    title_len_2d_list, content_len_2d_list = MetaData.get_newspaper_length_information(database_name = database_name,
                                                                               table_name_list = table_name_list)
    map(lambda list_name, title_list:
        MetaData.compute_basic_statistic_information(list_name = list_name,
                                                     list_comment = "title",
                                                     demo_list = title_list,
                                                     result_plot_save_base_dir = result_plot_save_base_dir),
        table_name_list, title_len_2d_list)
    map(lambda list_name, content_list:
        MetaData.compute_basic_statistic_information(list_name = list_name,
                                                     list_comment = "content",
                                                     demo_list = content_list,
                                                     result_plot_save_base_dir = result_plot_save_base_dir),
        table_name_list, content_len_2d_list)

    title_len_list = flatten(title_len_2d_list)
    content_len_list = flatten(content_len_2d_list)
    MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                                 list_comment = "title",
                                                 demo_list = title_len_list,
                                                 result_plot_save_base_dir = result_plot_save_base_dir)
    MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                                 list_comment = "content",
                                                 demo_list = content_len_list,
                                                 result_plot_save_base_dir = result_plot_save_base_dir)
    title_and_content_len_list = map(lambda title_len, content_len:
                                     title_len + content_len,
                                     title_len_list, content_len_list)
    MetaData.compute_basic_statistic_information(list_name = "all kinds of newspapers",
                                                 list_comment = "title and content",
                                                 demo_list = title_and_content_len_list,
                                                 result_plot_save_base_dir = result_plot_save_base_dir)
################################ PART4 EXECUTE ##################################
if __name__ == "__main__":
    main()