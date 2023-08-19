#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


# In[ ]:


def recall_at_k(recommended_list, bought_list, k=5):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)[:k]
    flag = np.isin(bought_list, recommended_list)
    recall =  flag.sum()/len(bought_list)
        
    return recall


# In[ ]:


def precision_at_k(recommended_list, bought_list, k=5):
    bought_list = np.array(bought_list)
    
    recommended_list = np.array(recommended_list)[:k]
    
    flags = np.isin(bought_list, recommended_list)
    
    precision = flags.sum() / len(recommended_list)
    
    return precision

