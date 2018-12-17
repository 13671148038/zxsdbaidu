# -*- coding: utf-8 -*-

# Define your item pipelines 141111111111111141231241211
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ZxsdisnoPipeline(object):

    def __init__(self, db_url, db_name, db_user_name, db_password, *args, **kwargs):
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
        # 获取文章
        sql = 'select article_id, \'ard\' from tb_article where status=3 and is_publish = 0 and attr = 1'
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.article = results

        # 获取聚合词条    warb端是goodclassid
        sql = 'select word_code, \'wd\' from tb_word where status=3 and is_publish = 0'
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.word = results

        # 获取词条        war端是频道加栏目加id加/1
        sql = (
            'select word_attr_code ,\'wdr\' '
            'from tb_word word left join tb_word_attr wordAttr on word.word_id = wordAttr.word_id '
            'where word.status=3 and word.is_publish = 0'
        )
        self.cursor.execute(sql),
        results = self.cursor.fetchall()
        spider.wordAttr = results

        # self.wordF = open(r'C:\Users\13671\Desktop\word.txt', 'w')
        # self.wordAttrF = open(r'C:\Users\13671\Desktop\wordAttr.txt', 'w')
        # self.articleF = open(r'C:\Users\13671\Desktop\article.txt', 'w')
        self.wordF = open(r'/usr/local/lib/python3.5/site-packages/scrapyd/dbs/logs/zxsdisno/demo/word.txt', 'w')
        self.wordAttrF = open(r'/usr/local/lib/python3.5/site-packages/scrapyd/dbs/logs/zxsdisno/demo/wordAttr.txt', 'w')
        self.articleF = open(r'/usr/local/lib/python3.5/site-packages/scrapyd/dbs/logs/zxsdisno/demo/article.txt', 'w')

    def process_item(self, item, spider):
        if '无内容aaa' in item['body']:
            path = item["path"]
            if 'wdr' in path:
                self.wordAttrF.write('{0}==={1}'.format(item["body"], item["path"]))
                self.wordAttrF.write("\n")
            elif 'ard' in path:
                self.articleF.write('{0}==={1}'.format(item["body"], item["path"]))
                self.articleF.write("\n")
            else:
                self.wordF.write('{0}==={1}'.format(item["body"], item["path"]))
                self.wordF.write("\n")
        return item

    def close_spider(self, spider):
        self.wordF.write('count:{0}   '.format(spider.wordCount))
        self.wordF.write('nocount;{0}   '.format(spider.noWordCount))
        self.wordF.write('allcount;{0}'.format(len(spider.word)))
        self.wordF.write("\n")

        self.wordAttrF.write('count:{0}   '.format(spider.wordAttrCount))
        self.wordAttrF.write('nocount;{0}   '.format(spider.noWordAttrCount))
        self.wordAttrF.write('allcount;{0}'.format(len(spider.wordAttr)))
        self.wordAttrF.write("\n")

        self.articleF.write('count:{0}   '.format(spider.articleCount))
        self.articleF.write('nocount;{0}   '.format(spider.noArticleCount))
        self.articleF.write('allcount;{0}'.format(len(spider.article)))
        self.articleF.write("\n")

        self.wordF.close()
        self.wordAttrF.close()
        self.articleF.close()
        self.cursor.close()
