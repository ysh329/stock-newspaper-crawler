# stock-newspaper-crawler  

<font color=red>This project has stopped, now only use for reference.</font>  

This project has the procedure of three steps:    
1. Create database used for storing crawled essays' data.  
2. Crawl data from web user defined and store them to database.  
3. Describe the metadata of crawled essays' data and generate report, then plot the bar chart and pie chart according to
 the descriptive report.  
 
 In this project, python is used widely. Especially,  
1. In crawler part, library BeautifulSoup, urllib2, re ;  
2. In database part, MySQLdb;  
3. In plot part, matplotlib;  
4. In other parts, logging, os, time, numpy.   

2015-10-18 21:57:00  

## My first respository on GitHub!  

I (have to) love :coffee:. More concretely, it's the first step (crawl corpus from CCSTOCK.CN) of LDA model(one of topic models).  

This little project is about the fundamentals of natural language processing, mainly concentrating on Chinese word count,
word frequency statistic and etc. The module of Chinese word count is accomplished by MM(Maximum Matching) method
and RMM(Reverse Maximum Matching) method.  

## Summary  

### 2015-7-29  
Project stops temporarily. Now I have realized the main function of crawl stock news data from CCSTOCK.CN. However, there still has remained some tasks:  
1. Further improve in success match rate of stock news. The regular expression need to be further optimized. Current match rate is about 0.86.  
2. Some Variables can be a generator type. Such as the variable all_essays_link_list, etc.  
3. Use map method to improve efficiency, such as when inserting records into database, etc.  
4. Go on Crawl function. If network status is bad or program stops accidentally, restart our main.py to go on crawling news from last break point.  
