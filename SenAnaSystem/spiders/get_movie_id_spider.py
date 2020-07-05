# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import ScrapyGetIdItem

class GetMovieIdSpider(scrapy.Spider):
    name = 'get_movie_id_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'SenAnaSystem.pipelines.ScrapyGetIdPipeline': 200},
    }
    def __init__(self, movieName=None, *args, **kwargs):
        super(GetMovieIdSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['movie.douban.com']
        self.start_urls = ['https://movie.douban.com/j/subject_suggest?q=' + movieName]
        self.moviename = movieName
        print(self.start_urls)

    def parse(self, response):
        # if response.body.decode("utf-8")==[]:
        #     scrapy.Request(self.start_urls, callback=self.parse)
        # print(response.body)
        # print(response.body.decode("utf-8"))
        data = json.loads(response.body.decode("utf-8"))    # 转为字典格式
        print(data)
        # print(data)
        key = True
        for i in range(len(data)):
            if data[i]["title"] == self.moviename and key:
                item = ScrapyGetIdItem()
                item['id'] = data[i]["id"]
                print(data[i]["id"])
                key = False
                yield item
