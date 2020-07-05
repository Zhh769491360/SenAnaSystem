# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import ScrapyLongItem

class CommentlongSpider(scrapy.Spider):
    name = 'comment_long_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'SenAnaSystem.pipelines.ScrapyLongPipeline': 400},
    }
    def __init__(self, movieName=None, *args, **kwargs):
        super(CommentlongSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['movie.douban.com']

        f = open("SenAnaSystem/json/movie_id.json", "r", encoding="utf-8")
        self.id = json.loads(f.read())
        f.close()
        self.start_urls = ['https://movie.douban.com/subject/' + self.id["id"] + '/reviews?start=0']  #1360
        print(self.start_urls)
        self.moviename=movieName


    def parse(self, response):
        if len(response.xpath("//div[@class='short-content']")) != 0:
            node_list = response.xpath("//div[@class='main review-item']")

            for node in node_list:
                item = ScrapyLongItem()
                condition_1 = node.xpath("./header[@class='main-hd']/span[@class='allstar10 main-title-rating' or @class='allstar20 main-title-rating']/@title")
                condition_2 = node.xpath("./header[@class='main-hd']/span[@class='allstar40 main-title-rating' or @class='allstar50 main-title-rating']/@title")
                base = node.xpath("./div[@class='main-bd']/div[@class='review-short']/div[@class='short-content']/text()")
                str = base.extract()[0]
                # [:-1],[:-3]对爬取的评论进行处理，[:-1]去除"("  [:-3]去除"..."
                if len(condition_1) > 0:
                    if str.strip() == "":
                        item['commentNeg'] = base.extract()[1][:-1].strip()[:-3]
                    else:
                        item['commentNeg'] = str[:-1].strip()[:-3]
                elif len(condition_2) > 0:
                    if str.strip() == "":
                        item['commentPos'] = base.extract()[1][:-1].strip()[:-3]
                    else:
                        item['commentPos'] = str[:-1].strip()[:-3]
                else:
                    item['commentMid'] = "NULL"
                yield item
            try:
                li = response.xpath("//link[@rel='next']/@href").extract()[0]
                url = "https://movie.douban.com/subject/" + self.id["id"] + "/reviews" + li
                yield scrapy.Request(url, callback=self.parse)
            except Exception as e:
                print(e+",未找到评论!")