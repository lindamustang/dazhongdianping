# -*- coding: utf-8 -*-
import scrapy
from dianpingscrapy.items import DianpingscrapyItem
from pyquery import PyQuery as pq
import re
from lxml import etree
from scrapy import Selector

class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/shanghai/ch10/g101']

    def parse(self, response):
        doc = pq(response.text)
        shops = doc('div.content>div#shop-all-list>ul>li').items()
        for li in shops:
            item = DianpingscrapyItem()
            item['name'] = li('div.txt>div.tit>a').attr('title')
            item['num'] = li('div.txt>div.tit>a').attr('data-shopid')
            item['star'] = li('div.comment>span').attr('title')
            item['sug1'] = li('div.recommend>a:nth-child(2)').text()
            item['sug2'] = li('div.recommend>a:nth-child(3)').text()
            item['sug3']= li('div.recommend>a:last-child').text()
            # tuangou = Selector(text=etree.HTML(li('div.svr-info').text()))
            # urls = tuangou.xpath('//a[@target="_blank"]/@href')
            # str_tuan = ''
            # for url in urls:
            #     str_tuan = url + ","
            # item['tuangou'] = urls

            yield item

        next = doc('div.shop-wrap>div.page>a.next').attr('href')
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

        pass
