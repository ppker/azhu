#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
人人网视频爬虫
"""

import logging
import scrapy
import json
from scrapy.http import FormRequest


class RenrenSpider(scrapy.Spider):
    name = "renren bak"
    allowed_domains = ["api.rr.tv"]

    usage_list = [
        'https://api.rr.tv/danmu/list',  # 弹幕list
        'https://api.rr.tv/user/rewardList',  # 应该是16个订阅的意思 视频分享的靠左边的按钮
        'https://api.rr.tv/v3plus/comment/hot',  # 热门评论
        'https://api.rr.tv/v3plus/comment/list',  # 评论列表
        'https://api.rr.tv/v3plus/video/detail',  # 推荐的最热视频列表
        'https://api.rr.tv/watch/get_video_info?videoId=2769161&quality=super',  # 观看视频
        'https://api.rr.tv/v3plus/index/section/content',  # 页面换一换推荐热门视频
        'https://api.rr.tv/v3plus/video/getTopFeed',  # 推荐页面视频列表
        'https://api.rr.tv/v3plus/video/getBottomFeed',  # 推荐页面视频下拉的列表
        'https://api.rr.tv/v3plus/video/listLastUpdate',  # 搞笑分类页面视频的列表

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
        'Content-Length': '250',
    }

    def start_requests(self):
        url = "https://api.rr.tv/v3plus/index/channel"
        my_headers = {
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
            'Host': 'api.rr.tv'
        }

        my_data = {
            'simpleBody': 'Sg9dBTl8HAy0PfEPYRa7zkw4rSdBOjeLa26KOvyCgTGDBhRLWm5BAJrd/PQlabWo'
        }

        url2 = 'https://api.rr.tv/v3plus/index/todayChoice'
        '''
        headers_2 = {}
        headers_2.update(my_headers)
        headers_2.update({
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Length': '0',
        })

        print('ssssssssss' * 3)
        print(headers_2)
        '''

        headers_2 = {
            'st': '7e57da0135b019689976c1932c9bfd5c',
            'deviceId': '860789039265332',
            'clientType': 'android_YingYongBao',
            'token': 'd7311ecb8388470cb75a42abb90b9851',
            'p': 'Android',
            'pkt': 'rrmj',
            'aliId': 'VoVRBcWFADsDAEE841Gma98x',
            'clientVersion': '4.2.6',
            'sm': '20191006123917abf59888fc1bcdcda88af894e2bb8d8901d6411154754838',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO A37m Build/LMY47I)',
            'Host': 'api.rr.tv',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        url_3 = 'https://api.rr.tv/watch/get_video_info?videoId=2191908&quality=super'
        headers_3 = {
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

        print('ssssssssss' * 3)
        '''
        return [
            FormRequest(url, method='POST', headers=my_headers, formdata=my_data, callback=self.parse, dont_filter=True)
        ]
        '''

        '''
        return [
            FormRequest(url2, method='POST', headers=headers_2, formdata={}, callback=self.parse, dont_filter=True)
        ]
        '''
        '''
        return [
            scrapy.Request(url_3, method='GET', headers=headers_3, body='', callback=self.parse, dont_filter=True)
        ]
        '''

        return [
            FormRequest(url2, method='POST', headers=headers_2, formdata={}, callback=self.parse, dont_filter=True)
        ]

    def parse(self, response):
        my_data = json.loads(response.body.decode('utf-8'))
        print(my_data)




