# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ChengyuspiderPipeline(object):

    collection_name = 'chengyu_detail'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 从crawler获取mongodb配置
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        # 初始化mongodb连接
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 关闭mongodb连接
        self.client.close()

    def process_item(self, item, spider):
        try:
            # 插入爬取数据
            self.db[self.collection_name].insert(dict(item))
            print('数据插入成功')
        except Exception as err:
            print('插入数据失败', err)
        return item
