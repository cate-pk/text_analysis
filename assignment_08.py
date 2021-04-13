#!/usr/bin/env python
# coding: utf-8

#     
# ### MAC OS 사용합니다.
# 
# '비트코인 잔치' 끝났나?는  2018년 1월 24일 네이버 뉴스에 실린 기사입니다.
# 
# url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004164498'
# 
# 이제까지 학습한 내용을 기반으로 다음 문제를 해결하시기 바랍니다.
# 
# 1. 네이버 뉴스로부터 scraping 해 온후, 제목, 소제목, 본문을  bitcoin_news.txt에 저장한 후 다시 읽어들입니다.
# 2. 읽어드린 기사 내용을 korean text preprocessing 하고, preprocessing 단계별 로직에 대한 코멘트를 넣으십시오.
#    반드시, 불용어 단어 채택이유를 설명하십시오.
# 3. 기사 내용에 바탕해 wordcloud를 스크린에 표시하십시오.
#    단어 빈도수를 결정한다면, 설정한 빈도수 기준에 대한 이유를 설명하십시오.

# In[1]:


import requests
from bs4 import BeautifulSoup
import konlpy.tag
import re


# In[2]:


def get_article_content(url):

    source = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
    soup = BeautifulSoup(source, 'lxml')
    
    # 제목
    title = soup.find('div', attrs={'class': 'article_info'})
    title = title.find('h3').text
    
    # 소제목
    sub_heading = soup.find('div', attrs={'class': '_article_body_contents'})
    sub_heading = sub_heading.find('b').text
    
    # 본문
    content_tag = '#articleBodyContents'
    content = soup.select(content_tag)
    content = content[0].text.split(']')[1].split('▶')[0]
    
    return title, sub_heading, content


# In[3]:


url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004164498'


# In[4]:


title, sub_heading, content = get_article_content(url)


# In[5]:


# 제목, 소제목, 본문을 bitcoin_news.txt에 저장
with open('bitcoin_news.txt', 'w', encoding = 'utf8') as f:
    f.write(title+'\n')
    f.write(sub_heading+'\n')
    f.write(content+'\n')


# In[6]:


# 저장한 기사를 다시 읽어들임
with open('bitcoin_news.txt', 'r', encoding='utf8') as f:
    content = f.read()


# In[7]:


# 불필요한 기호 없애기 등의 기본 전처리 작업
filtered_content = content.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('"','')


# In[8]:


# Komoran 사용하여 명사 추출
komoran = konlpy.tag.Komoran()
Noun_words = komoran.nouns(filtered_content)
print(Noun_words)
print(len(Noun_words))


# In[9]:


# 불용어 사전 정의 
stopwords = ['아시아경제', '김철현', '코인마켓캡', '그', '리', '기자', '무단전재' '배포금지', '저작권']

#불용어 단어 채택 이유: 추출한 명사 중에 하기와 같은 이유로 불용어 사전 정의하여 제거함
#  1. 고유명사: '아시아경제', '김철현', '코인마켓캡'
#  2. 대명사: '그'
#  3. 명사가 될 수 없는 단어: '리'
#  4. 글의 문맥에 있어 필요 없는 단어: '기자', '무단전재' '배포금지', '저작권'


# In[10]:


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


# In[11]:


# WordCloud 만들기
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False


# In[12]:


total_words = ''

for word in unique_Noun_words:
    total_words = total_words+' '+word


# In[13]:


wordcloud = WordCloud(max_font_size=90, relative_scaling=.95, 
                      font_path='/Library/Fonts/AppleGothic.ttf').generate(total_words)
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:




