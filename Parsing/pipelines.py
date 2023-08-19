# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class KinoYandexPipeline:

    def __init__(self):
        self.client = MongoClient('127.0.0.1:27017')
        self.mongo_db = self.client['Public_trade']

    def process_item(self, item, spider):
        data_unit = dict(описание=item['item_description'], ссылка=item['item_link'],
                         фото=item['item_photo_link'], цена=item['item_price'], регион=item['item_region'],
                         площадка=item['item_origin'], название=item['item_name'])
        print(data_unit)
        self.mongo_db[item['item_category']].insert_one(data_unit)
        return item
