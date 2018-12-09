# -*- coding: utf-8 -*-

# Define your item pipelines 141111111111111141231241211
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ZxsdisnoPipeline(object):

    def __init__(self, db_url, db_name, db_user_name, db_password):
        self.db_url = db_url
        self.db_name = db_name
        self.db_user_name = db_user_name
        self.db_password = db_password

        self.db = pymysql.connect(host=self.db_url, db=self.db_name, user=self.db_user_name, password=self.db_password)

    @classmethod
    def from_crawler(cls, crawler):
        print("crawler")
        return cls(
            db_url=crawler.settings.get('MYSQL_HOST'),
            db_name=crawler.settings.get('MYSQL_DBNAME'),
            db_user_name=crawler.settings.get('MYSQL_USER'),
            db_password=crawler.settings.get('MYSQL_PASSWD'),
        )

    def open_spider(self, spider):
        cursor = self.db.cursor()
        sql = 'select discount_id from tb_discount where discount_id=337'
        cursor.execute(sql),
        results = cursor.fetchall()
        spider.myurls = results[0][0]

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        num = spider.count
        print(num, '========================---------------000000099999999999999999999')
