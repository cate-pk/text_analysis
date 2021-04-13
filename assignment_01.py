#!/usr/bin/env python
# coding: utf-8

# In[1]:




# ## Exercise 4
# Create a dictionary variable that saves
# - Take input from a user {'Tom':20} (name: age pair)
# - Return Tom's age.
# - Add another person's age information: John, 30
# - Return the number of keys
# - Update the dictionary variable with another dictionary variable which is {'Sarah': 28, 'Jack': 41}
# - Return the keys of the updated dictionary variable

# In[2]:


# Take input from a user {'Tom':20} (name: age pair)

dict1 = {'Tom': 20}


# In[3]:


# Return Tom's age

dict1['Tom']


# In[4]:


# Add another person's age information: John, 30

dict1['John'] = 30
dict1


# In[5]:


# Return the number of keys

len(dict1)


# In[6]:


# Update the dictionary variable with another dictionary variable which is {'Sarah': 28, 'Jack': 41}

dict1.update({'Sarah': 28, 'Jack': 41})
dict1


# In[7]:


# Return the keys of the updated dictionary variable

dict1.keys()


# ## Exercise 5
# Python 에서 제공하는 다음 각 데이터 기본 크기를 화면에 출력하는 프로그램을 작성하시오
# - Integer, float, Boolean, string, list, dictionary, set.

# In[8]:


import sys

dt = {"Integer": int(), "float": float(), "Boolean": bool(), 
      "string": str(), "list": list(), "dictionary": dict(), "set": set()}

for k, v in dt.items():
    print('{} 데이터의 기본 크기: {} bytes'.format(k, sys.getsizeof(v)))


# In[ ]:




