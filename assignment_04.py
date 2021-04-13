#!/usr/bin/env python
# coding: utf-8


#     
# ### MAC OS 사용합니다.
# 
# - URL = http://www.yes24.com/Product/Goods/78145872
# - 해당 책의 판매지수, 베스트 셀러 내 건강 취미 부분 37위, 리뷰 내용을 화면에 출력하십시오.
# - 포맷은
#   판매지수: xxxxx, 베스트 셀러 건강 취미: yy 위 를 프린트하고,
# - 회원리뷰 중 리뷰 제목에 '뇌'가 들어가지 않은 리뷰 title만 한줄에 하나씩 프린트 하십시오.
# - 리뷰가 늘어남에 따라 달라질 수 있지만 리뷰 title에 '뇌'자가 들어가지 않은 것은 현재 10개입니다.

# In[1]:


from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs


# In[2]:


# Find 판매지수
url = 'http://www.yes24.com/Product/Goods/78145872'
source = requests.get(url).text
soup = bs(source, 'lxml')
num_sold = soup.find('span', attrs={'class':'gd_sellNum'}).text[25:31]

# 상기 url 내, network inspection 통해 'rank'라는 키워드로 새로운 url 확보하여 국내도서 순위와, 건강취미 부분 순위 데이터 확보
url1 = 'http://www.yes24.com/Product/addModules/BestSellerRank_Book/78145872/?categoryNumber=001001011008&FreePrice=N'
source1 = requests.get(url1).text
soup1 = bs(source1, 'lxml').text
category_rank = soup1[13:16]

print("판매지수: {}, 베스트 셀러 건강 취미: {}".format(num_sold, category_rank))


# In[3]:


review_per_page = [3,4,5,6,7]
review_titles = []
page_num = range(1,30,1)

try:
    for p in page_num:
        url2 = 'http://www.yes24.com/Product/communityModules/GoodsReviewList/78145872?Sort=1&PageNumber={}&Type=ALL'.format(p)
        source2 = requests.get(url2).text
        soup2 = bs(source2, 'lxml')

        for i in review_per_page:

            review_title_tag = '#infoset_reviewContentList > div:nth-child({}) > div.reviewInfoTop > span.review_tit > span'.format(i)
            review_title = soup2.select(review_title_tag)
            review_title = review_title[0].text

            review_titles.append(review_title)
except:
    pass


# In[4]:


filtered = []

for item in review_titles:
    if '뇌' not in item:
        filtered.append(item)

print(*filtered, sep='\n')


# In[ ]:




