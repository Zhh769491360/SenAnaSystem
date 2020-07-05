# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import time

from PyQt5.QtCore import QThread, pyqtSignal
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class SenanasystemSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SenanasystemDownloaderMiddleware(object):
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


ip_list = []  # IP代理池
proxyip = ""


# class myThreadIp(QThread):
#     update_ip = pyqtSignal(str)
#
#     def run(self):
#         self.alive = True
#         while self.alive:
#             global proxyip
#             try:
#                 self.update_ip.emit(proxyip.strip("https://"))
#                 time.sleep(10)
#             except:
#                 continue

class MyRandomProxy(object):
    logger = logging.getLogger(__name__)

    def get_random_ip(self):
        f = open("./SenAnaSystem/json/ip.json", "r", encoding="utf-8")
        ip_list = json.loads(f.read())
        global proxyip
        proxyip = random.choices(ip_list)[0]["ip"]
        print("middlewares:" + proxyip)
        f.close()
        return proxyip

    def process_request(self, request, spider):
        ip = self.get_random_ip()
        request.meta['proxy'] = str(ip)

    def process_response(self, request, response, spider):
        return response


class MyUserAgent(UserAgentMiddleware):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agent=crawler.settings.get('MY_USER_AGENT'))

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        print(agent)
        request.headers['User_Agent'] = agent
