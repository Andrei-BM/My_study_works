Папка содержащая дополнительные библиотечки для работы основного модуля.

utils.py 
- prefilter_items: функция предварительной обработки данных.

metrics.py - функции RS-метрик.
- recall_at_k: оценка полноты;
- precision_at_k: оценка точности;

recommenders.py - получение рекомендаций для модели 2-го уровня.
- get_als_recommendations: получение рекомендаций стандартными библиотеками Implicit;
- get_own_recommendations: рекомендуем товары из тех, что пользователь покупал;
- get_cosine_recommender: получение рекомендации на основе косинусной близости товаров;
- get_similar_items_recommendation: рекомендации "похожих" товаров;
- get_similar_users_recommendation: рекомендации top-N товаров среди купленных похожими пользователями.
