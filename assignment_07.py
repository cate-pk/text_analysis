#!/usr/bin/env python
# coding: utf-8


#     
# ### MAC OS 사용합니다.
# 
# 아래 url은 Naver news 교황 사실상 방북 결정…힘 실리는 文대통령 '한반도 평화프로세스‘ 라는 제목의 기사입니다.
# 
# url = 'https://news.naver.com/main/read.nhn?oid=421&sid1=100&aid=0003646082&mid=shm&mode=LSD&nh=20181018225255'
# 
# - 단어의 출현 빈도수를 NUM_WORDS = 10 로 정의하고,
# 1. Text Network Analysis 를 수행하여, matplotlib.pylot를 이용해 해당 Graph를 화면에 표시하고,
# 2. 연결중심도, 매개중심도, 근접중심도 각각 가장 높은 노드를 화면에 표시하십시오.
#      * 연결중심도는 노드 v가 가장 높습니다.
#      * 매개중심도는 .......
#      * 근접중심도는........
# 3. 10개 단어에 대해서 아래와 같이 화면에 표시하십시오.
#      * 단어 xxxx는 9개의 단어와 연결되어 있습니다.
#             ['ㄱㄱㄱ', 'ㄴㄴㄴ', 'ㄷㄷㄷ', ... 'ㅅㅅㅅ', 'ㅋㅋㅋ'] 
#      * 단어 yyyy는 7개의 단어와 연결되어 있습니다.
#            ['ㄱㄱㄱ', 'ㄴㄴㄴ', 'ㄷㄷㄷ', ... 'ㅅㅅㅅ', 'ㅈㅈㅈ'] 
#    .....
#    형태로 10개의 단어가 연결되어 있는 것을 화면에 표시하십시오.

# In[1]:


import requests
from bs4 import BeautifulSoup
import konlpy.tag
import re
import matplotlib.pyplot as plt
import matplotlib as mlt
from collections import Counter
import networkx as nx
import itertools


# In[2]:


def get_article_content(url):
    
    source = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
    soup = BeautifulSoup(source, 'lxml')

    title = soup.title.text

    body = soup.find('div', attrs={'id': 'articleBodyContents'}).text.split('}')[1]
    
    return title, body


# In[3]:


url = 'https://news.naver.com/main/read.nhn?oid=421&sid1=100&aid=0003646082&mid=shm&mode=LSD&nh=20181018225255'


# In[4]:


title, content = get_article_content(url)


# In[5]:


with open('pope.txt', 'w', encoding = 'utf8') as f:
    f.write(title+'\n')
    f.write(content+'\n')


# In[6]:


with open('pope.txt', 'r', encoding='utf8') as f:
    content = f.read()


# In[7]:


filtered = content.replace('\n', '').replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('"','')


# In[8]:


komoran = konlpy.tag.Komoran()
Noun_words = komoran.nouns(filtered)


# In[9]:


def get_sentences(text): # 문장 단위로 쪼개 줌
    sentences = re.split(r'[\.\?\!]\s+', text) # '.','?,'!'가 나오면 문장의 끝이라고 가정하고 해당 문자가 나오면 쪼개줌.
    return sentences


# In[10]:


get_sents = get_sentences(content)


# In[11]:


dataset = []
for i in range(len(get_sents)):
    dataset.append(komoran.nouns(re.sub(r'[^\s\d\w]', '', get_sents[i])))
    
total_nouns = []
for words in dataset:
    total_nouns.extend(words)


# In[12]:


# 단어의 출현 빈도 파악

# 불용어 사전 정의
stopwords = ['뉴스1' ,'네이버', '구독', '무단', '전재','배포', '금지']

# 중복된 단어 제거
unique_Noun_words = set(total_nouns)

# 불용어 제거
for word in unique_Noun_words:
    if word in stopwords:
        while word in total_nouns: 
            total_nouns.remove(word) 


# In[13]:


NUM_WORDS = 10


# In[14]:


# 단어의 출현 빈도수 설정을 위한 모듈 import
c = Counter(total_nouns)

# 빈도수 기준 상위 NUM_WORDS개 단어 출력
NUM_WORDS = 10
top_10 = c.most_common(NUM_WORDS)

# 단어만 추출
top_10_nouns = [a_tuple[0] for a_tuple in top_10]


# In[15]:


G = nx.Graph()
G.add_nodes_from(top_10_nouns)


# In[16]:


for pair in list(itertools.combinations(list(top_10_nouns), 2)): 
    if pair[0] == pair[1]:
        continue
    for sent in dataset:
        if pair[0] in sent and pair[1] in sent:
            if pair in list(G.edges()) or (pair[1],pair[0]) in list(G.edges()): 
                G[pair[0]][pair[1]]['weight'] += 1 # tie가 있으면 weight만 추가
            else:
                G.add_edge(pair[0], pair[1], weight=1 )


# In[17]:


nx.draw_networkx(G, font_family="AppleGothic")


# In[18]:


plt.show()


# In[19]:


# 연결중심성
dc = nx.degree_centrality(G)
k1 = [k for k,v in dc.items() if v == max(v for k,v in dc.items())]

print('연결중심성은 노드 {}가 가장 높습니다.'.format(k1))


# In[20]:


# 매개중심성
bc = nx.betweenness_centrality(G)
k2 = [k for k,v in bc.items() if v == max(v for k,v in bc.items())]

print('매개중심성은 노드 {}가 가장 높습니다.'.format(k2))


# In[21]:


# 근접중심성 
cc = nx.closeness_centrality(G)
k3 = [k for k,v in cc.items() if v == max(v for k,v in cc.items())]

print('근접중심성은 노드 {}가 가장 높습니다.'.format(k3))


# In[22]:


for i in top_10_nouns:
    print('단어 {}은(는) {}개의 단어와 연결되어 있습니다.'.format(i, len(G[i])))
    print(list(G.neighbors(i)))


# In[ ]:




