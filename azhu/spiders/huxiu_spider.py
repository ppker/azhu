#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Topic: 爬取虎嗅网首页
Desc : 
"""
import logging
import scrapy
from azhu.items import HuxiuItem


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    #start_urls = [
    #    "http://www.huxiu.com/index.php"
    #]

    def start_requests(self):

        scrapy.Request(url="http://www.huxiu.com/index.php", callback=self.parse)



    def parse(self, response):
        print('sss' * 2)
        print(response)
        print('sss' * 2)
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
            item = HuxiuItem()
            item['title'] = sel.xpath('h2/a/text()')[0].extract()
            item['link'] = sel.xpath('h2/a/@href')[0].extract()
            # url = response.urljoin(item['link'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()

            item['published'] = sel.xpath('div[@class="mob-author"]/span/text()')[0].extract()
            # yield scrapy.Request(url, callback=self.parse_article)


    '''
    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = HuxiuItem()
        item['title'] = detail.xpath('h1/text()')[0].extract()
        item['link'] = response.url
        item['published'] = detail.xpath(
            'div[@class="article-author"]/span[@class="article-time"]/text()')[0].extract()
        logging.info(item['title'],item['link'],item['published'])
        yield item
    '''
