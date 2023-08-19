# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http import HtmlResponse
from scrapy import signals
from scrapy.utils.python import without_none_values


# from selenium.webdriver.common.service import Service
# path_to_driver = Service('C:\\Study\\Parsing\\hometask_8\\chromedriver.exe')


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class KinoYandexSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        # opts = Options()
        # opts.add_argument('headless')
        # # assert not opts.headless
        # driver = webdriver.Chrome('C:\\Study\\Parsing\\hometask_8\\chromedriver.exe', chrome_options=opts)

        for r in start_requests:
            # driver.get(r.url)
            # body = driver.page_source
            yield r #HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=r)

        # driver.close()

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KinoYandexDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# class KinoYandexDefaultHeadersMiddleware:
#
#     def __init__(self, headers):
#         self._headers = headers
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         headers = without_none_values(crawler.settings['DEFAULT_REQUEST_HEADERS'])
#         return cls(headers.items())
#
#     def process_request(self, request, spider):
#         for k, v in self._headers:
#             request.headers.setdefault(k, v)

# class JSMiddleware(object):
#
#
#     def process_request(self, request, spider):
#         if spider.auth_url != request.url:
#             opts = Options()
#             opts.add_argument('start-maximized')
#             opts.add_experimental_option("useAutomationExtension", False)
#             opts.add_experimental_option("excludeSwitches", ["enable-automation"])
#             opts.add_argument('--disable-blink-features=AutomationControlled')
#             opts.add_argument('User-Agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
#             # opts.add_argument('headless')
#             # assert not opts.headless
#             driver = webdriver.Chrome('C:\\Study\\Parsing\\hometask_8\\chromedriver.exe', chrome_options=opts)
#             driver.get(request.url)
#             body = driver.page_source
#
#             return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
#             driver.close()
#         else:
#             pass
