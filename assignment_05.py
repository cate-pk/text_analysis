#!/usr/bin/env python
# coding: utf-8

# ### MAC OS 사용합니다.

# 다음은 서점 yes24 메인페이지 URL = 'http://www.yes24.com/main/default.aspx' 입니다.
# 
# 메인페이지에서 시작해 국내도서 베스트셀러, 순위 1-10위 책에 대해
# 
# .순위, 제목, 저자, 출판사, 판매가, 출간일을 프린트하고, 하단에 첫 회원리뷰의 첫 줄을 프린트 하시오.
# 
# 1. 제목:...............................................
# 
#     회원리뷰:....................................
# 
# 2. 제목: 달러구트 꿈 백화점, 저자: 이미예, 출판사: 팩토리나인, 판매가: 12,420원, 출간일: 2020년 07월 08일
# 
#    회원리뷰:판타지세계에서 사회 초년생이 성장해가는 이야기?
# 
# 3. ........................
# 
# 4. ....................
# 
# 5. ...................
# 
# .
# 
# 10. ......................................
# 
# 

# In[1]:


import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
driver = webdriver.Chrome(executable_path=r'C:\chromedriver_win32\chromedriver.exe')


# In[2]:


url = 'http://www.yes24.com/main/default.aspx'
driver.get(url)


# In[3]:


# 베스트셀러로 이동
element1 = driver.find_element_by_xpath('//*[@id="yesFixCorner"]/dl/dd/ul[1]/li[1]/a').click()
time.sleep(5)


# In[4]:


rank_list = [1,2,3,4,5,6,7,8,9,10]

for i in rank_list:
    # 배너 광고 없앰
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="divYes24SCMEvent"]/div[2]/div[2]/a/em/img').click()
    time.sleep(3)
    
    rank = i
    
    # price
    price_tag = '#bestList > ol > li.num{} > p.price > strong'.format(i)
    price = driver.find_element_by_css_selector(price_tag)
    price = price.text

    product_address = driver.find_element_by_xpath('//*[@id="bestList"]/ol/li[{}]/p[3]/a'.format(i)).click()
    time.sleep(5)
    
    # title
    title_tag = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2'
    title = driver.find_element_by_css_selector(title_tag)
    title = title.text
    
    # author
    author_tag = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth > a'
    author = driver.find_element_by_css_selector(author_tag)
    author = author.text

    # publish
    publisher_path = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_pub > a'
    publisher = driver.find_element_by_css_selector(publisher_path)
    publisher = publisher.text
    
    # date
    date_tag = '#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_date'
    date = driver.find_element_by_css_selector(date_tag)
    date = date.text
    
    # review
    try:
        review_tag = '#infoset_reviewContentList > div:nth-child(3) > div.reviewInfoBot.crop > a > div'
        review = driver.find_element_by_css_selector(review_tag).text
        review = review.split('.')[0]
        
        print('{}. 제목: {}, 저자: {}, 출판사: {}, 판매가: {}, 출간일: {}'.format(rank, title, author, publisher, price, date))
        print('   회원리뷰: '+review)        
        
    except NoSuchElementException:
        
        print('{}. 제목: {}, 저자: {}, 출판사: {}, 판매가: {}, 출간일: {}'.format(rank, title, author, publisher, price, date))
        print('   (작성된 리뷰가 없습니다.)')           
        
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)


# In[5]:


driver.close()

