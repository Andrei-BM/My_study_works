Проект парсинга сайта электронных торгов МЭТС. (https://m-ets.ru)
Модуль авторизуется на сайте просматривает лоты по заданной категории и добавляет данные в базу данных.

SPIDER

При запуске паука "scrapy crawl mets" с помощью параметра search можно задать категорию поиска объектов. "scrapy crawl mets -a search=car"
Возможные варианты параметра search:
- car - поиск автотранспорта
- home - недвижимость для личных целей
- land - земельные участки
- business - лоты для бизнеса
- other - прочие лоты.
Если параметр search не указан при запуске паука, поиск будет производится по категории (home) недвижимость для личных целей.

ITEMS

При инициализации объектов задаются методы обработки полученной пауком информации.
item_name - название предмета торгов;
item_link - ссылка на страничку лота;
item_region - название субъекта РФ, месторасположение объекта торгов;
item_price - цена лота;
item_description - подробное описание(может отсутствовать на странице в т.с. заменяется на название)
item_photo_link - список ссылок на фотографии объекта торгов;
item_origin - название торговой площадки;
item_category - категория про которой производился поиск. Используется для определения коллекции в которую нужно помещать объекты поиска.

PIPELINES

Открываем базу данных и записываем в неё результаты поиска. 
