# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from cnblog.items import CnblogItem
import re


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # self.db[CnblogItem.collection].create_index([])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[CnblogItem.collection].insert_one(item)
        return item


class CnblogPipeline(object):
    def process_item(self, item, spider):
        if item['release_time']:
            item['release_time'] = item['release_time'].replace('发布于', '').strip()
        if item['view']:
            item['view'] = re.match('.*?(\d+).*?', item['view']).group(1)
        if item['comments']:
            item['comments'] = re.match('.*?(\d+).*?', item['comments']).group(1)
        return item
