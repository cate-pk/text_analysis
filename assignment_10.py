#!/usr/bin/env python
# coding: utf-8


#     
# ### MAC OS 사용합니다.
# 
# Topic Modeling 문제입니다. (12월 10일 19:00가 경과하면 제출이 block 됩니다.)
# 
# #### 32개의 주제에 대해 topic별 15개단어와 단어별 분포를 total_results_test.txt에 저장하시오.
# 
# - 첨부하는 pickle 형태 자료명은 'total_sections_morphs.p' 입니다. type은 dictionary 이고, 내용은 신문기사이며 총 갯수는 7837개입니다.
# 
# - 불용어는 첨부하는 stop_words.txt에 저장되어 있습니다. 불용어를 빈도수로 처리하기 위해 아래와 같이 lower_bound와 upper_bound를 정합니다.
# 
#      * max_doc_frequency = 1000
#      * min_doc_frequency = 3
#      * max_term_frequency = 7000
#      * min_term_frequency = 5
# 
# - topic 수는 임의로  NUM_TOPICS = 32  로 설정합니다.
# 
# - topic마다 관련이 높은 상위 15개의 단어만 보기 위해 NUM_TOPIC_WORDS = 15 로 정합니다.
# 
# - 주제별 15개 단어별 분포를  저장하는 예시는 total_results_test 예시.txt에서 확인할 수 있습니다.

# In[1]:


# import modules

import pandas as pd
import pickle
import gensim
from gensim import corpora
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer 
from collections import Counter
from sklearn.decomposition import LatentDirichletAllocation
from collections import defaultdict

# setting
NUM_TOPICS = 32
NUM_TOPIC_WORDS = 15


# In[2]:


# 불용어 사전 정의
with open('stop_words.txt', 'r') as f:
    stop_words = f.read()
stop_words = stop_words.split('\n')

# 분석자료
with open('total_sections_morphs.p', 'rb') as f:
    d =pickle.load(f)
print(len(d))


# In[3]:


data = pd.DataFrame.from_dict(d, orient='index', columns=['text_title', 'paper_id', 'content'])


# In[4]:


tokenized_doc = []

for i in range(len(d)):
    article = data['content'][i]
    one_article = []
    for t in range(len(article)):
        token = article[t][0]
        one_article.append(token)
    tokenized_doc.append(one_article)


# In[5]:


# pos tagging 없앤 것, tokenized
data['tokenized'] = tokenized_doc 


# In[6]:


data[['content', 'tokenized']].head()


# In[7]:


# 빈도수를 기준으로 불용어처리 하기 위해
def get_filtered_words(docs): 
    term_fre_dict = defaultdict(int)
    doc_fre_dict = defaultdict(int)
    
    for doc in docs:
        for word in doc:
            term_fre_dict[word] += 1
        for word in set(doc):
            doc_fre_dict[word] += 1
    
    max_doc_frequency = 1000
    min_doc_frequency = 3
    max_term_frequency = 7000
    min_term_frequency = 5
    
    doc_frequency_filtered = {k:v for k, v in doc_fre_dict.items() if ((v>=min_doc_frequency) and (v <= max_doc_frequency))}
    term_frequency_filtered = {k:v for k, v in term_fre_dict.items() if ((v>=min_term_frequency) and (v <= max_term_frequency))}
    both_satisfied = {k:v for k, v in term_frequency_filtered.items() if k in doc_frequency_filtered}
    
    return both_satisfied


# In[8]:


# 빈도수로 불용어 제거 후 필터를 거친 단어들의 리스트
filtered_words = get_filtered_words(data.content)


# In[9]:


filtered_words2 = list(filtered_words.keys())
print(len(filtered_words2))
print(filtered_words2[:10])


# In[10]:


filtered_words_list = []
for i in filtered_words2:
    filtered_words_list.append(i[0])


# In[11]:


print(len(filtered_words_list))
print(filtered_words_list[:10])


# In[12]:


# unique 한 단어만 리스트로 정리
filtered_words_list_set = list(set(filtered_words_list))
print(len(filtered_words_list_set))


# In[13]:


# 기존에 정의된 불용어 사전에 있는 단어를 제거를 통해 최종 사용할 단어만 추출
final_filtered_words=[]

for i in filtered_words_list_set:
    if i not in stop_words:
        final_filtered_words.append(i)
        
print(len(final_filtered_words))


# In[14]:


#빈도수 범위 안에 있는 단어만 체택, 불용어 사전에 포함된 단어도 제거
data['cleaned'] = data.tokenized.apply(lambda x: [item for item in x if item in final_filtered_words]) 


# In[15]:


print(len(data['content'][0]))
print(len(data['tokenized'][0]))

# 모든 불용어 제거 후 토큰 수 줄어든 것 확인
print(len(data['cleaned'][0]))


# In[16]:


# 눈으로 확인
data[['tokenized', 'cleaned']].head()


# In[17]:


# detokenize
data['LatentDirichletAllocation'] = data['cleaned'].apply(' '.join)


# In[18]:


# 눈으로 확인
data[['cleaned', 'LatentDirichletAllocation']].head()


# In[19]:


lda_model = LatentDirichletAllocation(n_components=NUM_TOPICS, max_iter=10)


# In[73]:


vectorizer = CountVectorizer(min_df=100, max_df=1000)
data_vectorized = vectorizer.fit_transform(data['LatentDirichletAllocation'])


# In[74]:


lda_output = lda_model.fit_transform(data_vectorized)


# In[97]:


terms = vectorizer.get_feature_names()

def get_topics(components, feature_names, n=NUM_TOPIC_WORDS):
    f = open("total_results_test.txt", "a")
    for idx, topic in enumerate(components):
        print("Topic %d" % (idx),end="\n", file = f)
        print("단어      분포", file = f)
        print("------------------------", file = f)
        print(*[(feature_names[i], topic[i].round(10)) for i in topic.argsort()[:-n - 1:-1]], 
              sep = "\n",end="\n\n", file = f)
    f.close()


# In[98]:


get_topics(lda_model.components_,terms)


# In[ ]:




