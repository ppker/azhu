#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2019/12/11
# @Author   : Peng
# @Desc

"""58同城手机app租房抓包

获取筛选条件列表
https://apphouse.58.com/api/list/chuzu?tabkey=allcity&action=getFilterInfoV2&signature=cfc745658d30cfd97f69b48fb151bc11&curVer=9.4.3&schoolType=&appId=1&areaType=&localname=sh&subwayType=&os=android&format=json&geotype=baidu&v=1&ts=1576034440867&location=2,1402,1452&imei=860789039265332&filterParams={"biz":"0"}&sidDict={"PGTID":"151269591206573702924037315","GTID":"183603998206573859079134355","nameoflist":"23_index|gerenfangyuan|b","filtrate":1}&geoia=31.218097,121.356242&params={"list_extra":"geren","list_from":"index|gerenfangyuan|b","showFilterNum":true}
获取租房列表
第一页
https://apphouse.58.com/api/list/chuzu?tabkey=allcity&action=getListInfo,getFormInfo&signature=e5ee30b542cdebdb2472a7c0c75759e2&curVer=9.4.3&schoolType=&appId=1&areaType=&localname=sh&os=android&format=json&subwayType=&geotype=baidu&v=1&ts=1576034440870&imei=860789039265332&location=2,1402,1452&filterParams={"biz":"0"}&sidDict={"PGTID":"151269591206573702924037315","GTID":"183603998206573859079134355","nameoflist":"23_index|gerenfangyuan|b","filtrate":1}&geoia=31.218097,121.356242&params={"list_extra":"geren","list_from":"index|gerenfangyuan|b","showFilterNum":true}
第二页
https://apphouse.58.com/api/list/chuzu?action=getListInfo&appId=1&areaType=&localname=sh&format=json&geotype=baidu&v=1&ts=1576047753546&imei=860789039265332&page=2&params={"list_extra":"geren","list_from":"index|gerenfangyuan|b","showFilterNum":true}&tabkey=allcity&signature=c0396743a810df2ee25fbc8030219bf3&curVer=9.4.3&schoolType=&os=android&subwayType=&location=2,1402,1452&filterParams={"biz":"0"}&sidDict={"PGTID":"185454176206575684968081971","GTID":"120758245206575731007818834","nameoflist":"23_index|gerenfangyuan|b","filtrate":1}&geoia=31.218131,121.35616
第三页
https://apphouse.58.com/api/list/chuzu?action=getListInfo&appId=1&areaType=&localname=sh&format=json&geotype=baidu&v=1&ts=1576048882943&imei=860789039265332&page=3&params={"list_extra":"geren","list_from":"index|gerenfangyuan|b","showFilterNum":true}&tabkey=allcity&signature=2ac843d573c455a4b8e814b4e53d8086&curVer=9.4.3&schoolType=&os=android&subwayType=&location=2,1402,1452&filterParams={"biz":"0"}&sidDict={"PGTID":"120758245206575731007818834","GTID":"121948415206575731214304861","nameoflist":"23_index|gerenfangyuan|b","filtrate":1,"allNum":25}&geoia=31.218131,121.35616
"""

import scrapy, re, time, sys, json
from urllib import parse
import scrapy
from scrapy.http import FormRequest
from azhu.items import ZufangItem

