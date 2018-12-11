# -*- coding: utf-8 -*-

# Define your item pipelines 141111111111111141231241211
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import operator


class ZxsdisnoPipeline(object):

    def __init__(self, db_url, db_name, db_user_name, db_password):
        self.db_url = db_url
        self.db_name = db_name
        self.db_user_name = db_user_name
        self.db_password = db_password
        db = pymysql.connect(host=self.db_url, db=self.db_name, user=self.db_user_name, password=self.db_password)
        self.cursor = db.cursor()
        self.wordF = None
        self.wordAttrF = None
        self.articleF = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.settings.get('MYSQL_HOST'),
            db_name=crawler.settings.get('MYSQL_DBNAME'),
            db_user_name=crawler.settings.get('MYSQL_USER'),
            db_password=crawler.settings.get('MYSQL_PASSWD'),
        )

    def open_spider(self, spider):
        sql = 'select article_id, \'ard\' from tb_article where status=3 and is_publish = 0 and attr = 1  limit 0,20'
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.article = results

        sql = 'select word_code, \'wd\' from tb_word where status=3 and is_publish = 0 and word_id >0 and word_id<=10'
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.word = results

        sql = (
            'select word_attr_code ,\'wdr\' '
            'from tb_word word left join tb_word_attr wordAttr on word.word_id = wordAttr.word_id '
            'where word.status=3 and word.is_publish = 0 and word.word_id >0 and word.word_id<=4'
        )
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.wordAttr = results

        self.wordF = open(r'C:\Users\13671\Desktop\word.txt', 'w')
        self.wordAttrF = open(r'C:\Users\13671\Desktop\wordAttr.txt', 'w')
        self.articleF = open(r'C:\Users\13671\Desktop\article.txt', 'w')

    def process_item(self, item, spider):
        if '无内容' in item['body']:
            path = item["path"]
            if 'wdr' in path:
                self.wordAttrF.write(f'{item["body"]}==={item["path"]}')
                self.wordAttrF.write("\n")
            elif 'ard' in path:
                self.articleF.write(f'{item["body"]}==={item["path"]}')
                self.articleF.write("\n")
            else:
                self.wordF.write(f'{item["body"]}==={item["path"]}')
                self.wordF.write("\n")
        return item

    def close_spider(self, spider):
        self.wordF.write(f'count:{spider.wordCount}   ')
        self.wordF.write(f'nocount;{spider.noWordCount}   ')
        self.wordF.write(f'allcount;{len(spider.word)}')
        self.wordF.write("\n")

        self.wordAttrF.write(f'count:{spider.wordAttrCount}   ')
        self.wordAttrF.write(f'nocount;{spider.noWordAttrCount}   ')
        self.wordAttrF.write(f'allcount;{len(spider.wordAttr)}')
        self.wordAttrF.write("\n")

        self.articleF.write(f'count:{spider.articleCount}   ')
        self.articleF.write(f'nocount;{spider.noArticleCount}   ')
        self.articleF.write(f'allcount;{len(spider.article)}')
        self.articleF.write("\n")

        self.wordF.close()
        self.wordAttrF.close()
        self.articleF.close()
        self.cursor.close()
