#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import pymongo
import json
from datetime import datetime


def update(dtdate=None):
    """获取当日更新列表"""
    # with open(os.path.join('..', 'setting/mongosvr.json')) as f:
    if dtdate is None:
        dtdate = datetime.strftime(datetime.now(), "%m-%d")

    """定位 json 位置"""
    if __name__ == "__main__":
        with open(os.path.join('..', 'setting/mongosvr.json')) as f:
            mongosvr = json.load(f)
    else:

        with open('setting/mongosvr.json') as f:
            mongosvr = json.load(f)

    mongo_client = pymongo.MongoClient(mongosvr['host'], mongosvr['port'])

    db = mongo_client.zimuzu

    # for movie in db.today.find({'m_title': "/你的名字/"}).inserted_id:
    # for movie in db.today.find({'m_title': "你的名字.Kimi.No.Na.Wa.2016.1080p.Bluray-深影字幕组.mp4"}):
    movie_list = []
    # for movie in db.today.find({"m_title": "manhole.奉必的梦游仙境.第4集.720p.HDTV.x264.中韩双语字幕-深影字幕组.mp4"}):

    # for movie in db.today.find({'m_date': dtdate}).sort('area'):
    """排序"""
    for movie in db.today.find({'m_date': dtdate}).sort('m_update_time', -1):
        # print(movie)

        movie_list.append(movie)


    if len(movie_list) == 0:
        return None
    else:
        return movie_list


if __name__ == '__main__':
    update()
