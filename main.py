#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
from datetime import datetime
from flask import Flask, render_template
from core import ZimuzuCrawler, ZimuzuShow
import threading

app = Flask(__name__)


@app.route('/')
@app.route('/today.html')
def today_url():
    dt_date = datetime.strftime(datetime.now(), "%m-%d")

    datas = zmz_show.today_find(dt_date)

    return render_template('today.html', datas=datas, dtdate=dt_date)
    # return render_template('today.html')


def crawl_today():
    zmz.crawl_today_loop()


@app.route('/resource/<int:page>')
def crawl_detail(page):
    """抓取页面详细信息"""
    # zmz.crawl_detail(page)
    t = threading.Thread(target=zmz.crawl_detail, args=(page,))
    t.start()
    """展示页面"""
    data = zmz_show.detail_find(page)

    # print(data)

    if data is None:
        return render_template('404.html')
    # print(data)
    return render_template('detail.html', data=data)


def main():
    spider = threading.Thread(target=crawl_today)
    spider.start()

    spider2 = threading.Thread(target=zmz.crawl_today_detail)
    spider2.start()

    app.run('127.0.0.1', 23333)
    pass


if __name__ == '__main__':
    # app.run('127.0.0.1', 23333)

    zmz = ZimuzuCrawler.ZimuzuCrawler(3600)
    zmz_show = ZimuzuShow.ZimuzuShow()
    main()
