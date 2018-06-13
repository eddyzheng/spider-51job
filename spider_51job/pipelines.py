# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class Spider51JobPipeline(object):

    def open_spider(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = client.job51
        pass

    def close_spider(self):
        pass
    def process_item(self, item, spider):
        print '----pipline---'
        collection = self.db.list
        collection.insert(item)
        return item
