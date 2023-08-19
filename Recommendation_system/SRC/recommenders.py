#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

# Для работы с матрицами
from scipy.sparse import csr_matrix

# Матричная факторизация
from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import ItemItemRecommender, CosineRecommender  # нужен для одного трюка
from implicit.nearest_neighbours import bm25_weight, tfidf_weight

# from src.utils import prefilter_items

class MainRecommender:
    """Рекоммендации, которые можно получить из ALS
    
    Input
    -----
    user_item_matrix: pd.DataFrame
        Матрица взаимодействий user-item
    """
    
    def __init__(self, data, item_features, weighting='bm25'):
        
        # your_code. Это не обязательная часть. Но если вам удобно что-либо посчитать тут - можно это сделать
        # Топ покупок каждого юзера
        self.top_purchases = data.groupby(['user_id', 'item_id'])['quantity'].count().reset_index()
        self.top_purchases.sort_values('quantity', ascending=False, inplace=True)
        self.top_purchases = self.top_purchases[self.top_purchases['item_id'] != 999999]
        
        # Топ покупок по всему датасету
        self.overall_top_purchases = data.groupby('item_id')['quantity'].count().reset_index()
        self.overall_top_purchases.sort_values('quantity', ascending=False, inplace=True)
        self.overall_top_purchases = self.overall_top_purchases[self.overall_top_purchases['item_id'] != 999999]
        self.overall_top_purchases = self.overall_top_purchases.item_id.tolist()
        
        # Делаем матрицу user_item (из уже подготовленного df функцией prefilter)
        self.user_item_matrix = self.prepare_matrix(data)
        self.user_ii_matrix = self.user_item_matrix.copy()
        self.user_ii_matrix[self.user_ii_matrix > 0] = 1
        self.sparse_user_item = csr_matrix(self.user_item_matrix).tocsr()
        
        # Словари
        self.id_to_itemid, self.id_to_userid, self.itemid_to_id, self.userid_to_id = self.prepare_dicts(self.user_item_matrix)
        
        # Взвешивание
        if weighting == 'bm25':
            self.user_item_matrix = bm25_weight(self.user_item_matrix.T, K1=100, B=0.85).T.tocsr() 
        elif weighting == 'tfidf':
            self.user_item_matrix = tfidf_weight(self.user_item_matrix).tocsr() 
        
        self.model = self.fit(self, self.user_item_matrix)
        self.own_recommender = self.fit_own_recommender(self, self.user_ii_matrix)
        self.cosine_recommender = self.fit_cosine_recommender(self, self.user_item_matrix)
        
        # Сводная таблица товаров купленных пользователем сортировка по количеству
        self.popularity = self.make_popularity(data)
        
        # Переменные характеристик товаров
        self.categories_with_own_items, self.own_items_index = self.item_featuring(self, item_features)
        self.item_features = item_features 
        # self.filter_items = [self.itemid_to_id[999999]]
        self.filter_items = []
        
    @staticmethod
    def prepare_matrix(data):
        user_item_matrix = pd.pivot_table(data, 
                                  index='user_id', columns='item_id', 
                                  values='sales_value', # Можно пробовать другие варианты
                                  aggfunc='sum', 
                                  fill_value=0)

        user_item_matrix = user_item_matrix.astype(float)
        
        return user_item_matrix
    
    @staticmethod
    def prepare_dicts(user_item_matrix):
        """Подготавливает вспомогательные словари"""
        
        userids = user_item_matrix.index.values
        itemids = user_item_matrix.columns.values

        matrix_userids = np.arange(len(userids))
        matrix_itemids = np.arange(len(itemids))

        id_to_itemid = dict(zip(matrix_itemids, itemids))
        id_to_userid = dict(zip(matrix_userids, userids))

        itemid_to_id = dict(zip(itemids, matrix_itemids))
        userid_to_id = dict(zip(userids, matrix_userids))
        
        return id_to_itemid, id_to_userid, itemid_to_id, userid_to_id
     
    @staticmethod
    def fit_own_recommender(self, user_ii_matrix):
        """Обучает модель, которая рекомендует товары, среди товаров, купленных юзером"""
    
        model = ItemItemRecommender(K=2, num_threads=0)
        model.fit(csr_matrix(self.user_ii_matrix).tocsr())
        
        return model
    
    @staticmethod
    def fit(self, user_item_matrix, n_factors=150, regularization=0.002, alpha=0.1, iterations=20, num_threads=0):
        """Обучает ALS"""
        
        model = AlternatingLeastSquares(factors=n_factors, 
                                             regularization=regularization,
                                             alpha=alpha,
                                             iterations=iterations,  
                                             num_threads=num_threads,
                                             random_state=5)
        model.fit(self.user_item_matrix)
        
        return model
    
    @staticmethod
    def fit_cosine_recommender(self, user_item_matrix):
        """ Обучает модель на основе косинусной близости"""
        model = CosineRecommender(K=5, num_threads=0)
        model.fit(csr_matrix(user_item_matrix).tocsr(),
                  show_progress=True)
        return model
        
    
