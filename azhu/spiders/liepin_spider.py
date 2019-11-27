#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy, re, time, sys
from azhu.items import LiepinItem
from urllib import parse
from scrapy_redis.spiders import RedisSpider

class LiepinSpider(RedisSpider):

    name = 'liepin'
    allowed_domains = ['liepin.com']

    __loss_total_day = 0
    # __loss_total_dict = {"数据分析": 0, "golang": 0, "python": 0}
    # start_urls = [
    #     "https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=数据分析",
    #     "https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=golang",
    # ]
    redis_key = "liepin:start_urls"

    custom_settings = {
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler", # redis 调度中间件
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter", # redis 去重中间件

        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue", # 指定排序爬取地址时使用的队列,按优先级排序
        # "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderQueue", # 先进先出排序
        # "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderStack", # 后进先出排序

        "SCHEDULER_PERSIST": True, # 持久化 不会清理request数据

        # 只在使用SpiderQueue或者SpiderStack是有效的参数，指定爬虫关闭的最大间隔时间
        # SCHEDULER_IDLE_BEFORE_CLOSE = 10
        "DOWNLOAD_DELAY": 1.5,

        
        "LOG_LEVEL": "WARNING",
        "LOG_ENABLED": True,
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'azhu.middlewares.RotateUserAgentMiddleware': 400,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        "ITEM_PIPELINES": {
            'azhu.pipelines.LiepinPipeline': 700,
            'scrapy_redis.pipelines.RedisPipeline': 702,
        },

        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": 6379,

    }

    def parse(self, response):

        self.logger.info("peng. into parse")
        if 200 == response.status:
            loss_date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * 3))
            # 获取url中的query params
            url_info = parse.parse_qs(parse.urlparse(response.url).query)
            if 0 < len(url_info) and 'key' in url_info:
                if 0 < len(url_info['key']):
                    search_key = url_info['key'][0]
                else:
                    search_key = ""
            else:
                search_key = ""

            # 获取数据
            li_list = response.xpath("//ul[@class='sojob-list']/li")
            if [] != li_list:
                self.logger.info("peng>>>>>>>>>. get urls length is  ---%s", len(li_list))
                for i, li in enumerate(li_list):
                    li_url = li.xpath("./div[@class='sojob-item-main clearfix']/div[@class='job-info']/h3/a/@href").get()
                    # 兼容判断 冗错后面要新增一个类似email的容器来收集这些异常数据
                    if -1 == li_url.find("http"):
                        li_url  = "https://www.liepin.com" + li_url
                        # self.logger.warning("peng>>>>>>>>>. get urls is  ---%s", li_url)
                        # continue

                    answer_day = li.xpath("./div[@class='sojob-item-main clearfix']/div[@class='job-info']/p[@class='time-info clearfix']/span/text()").get()
                    # 匹配数字
                    if None != answer_day:
                        day_num_obj = re.findall('\d+', answer_day)
                    else:
                        day_num_obj = []

                    # 获取投递日期
                    publish_date = li.xpath("./div[@class='sojob-item-main clearfix']/div[@class='job-info']/p[@class='time-info clearfix']/time/@title").get()
                    publish_date = "" if None == publish_date else publish_date
                    publish_date = re.sub(r"年|月|日", "-", publish_date)
                    publish_date = publish_date[:-1]

                    print(">>>>>>>>>>>>>>", publish_date, loss_date)
                    if publish_date <= loss_date:
                        self.__loss_total_day += 1
                        if 20 <= self.__loss_total_day:
                            self.logger.warning("结束当前爬虫 --- %s", search_key)
                            self.__loss_total_day = 0
                            return
                        else:
                            self.logger.warning("开始触发无效期 %s---%d", publish_date, self.__loss_total_day)
                    else:
                        # 猎聘的数据有点小乱，并不是严格的时间倒序
                        self.__loss_total_day = 0


                    if [] != day_num_obj:
                        answer_day = day_num_obj[0]
                    else:
                        answer_day = 0

                    self.logger.warning("peng. li_url is %s ---- %s--- %s", li_url, answer_day, i)

                    triangle_mark = li.xpath("./i/b/text()").get()
                    if None == triangle_mark:
                        triangle_mark = ""

                    if None != li_url:
                        # 继续请求
                        yield scrapy.Request(li_url, callback=self.detail_parse, meta={'answer_day': answer_day, 'search_category': search_key, 'triangle_mark': triangle_mark}, dont_filter=False)
                        # break

        # 请求下一页
        next_page = response.xpath("//div[@class='sojob-result ']/div[@class='pager']/div[1]/a[last()-1]/@href").get()

        if None != next_page and "javascript:;" != next_page:
            next_page = "https://www.liepin.com" + next_page
            print("cccccccc", next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=False)




    def detail_parse(self, response):
        if 200 == response.status:
            # loss_date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400 * 0))
            items = LiepinItem()
            items['detail_url'] = response.url

            items['answer_day'] = int(response.meta['answer_day'])
            items['search_category'] = str(response.meta['search_category'])
            items['triangle_mark'] = str(response.meta['triangle_mark'])

            items['company'] = response.xpath("//div[@class='about-position']/div[@class='title-info']/h3/a/text()").get()
            if None == items['company']:
                items['company'] = response.xpath("//div[@class='about-position']/div[1]/div[@class='title-info ']/h3/text()").get()


            if None == items['company']:
                items['company'] = "未知"
            # 去掉两端的空白字符
            items['company'] = items['company'].strip()
            # print(">>>>>>company>>>>>>>>", items['company'])
            # 兼容匹配猎头发布的职位
            is_headhunting = 0
            if -1 != response.url.find("www.liepin.com/a/"):
                eme_pay = response.xpath("//*[@id='job-hunter']/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div/p[1]/text()").get()
                is_headhunting = 1
            else:
                eme_pay = response.xpath("//div[@class='about-position']/div[@class='job-item']/div[1]/div[1]/p[@class='job-item-title']/text()").get()
            if None == eme_pay:
                items['left_pay_k'] = 0
                items['right_pay_k'] = 0
                items['num_months'] = 0
                items['left_pay_w'] = 0
                items['right_pay_w'] = 0
            else:
                list_pay = re.findall('\d+', eme_pay)
                # 3
                if 3 == len(list_pay):
                    items['left_pay_k'] = int(list_pay[0])
                    items['right_pay_k'] = int(list_pay[1])
                    items['num_months'] = int(list_pay[2])
                    items['left_pay_w'] = round(int(list_pay[0]) * int(list_pay[2]) / 10, 1)
                    items['right_pay_w'] = round(int(list_pay[1]) * int(list_pay[2]) / 10, 1)
                elif 2 == len(list_pay):
                    items['left_pay_k'] = round(int(list_pay[0]) / 1.3, 1)
                    items['right_pay_k'] = round(int(list_pay[1]) / 1.3, 1)
                    items['num_months'] = 13 # 默认13薪
                    items['left_pay_w'] = int(list_pay[0])
                    items['right_pay_w'] = int(list_pay[1])
                else: # 面议
                    items['left_pay_k'] = 0
                    items['right_pay_k'] = 0
                    items['num_months'] = 0
                    items['left_pay_w'] = 0
                    items['right_pay_w'] = 0


            items['job_address'] = response.xpath("//div[@class='about-position']/div[@class='job-item']//p[@class='basic-infor']/span/a/text()").get()
            if None == items['job_address']:
                items['job_address'] = response.xpath("//div[@class='about-position']/div[1]/div[@class='job-main ']//p[@class='basic-infor']/span/text()").get()

            if None == items['job_address']:
                items['job_address'] = "未知"

            if is_headhunting:
                items['job_title'] = response.xpath("//div[@class='about-position']/div[1]/div[1]/h1/text()").get()
            else:
                items['job_title'] = response.xpath("//div[@class='about-position']/div[@class='title-info']/h1/text()").get()

            if None == items['job_title']:
                items['job_title'] = ""

            if is_headhunting:
                publish_time = response.xpath("//*[@id='job-hunter']/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div/p[2]/time/@title").get()
                # print(">>>>>>>>", publish_time)
            else:
                publish_time = response.xpath("//div[@class='about-position']/div[@class='job-item']/div[1]/div[1]/p[@class='basic-infor']/time/@title").get()
                # print(">>>>>>>>@@@@@@", publish_time)
            # 正则替换
            if None == publish_time:
                items['publish_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            else:
                publish_time = re.sub(r"年|月|日", "-", publish_time)
                items['publish_time'] = publish_time[:-1]

            '''
            if loss_date == items['publish_time']:

                if "" != items['search_category']:
                    if items['search_category'] in self.__loss_total_dict:
                        self.__loss_total_dict[items['search_category']] += 1
                        self.logger.warning("发现无效期 %d", self.__loss_total_dict[items['search_category']])

                is_shutdown = 1
                for key1, val1 in self.__loss_total_dict.items():
                    if 5 > val1:
                        is_shutdown = 0

                if is_shutdown: # 无效次数达到峰值, 主动关闭当前爬虫进程
                    self.logger.warning("无效次数达到峰值, 主动关闭当前爬虫进程--%s---%s", self.__loss_total_dict, items['search_category'])
                    self.crawler.engine.close_spider(self, "主动关闭当前爬虫进程")
                else:
                    if items['search_category'] in self.__loss_total_dict:
                        if 5 <= self.__loss_total_dict[items['search_category']]:
                            self.logger.warning("%s 超过5次了 %s", items['search_category'], self.__loss_total_dict[items['search_category']])
                            return
                

                # 超过期限了 关闭当前爬虫进程
                # self.__loss_total_day += 1
                # self.logger.warning("发现无效期 %d", self.__loss_total_day)
                # if 5 <= self.__loss_total_day:
                    # self.logger.warning("无效次数达到峰值, 主动关闭当前爬虫进程")
                    # self.__loss_total_day = 0 # 还原
                    # raise Exception('主动关闭当前爬虫进程')
                    # sys.exit("主动关闭当前爬虫进程")
                    # self.crawler.engine.close_spider(self, "主动关闭当前爬虫进程")
            '''

            if is_headhunting:
                ask_require = response.xpath("//div[@class='about-position']/div[1]/div[2]/div[1]/div[1]/div[1]")
            else:
                ask_require = response.xpath("//div[@class='about-position']/div[@class='job-item']/div[1]/div[1]/div[@class='job-qualifications']")

            items['education'] = ask_require.xpath("./span[1]/text()").get()
            if None == items['education']:
                items['education'] = ""
            items['experience'] = ask_require.xpath("./span[2]/text()").get()
            if None == items['experience']:
                items['experience'] = ""
            items['language'] = ask_require.xpath("./span[3]/text()").get()
            if None == items['language']:
                items['language'] = ""
            elif -1 == items['language'].find('语'):
                if -1 != items['language'].find('年龄') or -1 != items['language'].find('岁'):
                    items['age'] = items['language']
                items['language'] = ""
            if "age" not in items or None == items['age'] or "" ==  items['age']:
                items['age'] = ask_require.xpath("./span[4]/text()").get()

            if None == items['age']:
                items['age'] = "未知"


            mark_treatment = response.xpath("//div[@class='job-item']//ul[@class='comp-tag-list clearfix']/li")
            job_treatment = []
            if None == mark_treatment:
                items['job_treatment'] = ""
            else:
                for li in mark_treatment:
                    if None != li.xpath("./span/text()").get():
                        job_treatment.append(li.xpath("./span/text()").get())

                items['job_treatment'] = ",".join(job_treatment)

            if is_headhunting:
                # job_description = response.xpath("//*[@id='job-hunter']/div[1]/div[1]/div[1]/div[1]/div/div[3]/div").get()
                # print('>>>>>>job_description>>>>>>>>', job_description)
                job_description = response.xpath("//div[@class='about-position']/div[1]/div[@class='job-main job-description main-message']/div[1]").get()
                # print('>>>>>>job_test>>>>>>>>', job_test)
            else:
                job_description = response.xpath("//div[@class='about-position']/div[@class='job-item main-message job-description']/div[@class='content content-word']").get()
            if None == job_description:
                items['job_description'] = ""
            else:
                items['job_description'] = re.sub(r"<.*?>", "", job_description)

            items['job_description'] = items['job_description'].strip()
            # print(">>>>>>>>>>job_description>>>>>", items['job_description'])
            # print(">>>>>>>>>>test>>>>>", job_description)


            if is_headhunting:
                other_item = response.xpath("//div[@class='about-position']/div[1]/div[5]/div[1]/ul/li")
                if 0 < len(other_item):
                    for li_oth in other_item:
                        if li_oth.xpath("./span/text()").get() != None and li_oth.xpath("./span/text()").get().find('所属部门') != -1:
                            items['oth_department'] = li_oth.xpath("./text()").get()
                            if 'oth_department' not in items or None == items['oth_department']:
                                items['oth_department'] = ""
                        elif li_oth.xpath("./span/text()").get() != None and li_oth.xpath("./span/text()").get().find('专业要求') != -1:
                            items['oth_major'] = li_oth.xpath("./text()").get()
                            if None == items['oth_major']:
                                items['oth_major'] = ""
                        elif li_oth.xpath("./span/text()").get() != None and li_oth.xpath("./span/text()").get().find('汇报对象') != -1:
                            items['oth_report'] = li_oth.xpath("./text()").get()
                            if None == items['oth_report']:
                                items['oth_report'] = ""
                        elif li_oth.xpath("./span/text()").get() != None and li_oth.xpath("./span/text()").get().find('下属人数') != -1:
                            items['oth_underline'] = li_oth.xpath("./text()").get()
                            if None == items['oth_underline']:
                                items['oth_underline'] = ""

            else:
                other_item = response.xpath("//div[@class='about-position']//div[@class='content']/ul")

                items['oth_department'] = other_item.xpath("./li[1]/label/text()").get()
                items['oth_major'] = other_item.xpath("./li[2]/label/text()").get()
                items['oth_report'] = other_item.xpath("./li[3]/label/text()").get()
                items['oth_underline'] = other_item.xpath("./li[4]/label/text()").get()

                # 做兼容处理
                # items['oth_department'] = "" if 'oth_department' not in items or None == items['oth_department'] or "" == items['oth_department'] else items['oth_department']
                # items['oth_major'] = "" if None == items['oth_major'] else items['oth_major']
                # items['oth_report'] = "" if None == items['oth_report'] else items['oth_report']
                # items['oth_underline'] = "" if None == items['oth_underline'] else items['oth_underline']


            # 做兼容的处理
            if "oth_department" not in items or None == items['oth_department']:
                items['oth_department'] = ""

            if "oth_major" not in items or None == items['oth_major']:
                items['oth_major'] = ""

            if "oth_report" not in items or None == items['oth_report']:
                items['oth_report'] = ""

            if "oth_underline" not in items or None == items['oth_underline']:
                items['oth_underline'] = ""

            if is_headhunting:
                items['enterprise_introduce'] = response.xpath("//div[@class='about-position']/div[1]/div[@data-selector='introduction']/div[1]/div[1]").get()
            else:
                items['enterprise_introduce'] = response.xpath("//div[@class='about-position']/div[@class='job-item main-message noborder']/div[1]/div[1]").get()

            # print("======>>>enterprise_introduce>>>>>", items['enterprise_introduce'])

            if None == items['enterprise_introduce']:
                items['enterprise_introduce'] = ""

            items['enterprise_introduce'] = re.sub(r"<.*?>", "", items['enterprise_introduce'])
            items['enterprise_introduce'] = items['enterprise_introduce'].strip()

            if is_headhunting:
                items['eye_industry'] = ""
                items['eye_people'] = ""
                items['eye_address'] = ""
                items['eye_register_time'] = ""
                items['eye_register_fund'] = ""
                items['eye_deadline'] = ""
                items['eye_business_scope'] = ""
            else:
                items['eye_industry'] = response.xpath("//div[@class='side']/div[@class='right-blcok-post']//ul[@class='new-compintro']/li[1]/a/text()").get()
                if None == items['eye_industry']:
                    items['eye_industry'] = ""

                eye_people = response.xpath("//div[@class='side']/div[@class='right-blcok-post']//ul[@class='new-compintro']/li[2]/text()").get()
                # 取出:后面的文字内容
                if None != eye_people:
                    if -1 != eye_people.find("公司规模"):
                        items['eye_people'] = eye_people[eye_people.find("：")+1:]
                    elif -1 != eye_people.find("公司地址"):
                        items['eye_address'] = eye_people[eye_people.find("：") + 1:]
                        items['eye_people'] = ""
                    else:
                        items['eye_people'] = ""
                        items['eye_address'] = ""
                else:
                    items['eye_people'] = ""
                    items['eye_address'] = ""

                eye_address = response.xpath("//div[@class='side']/div[@class='right-blcok-post']//ul[@class='new-compintro']/li[3]/text()").get()

                # print("zhuzhuzhuzhuzhuzhuzuh===", eye_address)
                if None != eye_address:
                    items['eye_address'] = eye_address[eye_address.find("：")+1:]
                elif "eye_address" not in items or None == items['eye_address']:
                    items['eye_address'] = ""

                eye_base_dom = response.xpath("//div[@class='side']/div[@class='right-blcok-post']//ul[@class='new-compdetail']")
                eye_register_time = eye_base_dom.xpath("./li[1]/text()").get()
                # 取出：后面的文字内容
                if None != eye_register_time:
                    items['eye_register_time'] = eye_register_time[eye_register_time.find("：") + 1:]
                else:
                    items['eye_register_time'] = ""

                eye_register_fund = eye_base_dom.xpath("./li[2]/text()").get()
                if None != eye_register_fund:
                    items['eye_register_fund'] = eye_register_fund[eye_register_fund.find("：")+1:]
                else:
                    items['eye_register_fund'] = ""

                eye_deadline = eye_base_dom.xpath("./li[3]/text()").get()
                if None != eye_deadline:
                    items['eye_deadline'] = eye_deadline[eye_deadline.find("：")+1:]
                else:
                    items['eye_deadline'] = ""

                eye_business_scope = eye_base_dom.xpath("./li[4]/text()").get()
                if None != eye_business_scope:
                    items['eye_business_scope'] = eye_business_scope[eye_business_scope.find("：")+1:]
                else:
                    items['eye_business_scope'] = ""

            # print(items)
            yield items
