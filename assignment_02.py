#!/usr/bin/env python
# coding: utf-8

# In[7]:


# 
# Python은 화면에 쉽게 그림을 그릴 수 있는 Turtle Graphic을 지원합니다.
# 거북이가 화면 가운데를 출발해서 선 80개를 소라 모양으로 그리도록 프로그램을 작성하십시오. 
# 선의 색상은 무작위로 선택합니다. 
# 선의 길이는 5에서 시작해 1씩 증가하게 하고, 각도는 30도씩 회전시킵니다.

# In[8]:


import turtle
import random


# In[11]:


swidth, sheight = 350, 350
r, g, b, angle, dist, = 0, 0, 0, 30, 5 

turtle.title('Assignment 02')
turtle.shape('turtle')
turtle.setup(width = swidth + 30, height = sheight + 30)
turtle.screensize(swidth, sheight)
turtle.pensize(3)

for i in range(80) :
    r = random.random()
    g = random.random()
    b = random.random()
    turtle.pencolor((r, g, b))

    dist += 1 
    turtle.forward(dist)
    turtle.left(angle) 

turtle.done()


# In[ ]:




