#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
人人网视频爬虫
"""
import logging
import scrapy
import json
from scrapy.http import FormRequest
from azhu.items import RenrenItem
import os
from urllib.parse import urlparse

class RenrenSpider(scrapy.Spider):

    name = "renren"
    allowed_domains = ["api.rr.tv"]
    ids = []

    tem_video_data = []



    usage_list = [
        'https://api.rr.tv/danmu/list', # 弹幕list
        'https://api.rr.tv/user/rewardList', # 应该是16个订阅的意思 视频分享的靠左边的按钮
        'https://api.rr.tv/v3plus/comment/hot', # 热门评论
        'https://api.rr.tv/v3plus/comment/list', # 评论列表
        'https://api.rr.tv/v3plus/video/detail', # 推荐的最热视频列表
        'https://api.rr.tv/watch/get_video_info?videoId=2769161&quality=super', # 观看视频
        'https://api.rr.tv/v3plus/index/section/content', # 页面换一换推荐热门视频
        'https://api.rr.tv/v3plus/video/getTopFeed', # 推荐页面视频列表
        'https://api.rr.tv/v3plus/video/getBottomFeed', # 推荐页面视频下拉的列表
        'https://api.rr.tv/v3plus/video/listLastUpdate', # 分类标签页面视频的列表

    ]

    common_headers = {
        'st': '7e57da0135b019689976c1932c9bfd5c',
        'deviceId': '860789039265332',
        'clientType': 'android_YingYongBao',
        'token': 'd7311ecb8388470cb75a42abb90b9851',
        'p': 'Android',
        'pkt': 'rrmj',
        'aliId': 'VoVRBcWFADsDAEE841Gma98x',
        'clientVersion': '4.2.6',
        'sm': '20191006123917abf59888fc1bcdcda88af894e2bb8d8901d6411154754838',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO A37m Build/LMY47I)',
        'Host': 'api.rr.tv',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }

    def start_requests(self):
        """先获取推荐类的视频信息，然后视频down到服务器，记录落表"""
        # recommand_url = 'https://api.rr.tv/v3plus/video/getTopFeed'
        # 极限运动
        '''
        bGtwn5LKi33PukOwWMAgh7w6yqmN366eC0mxG0bNWcc8DvEDjv6u2i3huxZi5aJD
        bGtwn5LKi33PukOwWMAgh5K3cFC97x0hCNmpjYY4jcSXcTfsez7k0u5VQabSAC2E
        bGtwn5LKi33PukOwWMAghyDi9lHG0mZko1Y7rjMxj8ZWHwQzAJQZDMKFB0dhYUVZ
        bGtwn5LKi33PukOwWMAgh5MwYidwJdJlCcOwx0cJbEk7I4v4gBGyuaksMz1nSeym
        
        oE//ON7kdX0GIlxPsaBadGLaW8Ccpg7ISzJEfxLPuY37RT3KvwdMaZdFirOxKA6K
        Ac2kPaTC4tElPoHIgCLT9Ds8UkPiq+42LGAx/t/nePi0WLC/nN73etDM5y99VlXI
        qj8K82tdJzokcYJx/rvFU/h8rQ2R8VB5puFfqaCpHtwrvHcHmvJKn6uVQ7Lvyr7R
        '''

        # 脱口秀
        '''
        bGtwn5LKi33PukOwWMAgh9QAODI0LHNy7Cki9g8icAcEBKe5/EJkpSLHeUQmyAf0
        '''

        recommand_url = 'https://api.rr.tv/v3plus/video/listLastUpdate'
        post_data = {
            # 极限运动
            'simpleBody': r"bGtwn5LKi33PukOwWMAgh7w6yqmN366eC0mxG0bNWcc8DvEDjv6u2i3huxZi5aJD"
            # 脱口秀
            # 'simpleBody': r"bGtwn5LKi33PukOwWMAgh9QAODI0LHNy7Cki9g8icAcEBKe5/EJkpSLHeUQmyAf0"
        }

        return [
            FormRequest(recommand_url, method='POST', headers=self.common_headers, formdata=post_data, callback=self.list_parse, dont_filter=True)
        ]





    def parse(self, response):
        my_data = json.loads(response.body.decode('utf-8'))
        print(my_data)


    def list_parse(self, response):
        out_data = json.loads(response.body.decode('utf-8'))
        print('=====' * 5)
        print(out_data)
        if out_data != '':
            use_data = out_data['data']['simpleVideoViewList']
            if '' != use_data:
                for val in use_data:
                    if 'VIDEO' == val['objType']:
                        if val['objId'] not in self.ids:
                            self.ids.append(val['objId'])
                            # 构造一个信息体 提供给后面使用 一直传递到item结构体那边
                            self.tem_video_data.append({
                                'video_id': val['objId'],
                                'title': val['title'],
                                'cover': val['cover'],
                                'type': "极限运动"
                            })


        return self.make_file_urls(self.tem_video_data)


    def make_file_urls(self, tem_video_data):
        print('####' * 100)
        if [] == tem_video_data:
            return


        watch_url = 'https://api.rr.tv/watch/get_video_info?videoId={0}&quality=super'
        watch_headers = {
            'st': '7e57da0135b019689976c1932c9bfd5c',
            'deviceId': '860789039265332',
            'sign': 'a6b77f33ac39e085c56c7cf9231bbb9e',
            't': '1570351455827',
            'clientType': 'android_YingYongBao',
            'token': 'd7311ecb8388470cb75a42abb90b9851',
            'p': 'Android',
            'aliId': 'VoVRBcWFADsDAEE841Gma98x',
            'pkt': 'rrmj',
            'clientVersion': '4.2.6',
            'sm': '20191006123917abf59888fc1bcdcda88af894e2bb8d8901d6411154754838',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 App/RRSPApp platform/android AppVersion/4.2.6',
            'Host': 'api.rr.tv',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
        }

        for val_data in tem_video_data:
            yield scrapy.Request(watch_url.format(val_data['video_id']), method='GET', meta=val_data, headers=watch_headers, body='', callback=self.parse_mp4, dont_filter=True)



    def parse_mp4(self, response):
        data = json.loads(response.body.decode('utf-8'))
        if '' != data['data']:
            use_data = list(data['data'].values())[0]

            videl_name = os.path.basename(urlparse(use_data['url']).path)

            item = RenrenItem()
            item['mp4_urls'] = [use_data['url']]

            item['video_id'] = response.meta['video_id']
            item['title'] = response.meta['title']
            item['cover'] = response.meta['cover']
            item['type'] = response.meta['type']
            item['name'] = videl_name
            item['path'] = 'full_new/' + videl_name
            item['size'] = 100

            print("<<<" * 10)
            print(response.meta)
            yield item

