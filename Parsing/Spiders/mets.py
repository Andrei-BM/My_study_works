import scrapy
import os
from scrapy.http import HtmlResponse
from kino_yandex.items import KinoYandexItem
from scrapy.loader import ItemLoader
from Parsing import my_env

class MetsSpider(scrapy.Spider):

    category = dict(car='kvaSpis?g=1',
                    home='kvaSpis?g=2',
                    land='kvaSpis?g=4',
                    business='kvaSpis?g=3',
                    other='kvaSpis?g=6')
    name = 'mets'
    allowed_domains = ['m-ets.ru']
    start_urls = ['https://m-ets.ru/']
    my_login = os.environ.get('mets_login')
    my_pass = os.environ.get('mets_pass')
    auth_url = 'https://m-ets.ru/authorize'
    link_list = []

    # Задаём параметр search для выбора категории поиска при создании паука.
    def __init__(self, search='home', **kwargs):
        super(MetsSpider, self).__init__(**kwargs)
    # Создаём ссылку в зависимости от выбора категории.
        self.parse_link = self.category[search]
        self.search = search

    def parse(self, response):
    # После ответа на запрос главной страницы сайта, производим авторизацию.
        yield scrapy.FormRequest(self.auth_url,
                method='POST',
                callback=self.auth_pass,
                formdata={"uri": '',
                          "login": self.my_login,
                          "password": self.my_pass,})


    def auth_pass(self, response:HtmlResponse):
        # Переход на первую страницу для парсинга.
        yield response.follow(self.parse_link, callback=self.page_parse)

    def page_parse(self, response:HtmlResponse):
        # Создаём список страниц для парсинга категории поиска.
        if not self.link_list:
            self.link_list = response.xpath('//div[@class = "search-results__block"]/a/@href').getall()
        # Собираем первую страницу.
        item_list = response.xpath('//div[@class = "group5-a-wrap"]/a/@href').getall()
        for item in item_list:
            yield response.follow(item, callback=self.item_parse)
        # Проходим по остальным страницам в этом же методе.
        for link in self.link_list:
            yield response.follow(link, callback=self.page_parse)



    def item_parse(self, response:HtmlResponse):
        # Собираем информации со странички объекта торгов.
        loader = ItemLoader(item = KinoYandexItem(), response=response)
        loader.add_value('item_link', response.url)
        loader.add_value('item_photo_link', self.start_urls[0])
        loader.add_xpath('item_name', '//h1/text()')
        loader.add_xpath('item_description', '//h2[@class = "sved"]/text() | //h1/text()')
        loader.add_xpath('item_region', '//div[@class = "sved"]/a/text()')
        loader.add_xpath('item_price', '//div[@class = "sved"]/span/text()')
        loader.add_xpath('item_photo_link', '//td[@class = "lot__info_full-photo-wrapper"]/a/@href | //div[@class = "photo-gallery"]/a/@href')
        loader.add_value('item_origin', self.name)
        loader.add_value('item_category', self.search)
        yield loader.load_item()