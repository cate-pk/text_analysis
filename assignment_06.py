#!/usr/bin/env python
# coding: utf-8


#     
# ### MAC OS 사용합니다.
# 
# 아래는 ['세종대왕님이 우신다'...한글 파괴 앞장서는 지자체들] 이란 제목의 연합뉴스 기사이고, url은 다음과 같습니다.
# 
# url = 'https://www.yna.co.kr/view/AKR20181008116600055'
# 
# 연합뉴스 site로 부터 기사를 web scraping 해 온 후, KoNLPy 에서 제공하는 Okt 형태소 분석기를 사용해, Noun을 추출하고, 불용어 제거를 위한 별도의 사전을 다음과 같이 구성하고, stopwords = ['연합뉴스', '서울', '기자', '정경재', '김도훈', '저작권자', '무단', '전재', '재배포', '금지', '송고'], 이들  불용어가 제거된 최종 명사 리스트와 리스트의 원소 갯수를 화면에 표시하십시오.

# In[1]:


import requests
from bs4 import BeautifulSoup
import konlpy.tag


# In[2]:


def get_article_content(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    title = soup.title.text

    news_contents = soup.find_all ('p')
    content_text = ''
    for content in news_contents:
        content_text = content_text +' '+ content.text
    
    return title, content_text


# In[3]:


url = 'https://www.yna.co.kr/view/AKR20181008116600055'


# In[4]:


# Web Scraping
title, content_text = get_article_content(url)


# In[5]:


filtered_content = content_text.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('"','')


# In[6]:


# Okt 형태소 분석기 사용하여 Noun 추출
okt = konlpy.tag.Okt()
Noun_words = okt.nouns(filtered_content)


# In[7]:


# 불용어 사전 정의
stopwords = ['연합뉴스', '서울', '기자', '정경재', '김도훈', '저작권자', '무단', '전재', '재배포', '금지', '송고']


# In[8]:


# 중복된 단어 제거
unique_Noun_words = set(Noun_words)

# 불용어 제거
for word in unique_Noun_words:
    if word in stopwords:
        while word in Noun_words: 
            Noun_words.remove(word) 

# 화면에 표시
print(unique_Noun_words)            
print(len(unique_Noun_words))


# In[ ]:




