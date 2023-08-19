#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[11]:


def prefilter_items(data, item_features, take_n_popular=5000):
    # Уберем самые популярные товары (их и так купят)
    popularity = data.groupby('item_id')['user_id'].nunique().reset_index()
    popularity['share_unique_users'] = popularity['user_id']/data['user_id'].nunique()
    popularity.drop(columns=['user_id'], axis=1, inplace=True)
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(top_popular)]
        
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.004].item_id.tolist()
    data = data[~data['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    live_item = data[(data['week_no'] <= data['week_no'].max()) & (data['week_no'] > data['week_no'].max() - 52)]['item_id'].unique()
    data = data[data['item_id'].isin(live_item)]
    
    # Уберем не интересные для рекоммендаций категории (department)
    item_features.columns = [col.lower() for col in item_features.columns]
    item_features.rename(columns={'product_id': 'item_id'}, inplace=True)
    not_intresting_cat = ['VIDEO RENTAL', ' ', 'PHARMACY SUPPLY', 'KIOSK-GAS', 'ELECT &PLUMBING', 'GM MERCH EXP']
    not_intresting_item = item_features.loc[(item_features['department'].isin(not_intresting_cat)), 'item_id'].tolist()
    data = data[~data['item_id'].isin(not_intresting_item)]
        
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    # min - 0.99
    data['price'] = data['sales_value'] / (np.maximum(data['quantity'], 1))
    rec_price = data.groupby('item_id')['price'].mean().reset_index()
    rec_price.rename(columns={'price': 'mean_price'}, inplace=True)
    low_price = rec_price.loc[(rec_price['mean_price'] < 1), 'item_id'].unique().tolist()
    data = data[~data['item_id'].isin(low_price)]
    # Отберём 5000 самых популярных товаров
    popular = data.groupby('item_id')['quantity'].sum().reset_index()
    popular.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top = popular.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.to_list()
    # data.loc[~data['item_id'].isin(top), 'item_id'] = 999999
    data = data.loc[data['item_id'].isin(top)]
    
    return data