class ZuFangSpider(scrapy.Spider):

    name = 'zufang'
    allowed_domains = ["apphouse.58.com"]
    use_page = 1

    city_dict = {
        "sh": "上海",
    }

    custom_settings = {
        "DOWNLOAD_DELAY": 3.5,
        # "LOG_LEVEL": "WARNING",
        "LOG_ENABLED": True,
        "COOKIES_ENABLES": False,
        "USER_AGENT": "okhttp/3.11.0",

        "DOWNLOADER_MIDDLEWARES": {
        # 'azhu.middlewares.AzhuDownloaderMiddleware': 543,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 'azhu.middlewares.RotateUserAgentMiddleware': 400,
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
    }

    get_url_data = {
        "action": "getListInfo",
        "appId": '1',
        "areaType": "",
        "localname": "sh",
        "format": "json",
        "geotype": "baidu",
        "v": '1',
        "ts": '1576059430986',
        "imei": "860789039265332",
        "page": str(use_page),
        "params": '{"list_extra":"geren","list_from":"index|gerenfangyuan|b","showFilterNum":true}',
        "tabkey": "allcity",
        "signature": "49f193ca2142fef58dfc37c9aa88496c",
        "curVer": "9.4.3",
        "schoolType": "",
        "os": "android",
        "subwayType": "",
        "location": "2,1402,1452",
        "filterParams": '{"biz": "0"}',
        "sidDict": '{"PGTID":"120758245206575731007818834","GTID":"150759646206577261662872963","nameoflist":"23_index|gerenfangyuan|b","filtrate":1}',
        "geoia": "31.21808,121.356173"
    }

    common_headers = {

        # ':path': "/api/list/chuzu?{}".format(parse.urlencode(get_url_data).encode('utf-8')),
        ':method': 'GET',
        ':path': '/api/list/chuzu?action=getListInfo&appId=1&areaType=&localname=sh&format=json&geotype=baidu&v=1&ts=1576059430986&imei=860789039265332&page=2&params=%7B%22list_extra%22%3A%22geren%22%2C%22list_from%22%3A%22index%7Cgerenfangyuan%7Cb%22%2C%22showFilterNum%22%3Atrue%7D&tabkey=allcity&signature=49f193ca2142fef58dfc37c9aa88496c&curVer=9.4.3&schoolType=&os=android&subwayType=&location=2%2C1402%2C1452&filterParams=%7B%22biz%22%3A%220%22%7D&sidDict=%7B%22PGTID%22%3A%22120758245206575731007818834%22%2C%22GTID%22%3A%22150759646206577261662872963%22%2C%22nameoflist%22%3A%2223_index%7Cgerenfangyuan%7Cb%22%2C%22filtrate%22%3A1%7D&geoia=31.21808%2C121.356173',
        ':authority': 'apphouse.58.com',
        ':scheme': 'https',
        'xxzl_smartid': '',
        'uuid': '4efcfcab-2afd-4615-9e71-da5730e00740',
        'maptype': '2',
        'dirname': 'sh',
        'version': '9.4.3',
        'osarch': 'arm64-v8a',
        'nettype': 'wifi',
        '58ua': '58app',
        'ppu': '',
        'apkbus': '',
        'ajkauthticket': '',
        'm': '',
        'owner': 'baidu',
        'rnsoerror': '0',
        'nop': '',
        'currentcid': '2',
        'platform': 'android',
        '58mac': '',
        'location': '2,1402,1452',
        'jumpextra': '{"spm":"","utm_source":""}',
        'channelid': '2266',
        'r': '1280_720',
        'product': '58app',
        'official': 'true',
        'lon': '121.356173',
        'osv': '5.1',
        'marketchannelid': '2266',
        'xxzl_deviceid': 'Nh2ObnY8IaR656F+vvAYDjj9kMY8hUjUY1pUL6IydOv1W7r5zCVHo2GCaFI4RpJH',
        'xxzl_cid': '84b1e644f8b94b118851f4ab9216dd19',
        'id58': '100867291075587',
        'rimei': '860789039265332',
        'totalsize': '11.9',
        'accept-encoding': 'gzip,deflate',
        'bundle': 'com.wuba',
        'oldimei': '860789039265332',
        'imei': '860789039265332',
        'productorid': '1',
        'bangbangid': '1080866310644636103',
        'uniqueid': 'e659f0c4839d134773f8b05984952feb',
        'apn': 'WIFI',
        'xxzlsid': '5Qx2Oz-UEo-Ld4-QTQ-2Fkza9f6E',
        'androidid': '2c7ea6120747c506',
        'cid': '2',
        'deviceid': '2c7ea6120747c506',
        'ltext': '%E5%8C%97%E6%96%B0%E6%B3%BE',
        'os': 'android',
        'locationstate': '1',
        'brand': 'OPPO',
        'ua': 'OPPO A37m',
        'uid': '',
        'lat': '31.21808',
        'jumpinfo': '',
        'user-agent': 'okhttp/3.11.0',
    }

    common_list_url = "https://apphouse.58.com/api/list/chuzu"



    def start_requests(self):
        current_time = round(time.time() * 1000)

        return [
            FormRequest(self.common_list_url, method='GET', headers=self.common_headers, formdata=self.get_url_data, callback=self.list_parse, meta={"page": self.use_page}, dont_filter=False)
        ]


    def list_parse(self, response):
        if 200 == response.status:
            out_data = json.loads(response.body.decode('utf-8'))
            item = ZufangItem()
            if 0 == out_data['status'] and 0 < len(out_data['result']['getListInfo']['infolist']):
                for detail in out_data['result']['getListInfo']['infolist']:
                    # print("$$$$$$$$$$$$$$$$$$$$$", detail)
                    if "title" in detail and "" != detail['title']:
                        item["title"] = detail['title']
                        item["house_type"] = detail['huxing']
                        # print("@@@@@@@@@@@@@@@@@@@@", detail['detailaction'])

                        # apartment公寓 单独判断处理
                        if isinstance(detail['detailaction'], dict):
                            item["charge_url"] = detail['detailaction']['content']['charge_url']
                            house_base_info = detail['detailaction']['content']['preLoadInfo']['result']['info'][4]['zf_titleinfo_area']['base_info']
                            item["house_type_full"] = house_base_info[0]['title']
                            item["house_area"] = house_base_info[1]['title']
                            item["house_tier"] = house_base_info[2]['title']
                            item["house_orientation"] = house_base_info[3]['title']
                            zf_baseinfo_area = detail['detailaction']['content']['preLoadInfo']['result']['info'][6][
                                'zf_baseinfo_area']
                            item["house_labels"] = ""
                            item["can_one"] = 0 # 押一付一
                            item["has_balcony"] = 0 # 是否有阳台
                            if 0 < len(zf_baseinfo_area['tags']):
                                tags = []
                                for tag in zf_baseinfo_area['tags']:
                                    if "押一付一" == tag['title']: # 押一付一
                                        item["can_one"] = 1

                                    if re.search("阳台", tag['title']):
                                        item["has_balcony"] = 1

                                    tags.append(tag['title'])

                                item["house_labels"] = ",".join(tags)

                        else: # 目前是公寓
                            if isinstance(detail['detailaction'], str):
                                detail_params = parse.parse_qs(parse.urlparse(detail['detailaction']).query)
                                if 'params' in detail_params:
                                    detail_params_json = json.loads(detail_params['params'][0])
                                    # 进行处理











                        item["estate_title"] = detail['dictName']

                        city_py = detail['detailaction']['content']['local_name']
                        city_name = self.city_dict[city_py]

                        item["address"] = city_name + detail['distanceDict']['local_address'] + detail['dictName']
                        item["rent"] = detail['priceDict']['p']
                        item["request_url"] = response.url

                        self.logger.warning("this is item is %s", item)
                        self.logger.warning(">>>>>>>>>>>>")

                        # print("@@@@@@@@@", item)
                        # return
                        yield item

            # 获取下一页数据
            if response.meta["page"] <= 200: # 目前是200页
                now_page = response.meta["page"] + 1
                self.get_url_data.page = str(now_page)

                self.logger.warning(">>>>>>>>>>>>>开始第%s页", now_page)
                return FormRequest(self.common_list_url, method='GET', headers=self.common_headers, formdata=self.get_url_data, callback=self.list_parse, meta={"page": now_page}, dont_filter=False)






        else:
            self.logger.warning("peng. no parse context")












