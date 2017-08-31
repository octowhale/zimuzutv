#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import requests
from core.crawlers import analysis
from core.storage import todaybucket, detailbucket, redisbucket
import json
import redis

import time
import threading


class ZimuzuCrawler(object, ):
    def __init__(self, time2wait):
        self.SITE = 'http://www.zimuzu.tv'
        self.LOGIN_URL = "{}/User/Login/ajaxLogin".format(self.SITE)
        self.ZMZ_AUTH = json.load(open('setting/zimuzu_auth.json', 'r', encoding='utf-8'))
        self.ENCODING = 'utf-8'
        self.s = requests.Session()
        self.time2wait = time2wait
        self.redis_client = redisbucket.RedisBucket()
        self.login()

    def login(self):
        """登录"""

        """todo: 是否登录判断，解决每次抓取都需要登录的尴尬"""
        r = self.s.post(self.LOGIN_URL, data=self.ZMZ_AUTH)

        if r.status_code != 200:
            print("登录失败")
        else:
            print("登录成功")
            return (self.s)

    def crawl_html(self, url):
        self.login()

        r = self.s.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        return r.text

    def crawl_today(self):

        today_url = "{}/today".format(self.SITE)
        # r = self.s.get(today_url)
        # if r.status_code != 200:
        #     self.login()

        # print(today_url)
        html = self.crawl_html(today_url)

        items = analysis.today(html)

        todaybucket.upsert(items)

        print("等待 {} 秒继续执行下一次任务".format(self.time2wait))
        time.sleep(int(self.time2wait))

    def crawl_today_loop(self):
        while True:
            self.crawl_today()

    def crawl_detail(self, page):
        """抓取影片所有相关连接"""

        """todo: 引入 redis，解决每次点击都爬取页面的问题"""

        now_time = time.time()

        # detail_update_sign = redisbucket.get_update_detail_info(page, now_time)
        detail_update_sign = self.redis_client.get_update_detail_info(page, now_time)
        if not detail_update_sign:
            """如果返回为 False， 则跳过更新"""
            return None

        """开始更新页面"""
        """http://www.zimuzu.tv/resource/list/35575"""
        detail_url = "{}/resource/list/{}".format(self.SITE, page)

        """判断是否需要抓取页面"""

        """抓取页面"""
        html = self.crawl_html(detail_url)

        items = {'m_id': page, 'm_update_time': time.time()}
        items = analysis.detail(html, items)

        result = detailbucket.upsert(items)  # return True if success
        if result:
            """向 redis 里面插入信息"""
            self.redis_client.set_detail_update_info(page, now_time)


if __name__ == '__main__':
    zmz = ZimuzuCrawler()
    zmz.crawl_today()
