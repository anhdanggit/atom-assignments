#!/usr/bin/env python
# coding: utf-8

# In[13]:


import json


# In[18]:


email_data= '{"email": {"SENDER_EMAIL":"chuviethong.vn@gmail.com","PWD_EMAIL":"sachhbgmhpzhbbzh","WEATHER_API_KEY":"7344e7a3019d9e968f588eb950eba78c"}}'
dict_obj = json.loads(email_data)
print(dict_obj)
print("Type of dict_obj", type(dict_obj))
print("EMAIL......",  dict_obj.get('email'))


# In[ ]:




