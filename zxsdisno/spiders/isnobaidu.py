from scrapy.spiders import Spider
from scrapy import Request
import random
import time
import operator

from zxsdisno.items import ZxsdisnoItem


class IsnobaiduSpider(Spider):
    name = 'demo'

    # start_urls = [
    #     'https://www.baidu.com/s?wd=http%3A%2F%2Fwww.2ge.cn%2Fhome%2Fwdr%2FEF0AAB841ABCD83673FB00E58F6E7BCA26'
    #     # "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8"
    # ]

    def __init__(self, *args, **kwargs):
        self.article = []
        self.word = []
        self.wordAttr = []
        self.articleCount = 0
        self.noArticleCount = 0
        self.wordAttrCount = 0
        self.wordCount = 0
        self.noWordCount = 0
        self.noWordAttrCount = 0
        self.cookies = {
            'BD_UPN	': '13314752',
            'BAIDUID': '8A280E2849B24A71325777A587EC0D2A:FG=1',
            'BIDUPSID': '8A280E2849B24A71325777A587EC0D2A',
            'PSTM': '1540197775',
            'BDUSS': 'HNiSEVTQlV3U3V5SVJ6Rnd5Z2hZZFZnZUxPbGVwN1ViMn5RTVNJWHl6RnJ6VFZjQUFBQUFBJCQAAAAAAAAAAAEAAACRUkyFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGtADlxrQA5cR',
            'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
            'BD_CK_SAM': '1',
            'H_PS_645EC': 'a680OoHHIbTSnh/luMiDlQaiV8ocIgy+LqpZIwaojh+a6IHHjaHmIiIs2KM',
            'H_PS_PSSID': '1436_21098_28019_27244_22074',
            'PSINO': '2',
            'sugstore': '0',
        }
        self.headers = {
            # 'Accept': '*/*',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            # 'Host': 'www.baidu.com',
            # 'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        }
        self.userUgents = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        ]
        self.cookieField = [
            '9407gzabf9wRb52PqlsIANtxpxSyMUlbbLX/ocxOBsABvUArR+OPd+iffbI',
            '8b2cRDZ8G8ZlViUd/q6wdnarU5LM37zMrLHdTRVyR46vmSQk8pP8XQsOaFA',
            'a680OoHHIbTSnh/luMiDlQaiV8ocIgy+LqpZIwaojh+a6IHHjaHmIiIs2KM',
            '4393NWiQvQrx+ZDZwZO85r/nU+nmbmdCzpIaQU+uopG06LUDz5PAmBgCUJU'
        ]

    def start_requests(self):
        urlPreFix = 'https://www.baidu.com/s?wd=http://www.2ge.cn/home/{0}/{1}'
        all = self.word + self.wordAttr + self.article
        for wordTuple in all:
            time.sleep(random.uniform(0, 1))
            agent = random.choice(self.userUgents)
            self.headers['User-Agent'] = agent
            yield Request(urlPreFix.format(wordTuple[1], wordTuple[0]), callback=self.parse, headers=self.headers,
                          cookies=self.cookies)

    def parse(self, response):
        prefix = 'https://www.baidu.com/s?wd='
        keyWord = 'www.2ge.cn'
        body = response.xpath('//div[@class="f13"]/a/b/text()').extract()
        item = ZxsdisnoItem()
        url = response.url[len(prefix):]
        if len(body) > 0 and keyWord in body[0]:
            item['body'] = '有内容'
            item['path'] = url
            if 'wdr' in url:
                self.wordAttrCount = self.wordAttrCount + 1
            elif 'ard' in url:
                self.articleCount = self.articleCount + 1
            else:
                self.wordCount = self.wordCount + 1
        else:
            item['body'] = '无内容aaa'
            item['path'] = url
            if 'wdr' in url:
                self.noWordAttrCount = self.noWordAttrCount + 1
            elif 'ard' in url:
                self.noArticleCount = self.noArticleCount + 1
            else:
                self.noWordCount = self.noWordCount + 1
        yield item
