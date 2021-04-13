#!/usr/bin/env python
# coding: utf-8


# 
# * Using the following url, 
# http://www.yes24.com/24/category/bestseller
# 
# * Find top 40 best sellers except 19 th and 20 th
#  - Error 가 발생하는 순위는 제외
#  - 순위
#  - 책제목
#  - 저자
#  - 출판사
#  - 출간일
#  
# * Save the info into a file

# In[1]:


import requests
from bs4 import BeautifulSoup as bs


# In[2]:


url = 'http://www.yes24.com/24/category/bestseller'
source = requests.get(url).text
soup = bs(source, 'lxml')


# In[3]:


#list of indices to be ignored
ignore=[0, 19, 20] 

# list of ranks
list = [indice for indice in range(41) if indice not in ignore]


# In[4]:


bestsellers = []

for i in list:
    try:
        rank = i

        # title
        title_tag = '#bestList > ol > li.num{0} > p:nth-child(3) > a'.format(i)
        title_full = soup.select(title_tag)
        title = title_full[0].text

        # author
        author_tag = '#bestList > ol > li.num{0} > p.aupu > a:nth-child(1)'.format(i)
        author = soup.select(author_tag)
        author = author[0].text

        # publisher
        publisher_tag = '#bestList > ol > li.num{0} > p.aupu > a:nth-child(2)'.format(i)
        publisher = soup.select(publisher_tag)
        publisher = publisher[0].text
        
        # publishing date
        product_address = str(title_full)[10:33]
        product_url = "http://www.yes24.com" + product_address

        source_p = requests.get(product_url).text
        soup_p = bs(source_p, 'lxml')

        date_tag = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_date'
        date = soup_p.select(date_tag)
        date = date[0].text

        bestsellers.append([rank, title, author, publisher, date])
        
    except:
        pass


# In[5]:


with open('yes24_best_seller_results.txt', 'w') as f:
    for item in bestsellers:
        f.write("%s\n" % item)
f.close()


# In[ ]:




