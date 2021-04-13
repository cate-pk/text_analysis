#!/usr/bin/env python
# coding: utf-8


#     
# ### MAC OS 사용합니다.
# 
# 프로그램을 수행하는 디렉토리에 /docs 하위 디렉토리를 만들고, 여기에 4개의 파일을 저장합니다.
# 
# (apple_iphone1.txt ... serena_williams1.txt는 지난주 오늘의 강의자료 내 *.zip 파일을 풀면 얻을 수 있습니다)
# 
# BoW모델을 사용해, Euclidean 거리와 Cosine Similarity를 사용해 4개 문서 중 문서가 다루는 주제가 유사한 문서를 제시하십시오.

# In[1]:


import os
from os.path import isfile, join
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer 

import nltk
nltk.download('stopwords')
import re

import my_preprocessing


# In[2]:


mypath = './docs/'
os.listdir(mypath)


# In[3]:


# mypath에 file이 아니고 디렉토리가 있을 수 있으므로 file만 골라냅니다.
onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

# 4개 파일 내용을 리스트로 읽어드리기 위해 total_docs를 empty list로 정의하고,
# for loop을 실행시켜 4개 파일의 내용을 차례로 추가합니다.
total_docs = [] 
for file in onlyfiles:
    file_path = mypath+file
    with open(file_path, 'r', encoding='utf8') as f:
        content = f.read()
    total_docs.append(content)


# In[4]:


# 불용어 사전 정의
stopwords = ['be', 'today', 'yesterday', 'new', 'york', 'time']


# In[5]:


# 전처리
docs_nouns = [my_preprocessing.En_preprocessing(doc, stopwords) for doc in total_docs]


# In[6]:


# document에 있는 모든 명사 단어들을 합침
total_docs_nouns = [] 
for words in docs_nouns:
    total_docs_nouns.extend(words)


# In[7]:


# returns a frequency-based DTM: 
def tf_extractor(corpus): 
    vectorizer = CountVectorizer(min_df=1, ngram_range=(1,1))
    features = vectorizer.fit_transform(corpus) # transform texts to a frequency matrix
    return vectorizer, features    

# returns a tf-idf based DTM
def tfidf_extractor(corpus):
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,1))
    features = vectorizer.fit_transform(corpus)
    return vectorizer, features


# In[8]:


# 4개 문서 각각에 대해, 각 문서의 명사 단어로 된 리스트를 만듬.
# 불필요한 단어들을 제거하고 난후 DTM로 변환하기 위해 다시 list of strings의 형태로 변환
documents_filtered = []
for doc in docs_nouns:
    document_filtered =''
    for word in doc:
        document_filtered = document_filtered+' '+word
    documents_filtered.append(document_filtered)


# In[9]:


# 문서들을 TF 기반 DTM으로 (matrix) 변환
vectorizer_tf, DTM_tf = tf_extractor(documents_filtered)
DTM_TF = np.array(DTM_tf.todense())

# 문서들을 TFIDF 기반 DTM으로(matrix) 변환
vectorizer_tfidf, DTM_tfidf = tfidf_extractor(documents_filtered)
DTM_TFIDF = np.array(DTM_tfidf.todense())


# In[10]:


tf01 = np.linalg.norm(DTM_TF[0]-DTM_TF[1])
tf02 = np.linalg.norm(DTM_TF[0]-DTM_TF[2])
tf03 = np.linalg.norm(DTM_TF[0]-DTM_TF[3])
tf12 = np.linalg.norm(DTM_TF[1]-DTM_TF[2])
tf13 = np.linalg.norm(DTM_TF[1]-DTM_TF[3])
tf23 = np.linalg.norm(DTM_TF[2]-DTM_TF[3])

tf_distance = [tf01,tf02,tf03,tf12,tf13,tf23]

print("TF 기반 Euclidean distance:\n* 문서1&문서2: {}\n* 문서1&문서3: {}\n* 문서1&문서4: {}\n* 문서2&문서3: {}\n* 문서2&문서4: {}\n* 문서3&문서4: {}\n".format(tf01, tf02, tf03, tf12, tf13, tf23))


# In[11]:


tfidf01 = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[1])
tfidf02 = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[2])
tfidf03 = np.linalg.norm(DTM_TFIDF[0]-DTM_TFIDF[3])
tfidf12 = np.linalg.norm(DTM_TFIDF[1]-DTM_TFIDF[2])
tfidf13 = np.linalg.norm(DTM_TFIDF[1]-DTM_TFIDF[3])
tfidf23 = np.linalg.norm(DTM_TFIDF[2]-DTM_TFIDF[3])
print("TFIDF 기반 Euclidean distance:\n* 문서1&문서2: {}\n* 문서1&문서3: {}\n* 문서1&문서4: {}\n* 문서2&문서3: {}\n* 문서2&문서4: {}\n* 문서3&문서4: {}\n".format(tf01, tf02, tf03, tf12, tf13, tf23))


# In[12]:


cos_tf01 = np.dot(DTM_TF[0],DTM_TF[1])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[1]))
cos_tf02 = np.dot(DTM_TF[0],DTM_TF[2])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[2]))
cos_tf03 = np.dot(DTM_TF[0],DTM_TF[3])/(np.linalg.norm(DTM_TF[0])*np.linalg.norm(DTM_TF[3]))
cos_tf12 = np.dot(DTM_TF[1],DTM_TF[2])/(np.linalg.norm(DTM_TF[1])*np.linalg.norm(DTM_TF[2]))
cos_tf13 = np.dot(DTM_TF[1],DTM_TF[3])/(np.linalg.norm(DTM_TF[1])*np.linalg.norm(DTM_TF[3]))
cos_tf23 = np.dot(DTM_TF[2],DTM_TF[3])/(np.linalg.norm(DTM_TF[2])*np.linalg.norm(DTM_TF[3]))
print("TF 기반 cosine 유사도:\n* 문서1&문서2: {}\n* 문서1&문서3: {}\n* 문서1&문서4: {}\n* 문서2&문서3: {}\n* 문서2&문서4: {}\n* 문서3&문서4: {}\n".format(cos_tf01, cos_tf02, cos_tf03, cos_tf12, cos_tf13, cos_tf23))


# In[13]:


cos_tfidf01 = np.dot(DTM_TFIDF[0],DTM_TFIDF[1])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[1]))
cos_tfidf02 = np.dot(DTM_TFIDF[0],DTM_TFIDF[2])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[2]))
cos_tfidf03 = np.dot(DTM_TFIDF[0],DTM_TFIDF[3])/(np.linalg.norm(DTM_TFIDF[0])*np.linalg.norm(DTM_TFIDF[3]))
cos_tfidf12 = np.dot(DTM_TFIDF[1],DTM_TFIDF[2])/(np.linalg.norm(DTM_TFIDF[1])*np.linalg.norm(DTM_TFIDF[2]))
cos_tfidf13 = np.dot(DTM_TFIDF[1],DTM_TFIDF[3])/(np.linalg.norm(DTM_TFIDF[1])*np.linalg.norm(DTM_TFIDF[3]))
cos_tfidf23 = np.dot(DTM_TFIDF[2],DTM_TFIDF[3])/(np.linalg.norm(DTM_TFIDF[2])*np.linalg.norm(DTM_TFIDF[3]))
print("TFIDF 기반 cosine 유사도:\n* 문서1&문서2: {}\n* 문서1&문서3: {}\n* 문서1&문서4: {}\n* 문서2&문서3: {}\n* 문서2&문서4: {}\n* 문서3&문서4: {}\n".format(cos_tfidf01, cos_tfidf02, cos_tfidf03, cos_tfidf12, cos_tfidf13, cos_tfidf23))


# In[14]:


print('* TF, TFIDF 기반 Euclidean distance가 가장 가까운 문서들은 "serena_williams1.txt"과 "kevin_durant1.txt"이다.')
print('* TF, TFIDF 기반 cosine 유사도 가장 높은 문서들은 "apple_iphone2.txt"과 "apple_iphone1.txt"이다.')


# In[ ]:




