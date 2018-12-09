from scrapy.spiders import Spider
from scrapy import Request

from zxsdisno.items import ZxsdisnoItem


class IsnobaiduSpider(Spider):
    name = 'demo'
    # allowed_dimains = ['www.baidu.com']
    start_urls = [
        'https://www.baidu.com/s?wd=http%3A%2F%2Fwww.2ge.cn%2Fhome%2Fwdr%2FEF0AAB841ABCD83673FBE58F6E7BCA26',
        'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=ed6d4a0a00040d41&ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=http://www.2ge.cn/home/wdr/EF0AAB841ABCD83673FBE58F6E7BCA26&oq=http%3A%2F%2Fwww.2ge.cn%2Fhome%2Fwdr%2F%26gt%3BF0AAB841AB%26lt%3BD8%26lt%3B67%26lt%3BFB%26gt%3B58F6%26gt%3B7B%26lt%3BA26&rsv_pq=ed6d4a0a00040d41&rsv_t=6d0dsIj/iOeSME5QnLuJzgFfIzPQ9ayVoI6rhJ4s+MLfawsYdR6fvPCZmKc&rqlang=cn&rsv_enter=0&rsv_sug=1&bs=http://www.2ge.cn/home/wdr/EF0AAB841ABCD83673FBE58F6E7BCA26&rsv_sid=undefined&_ss=1&clist=835926ba8e6eb449&hsug=&f4s=1&csor=27&_cr1=43913'
        # "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8"
    ]

    def __init__(self):
        self.myurls = None
        self.count = 0

    # def start_requests(self):
    #     print(self.myurls)
    #     urlPreFix = 'https://www.baidu.com/s?wd=http://www.2ge.cn/home/wdr/{0}'
    #     urls = [
    #         'EF0AAB841ABCD83673FBE58F6E7BCA26',
    #         'EFA4B197A964C5DFFBCA6F48F7160C3C'
    #     ]
    #     for url in urls:
    #         yield Request(urlPreFix.format(url), callback=self.parse)

    def parse(self, response):
        print(response)
        # result = response.xpath('//div[@class="c-abstract"]/text()').extract()
        item = ZxsdisnoItem()
        # item["title"] = response.xpath('//div[@class="p-name p-name-type-2"]/a/em/text()').extract()
        item['result'] = 99
        self.count = self.count + 1
        yield item
