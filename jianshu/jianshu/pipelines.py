# -*- coding: utf-8 -*-
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JianshuPipeline(object):
    def __init__(self):
        client=pymongo.MongoClient('localhost',27017)
        mydb=client['mydb']
        jianshu=mydb['jianshu']
        self.post=jianshu
    def process_item(self, item, spider):
        d=dict(item)
        self.post.insert(d)
        return item
