# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline
import pymysql
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem


class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return 'full_new/' + os.path.basename(urlparse(request.url).path)
        # return 'full/%s%s' % (media_guid, media_ext)

    '''
    def item_completed(self, results, item, info):

        if isinstance(item, dict) or self.files_result_field in item.fields:
            item[self.files_result_field] = [x for ok, x in results if ok]

            if "" != results[0][1]['path']:
                item['name'] = results[0][1]['path'].split("/")[-1]
                item['path'] = results[0][1]['path']
            else:
                item['name'] = ""
                item['path'] = ""

            # item['size'] = 100
        return item
    '''


class RenrenPipeline(object):

    # 140.143.32.44
    def __init__(self):
        print('sss'*30)
        dbparms = dict(
            host = 'localhost',
            db = 'spider_video',
            user = 'root',
            passwd = '123456',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        self.select_db = pymysql.connect("localhost", "root", "123456", "spider_video")
        self.cursor = self.select_db.cursor()

    def process_item(self, item, spider):

        self.cursor.execute("select id from renren_video where video_id = %d" % item['video_id'])
        select_data = self.cursor.fetchone()
        print("~~~~~~" * 10)
        print(select_data)
        if select_data:
            raise DropItem("video had in" % item)
        else:
            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider)
            return item



    def handle_error(self, failure, item, spider):
        print('this has errors')
        insert_sql, params = item.get_insert_sql()
        print(insert_sql % params)
        print(failure)

    def do_insert(self, cursor, item):

        insert_sql, params = item.get_insert_sql()
        print("target going up up" + "@@"*10)
        # print(insert_sql % params)
        cursor.execute(insert_sql % params)


    def close_spider(self, spider):
        self.select_db.close()




class LiepinPipeline(object):

    def __init__(self, db_mysql):

        dbparms = {"cursorclass": pymysql.cursors.DictCursor, "use_unicode": True}
        dbparms.update(db_mysql)
        # print(">>>>>>" * 10, dbparms)

        '''
        dbparms = dict(
            host = 'localhost',
            db = 'zen_spider',
            user = 'root',
            passwd='123456',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        '''

        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_mysql = crawler.settings.get('DB_MYSQL'))


    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        print('this has errors')
        insert_sql, params = item.get_insert_sql()
        print(insert_sql % params)
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        print("begin to insert data >>>>", item['detail_url'])
        # print(insert_sql % params)
        cursor.execute(insert_sql, params)

    def close_spider(self, spider):
        pass
