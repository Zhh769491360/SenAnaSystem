# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import ScrapyShortItem
class CommentshortSpider(scrapy.Spider):
    name = 'comment_short_spider'
    custom_settings = {
        'ITEM_PIPELINES': {'SenAnaSystem.pipelines.ScrapyShortPipeline': 300},
    }
    def __init__(self, movieName=None, *args, **kwargs):
        super(CommentshortSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ['movie.douban.com']

        f = open("SenAnaSystem/json/movie_id.json", "r", encoding="utf-8")
        self.id = json.loads(f.read())
        f.close()
        self.start_urls = ['https://movie.douban.com/subject/' + self.id["id"] + '/comments?start=0&limit=20&sort=new_score&status=P']
        print(self.start_urls)

        self.moviename=movieName

    def parse(self, response):
        if len(response.xpath("//span[@class='short']")) != 0:
            node_list = response.xpath("//div[@class='comment']")

            for node in node_list:
                item = ScrapyShortItem()
                condition_1 = node.xpath("./h3/span[@class='comment-info']/"
                                         "span[@class='allstar10 rating' or @class='allstar20 rating']/@title")
                condition_2 = node.xpath("./h3/span[@class='comment-info']/"
                                         "span[@class='allstar40 rating' or @class='allstar50 rating']/@title")
                if len(condition_1) > 0:
                    item['commentNeg'] = node.xpath("./p/span/text()").extract()[0]
                elif len(condition_2) > 0:
                    item['commentPos'] = node.xpath("./p/span/text()").extract()[0]
                else:
                    item['commentMid'] ="NULL"
                yield item
            try:
                li = response.xpath("//a[@class='next']/@href").extract()[0].split("&")
                url = "https://movie.douban.com/subject/" + self.id["id"] + "/comments" \
                      + li[0] + "&" \
                      + li[1] + "&" \
                      + li[2] + "&" \
                      + li[3]
                if int(li[0].split("=")[1]) != 220:
                    yield scrapy.Request(url, callback=self.parse)
            except Exception as e:
                print(e+",未找到评论!")