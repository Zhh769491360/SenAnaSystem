# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ScrapyShortPipeline(object):
    def __init__(self):
        f = open("./SenAnaSystem/json/movie_name.json", "r", encoding="utf-8")
        moviename = json.loads(f.read())
        f.close()

        self.f1 = open("./SenAnaSystem/json/" + moviename["movieName"] + "/comment_short_pos.json", "w",
                       encoding="utf-8")
        self.f2 = open("./SenAnaSystem/json/" + moviename["movieName"] + "/comment_short_neg.json", "w",
                       encoding="utf-8")

    def process_item(self, item, spider):
        dic = dict(item)
        content = json.dumps(dic, ensure_ascii=False) + ",\n"
        if dic.get("commentPos", "error") != "error":
            self.f1.write(content)
        elif dic.get("commentNeg", "error") != "error":
            self.f2.write(content)
        return item

    def close_spider(self, spider):
        self.f1.close()
        self.f2.close()

class ScrapyLongPipeline(object):
    def __init__(self):
        f = open("./SenAnaSystem/json/movie_name.json", "r", encoding="utf-8")
        moviename = json.loads(f.read())
        f.close()

        self.f1 = open("./SenAnaSystem/json/" + moviename["movieName"] + "/comment_long_pos.json", "w",
                       encoding="utf-8")
        self.f2 = open("./SenAnaSystem/json/" + moviename["movieName"] + "/comment_long_neg.json", "w",
                       encoding="utf-8")

    def process_item(self, item, spider):
        dic = dict(item)
        content = json.dumps(dic, ensure_ascii=False) + ",\n"
        if dic.get("commentPos", "error") != "error":
            self.f1.write(content)
        elif dic.get("commentNeg", "error") != "error":
            self.f2.write(content)
        return item

    def close_spider(self, spider):
        self.f1.close()
        self.f2.close()

class ScrapyGetIdPipeline(object):
    def __init__(self):
        self.f = open("./SenAnaSystem/json/movie_id.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()