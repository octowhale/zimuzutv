#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import requests
from core.crawlers import analysis
from core.storage import todaybucket
import json

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

    def login(self):
        r = self.s.post(self.LOGIN_URL, data=self.ZMZ_AUTH)

        if r.status_code != 200:
            print("登录失败")
        else:
            return (self.s)

    def crawl_today(self):

        today_url = "{}/today".format(self.SITE)
        # r = self.s.get(today_url)
        # if r.status_code != 200:
        #     self.login()

        # print(today_url)
        self.login()
        r = self.s.get(today_url)

        r.raise_for_status()
        r.encoding = r.apparent_encoding

        html = r.text

        items = analysis.today(html)

        todaybucket.upsert(items)

        print("等待 {} 秒继续执行下一次任务".format(self.time2wait))
        time.sleep(int(self.time2wait))

    def crawl_today_loop(self):
        while True:
            self.crawl_today()

    def crawl_detail(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()

    zmz = ZimuzuCrawler()
    zmz.crawl_today()
