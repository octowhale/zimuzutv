#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import requests
from core.crawlers import analysis
from core.storage import todaybucket, detailbucket, redisbucket
import json
from random import randint
import queue

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
        self.lock = threading.Lock()
        self.semaphore = threading.BoundedSemaphore(1)
        self.q = queue.PriorityQueue()
        self.is_login = False

    def login(self, is_login=True):
        """登录"""

        """todo: 是否登录判断，解决每次抓取都需要登录的尴尬"""
        r = self.s.post(self.LOGIN_URL, data=self.ZMZ_AUTH)

        rc = json.loads(r.content)

        for c in rc:
            print(c, rc[c])
            # if r.status_code != 200:
            #     print("登录失败")
            # else:
            #     print("登录成功")
            #     return (self.s)
            # self.s.get('http://www.zimuzu.tv/user/user/')

    def crawl_html(self, url):

        if not self.is_login:
            self.login()

        r = self.s.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        # self.dumps_to_file('xxx.html', r.text)
        return r.text

    def dumps_to_file(self, fname, content):
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

    def crawl_today(self):

        today_url = "{}/today".format(self.SITE)
        # r = self.s.get(today_url)
        # if r.status_code != 200:
        #     self.login()

        # print(today_url)
        html = self.crawl_html(today_url)

        items = analysis.today(html)

        threading.Thread(target=todaybucket.upsert, args=(items,)).start()

        # todaybucket.upsert(items)

        # self.is_login = True
        print(len(items))
        for item in items:
            page = item['m_detail'].split('/')[-1]
            # print(page)
            # threading.Thread(target=self.crawl_detail, args=(page,)).start()
            # print(item)

            self.q.put((10, page))

            # self.is_login = False

    def crawl_today_detail(self):

        while True:
            self.is_login = True
            pri, page = self.q.get()
            self.crawl_detail(page)
            # print(page)
            # time.sleep(1)
            self.is_login = False

    def crawl_today_loop(self):
        while True:
            self.crawl_today()
            print("等待 {} 秒继续执行下一次任务".format(self.time2wait))
            time.sleep(int(self.time2wait))

    def crawl_detail(self, page):
        """抓取影片所有相关连接

            page: 资源id
            pri: 队列权重
        """
        """todo: 引入 redis，解决每次点击都爬取页面的问题"""

        self.semaphore.acquire()
        # print('锁')

        now_time = time.time()

        # detail_update_sign = redisbucket.get_update_detail_info(page, now_time)
        is_crawl = self.redis_client.get_update_detail_info(page, now_time)
        if not is_crawl:
            """如果返回为 False， 则跳过更新"""
            self.semaphore.release()
            return None

        # 等待时间
        time.sleep(2)
        """开始更新页面"""
        """http://www.zimuzu.tv/resource/list/35575"""

        # time.sleep(randint(5, 10))
        detail_url = "{}/resource/list/{}".format(self.SITE, page)

        """判断是否需要抓取页面"""

        """抓取页面"""
        # print(page),
        html = self.crawl_html(detail_url)

        items = {'m_id': page, 'm_update_time': time.time()}
        items = analysis.detail(html, items)

        if items is None:
            self.semaphore.release()
            return None

        # print("zimuzu.Crawler,146,", items)
        # result = detailbucket.upsert(items)  # return True if success
        upsert_result = detailbucket.upsert(items)  # return True if success

        if upsert_result:
            """插入成功，更新 redis """
            print("{} 插入成功，更新 redis".format(page))
            self.redis_client.set_detail_update_info(page, now_time)
        else:
            """插入失败，重新排队"""
            print("{} 抓取失败，重新进入队列".format(page))
            self.q.put((20, page))

        # time.sleep(5)
        self.semaphore.release()
        # print('释放锁')


if __name__ == '__main__':
    zmz = ZimuzuCrawler()
    zmz.crawl_today()
