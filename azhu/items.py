# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy, time


class AzhuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HuxiuItem(scrapy.Item):
    """虎嗅网新闻Item"""
    title = scrapy.Field()      # 标题
    link = scrapy.Field()       # 链接
    desc = scrapy.Field()       # 简述
    published = scrapy.Field()  # 发布时间


class LiepinItem(scrapy.Item):
    """猎聘网数据Item"""
    job_title = scrapy.Field() # 职位名称
    left_pay_k = scrapy.Field() # 薪资 月薪 左侧值 k
    right_pay_k = scrapy.Field() # 薪资 月薪 右侧值 k
    num_months = scrapy.Field() # 一年多少薪 default 13
    left_pay_w  = scrapy.Field() # 换算成年薪 左侧值 w
    right_pay_w = scrapy.Field() # 换算成年薪 右侧值 w

    answer_day = scrapy.Field() # 投递后反馈的工作日
    company = scrapy.Field() # 公司名称
    job_address = scrapy.Field() # 工作城市
    publish_time = scrapy.Field() # 发布时间
    education = scrapy.Field() # 学历要求
    experience = scrapy.Field() # 工作经验要求
    language = scrapy.Field() # 语言要求
    age = scrapy.Field() # 年龄要求
    job_treatment = scrapy.Field() # 工作待遇标签[通讯津贴, 午餐补助, 定期体检, 管理规范]
    job_description = scrapy.Field() # 职位描述

    # oth -> other 其他信息
    oth_department = scrapy.Field() # 所属部门
    oth_report = scrapy.Field() # 汇报对象
    oth_major = scrapy.Field() # 专业要求
    oth_underline = scrapy.Field() # 下属人数
    enterprise_introduce = scrapy.Field() # 企业介绍

    # sky_eye 天眼查数据
    eye_industry = scrapy.Field() # 行业
    eye_people = scrapy.Field() # 公司规模
    eye_address = scrapy.Field() # 公司地址
    eye_register_time = scrapy.Field() # 注册时间
    eye_register_fund =  scrapy.Field() # 注册资金
    eye_deadline = scrapy.Field() # 经营期限
    eye_business_scope = scrapy.Field() # 经营范围

    detail_url = scrapy.Field() # 请求详情页面url
    search_category = scrapy.Field() # 搜索标签分类 | 数据分析
    triangle_mark = scrapy.Field() # 三角标记


    def get_insert_sql(self):

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        insert_sql = """
            insert into `liepin`(job_title, left_pay_k, right_pay_k, num_months, left_pay_w, right_pay_w, answer_day, company, job_address, publish_time, education, experience, language, 
            age, job_treatment, job_description, oth_department, oth_report, oth_major, oth_underline, enterprise_introduce, eye_industry, eye_people, 
            eye_address, eye_register_time, eye_register_fund, eye_deadline, eye_business_scope, detail_url, search_category, triangle_mark, created_at, updated_at) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            self['job_title'], float(self['left_pay_k']), float(self['right_pay_k']), int(self['num_months']), float(self['left_pay_w']), float(self['right_pay_w']), float(self['answer_day']), self['company'], self['job_address'], self['publish_time'], self['education'], self['experience'], self['language'],
            self['age'], self['job_treatment'], self['job_description'], self['oth_department'], self['oth_report'], self['oth_major'], self['oth_underline'], self['enterprise_introduce'], self['eye_industry'], self['eye_people'],
            self['eye_address'], self['eye_register_time'], self['eye_register_fund'], self['eye_deadline'], self['eye_business_scope'], self['detail_url'], self['search_category'], self['triangle_mark'], now_time, now_time
        )

        return insert_sql, params


class RenrenItem(scrapy.Item):

    mp4_urls = scrapy.Field()
    mp4s = scrapy.Field()
    video_id = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    path = scrapy.Field()
    size = scrapy.Field()


    def get_insert_sql(self):

        insert_sql = """
            insert into renren_video(video_id, title, cover, origin_url, video_name, video_path, size, type) 
            VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%d', '%s');
        """
        params = (
            self['video_id'], self['title'], self['cover'], self['mp4_urls'][0], self['name'], self['path'], self['size'], self['type']
        )

        return insert_sql, params


