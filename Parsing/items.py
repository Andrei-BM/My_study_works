# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose, Identity

# Функци очистики описания.
def clean_description(obj: list):
    return ' '.join(obj[0].split())

# Функция очистки названия.
def clean_name(obj: list):
    return ' '.join(obj[0].split()).split(sep=',')[0]

# Функция очистик поля "цена".
def clean_price(obj: list):
    return int(''.join(obj[0].split())[:-4])

# Функция созадния ссылок на фото объекта.
def join_links(obj: list):
    return [obj[0] + el for el in obj[1:]]


class KinoYandexItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field(input_processor=TakeFirst(), output_processor=Compose(clean_name))
    item_link = scrapy.Field(output_processor=TakeFirst())
    item_region = scrapy.Field(input_processor=Compose(lambda x: x[-1]), output_processor=TakeFirst())
    item_price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    item_description = scrapy.Field(output_processor=Compose(clean_description))
    item_photo_link = scrapy.Field(output_processor=Compose(join_links))
    item_origin = scrapy.Field(output_processor=TakeFirst())
    item_category = scrapy.Field(output_processor=TakeFirst())