#     def _update_dict(self, user_id):
#         """Если появился новый user / item, то нужно обновить словари """
#         flag = True
#         if user_id not in self.userid_to_id.keys():
            
#             max_id = max(list(self.userid_to_id.values()))
#             max_id += 1
            
#             self.userid_to_id.update({user_id: max_id})
#             self.id_to_userid.update({max_id: user_id})
#             flag = False
#         return flag
            
    def _get_similar_item(self, item_id):
        """Находит товар, похожий на item_id"""
        recs = self.model.similar_items(self.itemid_to_id[item_id], N=2)
        top_rec = recs[1][0]
        return self.id_to_itemid[top_rec]
    
    def _extend_with_top_popular(self, recommendations, N=5):
        """Если количество рекомендаций < N, то дополняем их топ-популярным """
        
        if len(recommendations) < N:
            top_popular = [rec for rec in self.overall_top_purchases[:N] if rec not in recommendations]
            recommendations.extend(top_popular)
            recommendations = recommendations[:N]
            
        return recommendations
    
    def _get_recommendations(self, user, model, N):
        """Рекомендации через стандартные библиотеки implicit"""
        
        
        res = model.recommend(userid=user,
                              user_items=self.sparse_user_item[user],
                              N=N,
                              filter_already_liked_items=False,
                              filter_items=self.filter_items,
                              recalculate_user=True)
        
        mask = res[1].argsort()[::-1]
        
        res = [self.id_to_itemid[rec] for rec in res[0][mask]]
        res = self._extend_with_top_popular(res, N=N)
    
        assert len(res) == N, 'Количество рекомендаций != {}'.format(N)
        return res
    
    def get_als_recommendations(self, user, N=5):
        """Рекомендации через стандартные библиотеки implicit"""
        
        if user in self.userid_to_id.keys():
            user_id = self.userid_to_id[user]
            return self._get_recommendations(user_id, model=self.model, N=N)
        else:
            return self._extend_with_top_popular([], N=N)
    
    def get_own_recommendations(self, user, N=5):
        """Рекомендуем товары среди тех, которые юзер уже купил."""
        
        
        if user in self.userid_to_id.keys():
            user = self.userid_to_id[user]
            res = self.own_recommender.recommend(userid=user,
                              user_items=self.sparse_user_item[user],
                              N=N,
                              filter_already_liked_items=False,
                              filter_items=self.filter_items,
                              recalculate_user=False)
            mask = res[1].argsort()[::-1]
            res = [self.id_to_itemid[rec] for rec in res[0][mask]][:N]
            res = self._extend_with_top_popular(res, N=N)
        else:
            res = self._extend_with_top_popular([], N=N)
    
        assert len(res) == N, 'Количество рекомендаций != {}'.format(N)
        return res
    
    def get_cosine_recommender(self, user, N=5):
        """ Рекомендуем товары на основе косинусной близости"""
        if user in self.userid_to_id.keys():
            user = self.userid_to_id[user]
            res = self.cosine_recommender.recommend(userid=user,
                              user_items=self.sparse_user_item[user],
                              N=N,
                              filter_already_liked_items=False,
                              filter_items=self.filter_items,
                              recalculate_user=False)
            mask = res[1].argsort()[::-1]
            res = [self.id_to_itemid[rec] for rec in res[0][mask]][:N]
            return res
        else:
            return []
        
    @staticmethod
    def make_popularity(data):
        popularity = data.groupby(['user_id', 'item_id'])['quantity'].count().reset_index()
        popularity.sort_values('quantity', ascending=False, inplace=True)
        popularity = popularity[popularity['item_id'] != 999999]
        
        return popularity
    
    @staticmethod
    def item_featuring(self, item_features):
        top_features = item_features[item_features['item_id'].isin(self.itemid_to_id.keys())]
        categories_with_own_items = top_features[top_features['brand'] == 'Private']['department'].unique().tolist()
        
        own_items = top_features[top_features['brand'] == 'Private'].item_id.tolist()
        own_items_index = [self.itemid_to_id[el] for el in own_items]
        
        return categories_with_own_items, own_items_index

    def get_similar_items_recommendation(self, user, N=5):
        """Рекомендуем товары, похожие на топ-N купленных юзером товаров
        Возвращает уже список товаров с оригинальным item_id"""
        if user in self.userid_to_id.keys():
            recs = []
            # filter_items = [self.itemid_to_id[999999]]
            # Переводим id пользователя
            # user = self.userid_to_id[user]
        
            # Из сводной таблицы выбираем 5 лучших товаров купленных пользователем (сортировка по количеству купленных)
            for el in self.popularity.loc[(self.popularity['user_id'] == user), 'item_id'][:N].tolist():
            
            # Проверяем есть ли товар в категории где у нас СТМ(собственные торговые марки)
                if self.item_features.loc[(self.item_features['item_id'] == el)]['department'].values in self.categories_with_own_items:
                    answer = self.model.similar_items(self.itemid_to_id[el], N=3)[0][1:]
                
                # Проверяем есть ли среди рекомендованых товары СТМ
                    check = [i for i in answer if i in self.own_items_index]
                    recs.append(check[0]) if len(check) >= 1 else recs.append(answer[0])
            
                else:
                    recs.append(self.model.similar_items(self.itemid_to_id[el], N=2, filter_items=self.filter_items)[0][1])
            recs = [self.id_to_itemid[rec] for rec in recs]
            recs = self._extend_with_top_popular(recs, N=N)
        else:
            recs = self._extend_with_top_popular([], N=N)
        assert len(recs) == N, 'Количество рекомендаций != {}'.format(N)
        return recs
    
    def get_similar_users_recommendation(self, user, N=5):
        """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
        
        if user in self.userid_to_id.keys():
            user = self.userid_to_id[user]
            result = []
            restricted_items = [self.itemid_to_id[999999]]
            list_users = self.model.similar_users(user, N=N+1)[0][1:]
            for el in list_users:
                result.append(self.model.recommend(userid=el, 
                                                       user_items=self.sparse_user_item[el],
                                                       N=1, 
                                                       filter_already_liked_items=False, 
                                                       filter_items=restricted_items, 
                                                       recalculate_user=True)[0][0])
                restricted_items.append(result[-1])
                                        
            res = [self.id_to_itemid[el] for el in result]
            res = self._extend_with_top_popular(res, N=N)
        else:
            res = self._extend_with_top_popular([], N=N)
        assert len(res) == N, 'Количество рекомендаций != {}'.format(N)
        
        return res

