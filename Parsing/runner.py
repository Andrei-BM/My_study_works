from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings, project_data_dir
from kino_yandex.spiders.mets import MetsSpider



if __name__ == '__main__':

    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    runner.crawl(MetsSpider, search='home')

    reactor.run()