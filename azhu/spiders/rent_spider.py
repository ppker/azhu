#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2019/11/27
# @Author   : Peng
# @Desc

import scrapy, re, time, sys
from azhu.items import ZufangItem
from urllib import parse
from scrapy_redis.spiders import RedisSpider

class RentSpider(RedisSpider):

    name = 'rent'
    allowed_domains = ['sh.58.com']
    redis_key = 'rent:start_urls'

    # start_urls
    sh_url = 'https://sh.58.com/chuzu/0/?PGTID=0d3090a7-0000-2ce9-0209-f26150e362a5&ClickID=2'

    custom_settings = {
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",  # redis 调度中间件
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",  # redis 去重中间件

        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue",  # 指定排序爬取地址时使用的队列,按优先级排序
        # "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderQueue", # 先进先出排序
        # "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderStack", # 后进先出排序

        "SCHEDULER_PERSIST": True,  # 持久化 不会清理request数据
        "CLOSESPIDER_PAGECOUNT": 3, # spider关闭次数 根据item的次数

        # 只在使用SpiderQueue或者SpiderStack是有效的参数，指定爬虫关闭的最大间隔时间
        # SCHEDULER_IDLE_BEFORE_CLOSE = 10
        "DOWNLOAD_DELAY": 5.5,

        "COOKIES_ENABLED": True,

        "LOG_LEVEL": "WARNING",
        "LOG_ENABLED": True,
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'azhu.middlewares.RotateUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        "ITEM_PIPELINES": {
            # 'azhu.pipelines.LiepinPipeline': 700,
            'scrapy_redis.pipelines.RedisPipeline': 702,
        },

        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": 6379,
    }

    common_header = {
        'authority': 'sh.58.com',
        'path': '/chuzu/0/?PGTID=0d3090a7-0000-2ce9-0209-f26150e362a5&ClickID=2',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://sh.58.com/chuzu/?PGTID=0d100000-0000-2973-559e-35ffd04dcd26&ClickID=2',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': 1,
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

    }

    common_cookies = {
        'f': 'n',
        'commontopbar_new_city_info': '2%7C%E4%B8%8A%E6%B5%B7%7Csh',
        'f': 'n',
        'userid360_xml': 'BA4FB3B90DA19A571AD66D70EE598E68',
        'time_create': '1577447810650',
        'commontopbar_new_city_info': '2%7C%E4%B8%8A%E6%B5%B7%7Csh',
        'id58': 'e87rZl3buuIop9Z3A0WSAg==',
        '58tj_uuid': '92624bc2-cac0-41e0-b3fe-33e956ef3789',
        'als': '0',
        'wmda_uuid': '5dc9266132469609ce29d71b40a0e6aa',
        'wmda_new_uuid': '1',
        'xxzl_deviceid': 'vVa628zEKWzwpwxwkZmhs6scXA%2BkWXDcaH%2BeFVFc7BSv6NBFis%2B2ijmr%2FPqyNtLF',
        'f': 'n',
        'city': 'sh',
        '58home': 'sh',
        'defraudName': 'defraud',
        'Hm_lvt_ae019ebe194212c4486d09f377276a77': '1574858350',
        'Hm_lpvt_ae019ebe194212c4486d09f377276a77': '1574858350',
        'Hm_lvt_dcee4f66df28844222ef0479976aabf1': '1574905916',
        'Hm_lpvt_dcee4f66df28844222ef0479976aabf1': '1574908086',
        'wmda_visited_projects': '%3B10104579731767%3B11187958619315%3B2385390625025',
        'commontopbar_new_city_info': '2%7C%E4%B8%8A%E6%B5%B7%7Csh',
        'commontopbar_ipcity': 'sh%7C%E4%B8%8A%E6%B5%B7%7C0',
        'new_uv': '10',
        'utm_source': '',
        'spm': '',
        'init_refer': '',
        'wmda_session_id_11187958619315': '1575014916877-3989783a-ded4-311a',
        'new_session': '0',
        'ppStore_fingerprint': 'D9899EFDCC49FB4F1E8A17B4AD1D9626872EEBDDD1ADF757%EF%BC%BF1575015719471',
        'xzfzqtoken': 'AzZM7skPJhWzoH8ny1O4bWThOhNjf%2F0Xaye8Bv9720hZY3OAmFifk2TvJF%2BW4cHWin35brBb%2F%2FeSODvMgkQULA%3D%3D',
        'xxzl_cid': '6d4cfb2ca2564501a680fc2c4f9e7911',
        'xzuid': '512caf7d-48e3-4499-869f-66d4282734aa',
    }

    def make_requests_from_url(self, url):
        """
        对request做一些设置
        :param url:
        :return:
        """
        request = super(RentSpider, self).make_requests_from_url(url)
        request.headers = self.common_header
        request.cookies = self.common_cookies
        return request


    def parse(self, response):
        self.logger.warning("peng. start parse url %s", response.url)
        if 200 == response.status:

            li_list = response.xpath("//div[@class='list-wrap']/div[2]/ul[@class='house-list']/li[@class='house-cell']")

            if 0 == len(li_list):
                self.logger.warning("peng. no has get li_url")
                print(">>>>>>>>", response.text)
            else:
                for li in li_list:
                    li_url = li.xpath("./div[@class='des']/h2/a/@href").get("")
                    if "" != li_url:
                        yield scrapy.Request(li_url, callback=self.parse_detail, dont_filter=False, headers=self.common_header)
                    else:
                        self.logger.warning("peng. li_url is null>>>>>")

            # 请求下一页
            next_url = response.xpath("//li[@id='pager_wrap']/div/a[@class='next']/@href").get("")
            if "" != next_url:
                self.logger.warning("peng. request the next page url is %s", next_url)

                # yield scrapy.Request(next_url, callback=self.parse, dont_filter=False, headers=self.common_header)
            else:
                self.logger.warning("peng. no has next page")



        else:
            self.logger.warning("peng. had find some error")


    def parse_detail(self, response):
        self.logger.warning("peng parse detail page >>>>> ")
        if 200 == response.status:
            items = RentItem()
            items['detail_url'] = response.url
            items['title'] = response.xpath("//div[@class='house-title']/h1/text()").get("").strip()
            items['publish_time'] = response.css("div.house-title p.house-update-info::text").get("").strip()
            items['rental_money'] = response.css("div.house-basic-info div.house-pay-way span:nth-child(1) b::text").get("")
            items['pay_period'] = response.css("div.house-basic-info div.house-pay-way span:nth-child(2)::text").get("")
            house_basic = response.css("div.house-basic-desc div.house-desc-item ul")
            items['rent_type'] = house_basic.xpath("./li[1]/span[2]/text()").get()
            house_type = house_basic.xpath("./li[2]/span[2]/text()").get("")
            house_type_list = house_type.split(" ")
            print(house_type_list)
            return


            items['orientation'] = house_basic.xpath("./li[3]/span[2]/text()").get()
            items['floor'] = 0
            items['house_estate'] = house_basic.xpath("./li[4]/span[2]/a/text()").get()
            items['address'] = house_basic.xpath("./li[5]/span[2]/a[1]/text()").get("").strip() + house_basic.xpath("./li[6]/span[2]/text()").get("").strip()
            items['publish_user'] = response.css("div.house-basic-desc div.house-agent-info p.agent-name a::text").get("").strip()
            items['platform'] = '58同城'

            print(items)
            return






