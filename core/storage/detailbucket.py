#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import pymongo
import json

# mongo_auth = json.load(open('mongo_auth.json', 'r', encoding='utf-8'))
with open('setting/mongo_auth.json', 'r', encoding='utf-8') as f:
    mongo_auth = json.load(f)
    host, port = mongo_auth['host'], mongo_auth['port']


def upsert(items):
    """将影片信息记录在 mongodb 中，如存在，则更新
    如果返回为 True 表示插入成功
    """
    # print(__name__, items)
    # with pymongo.MongoClient('ss.tangx.in', 9200) as client:
    with pymongo.MongoClient(host, port) as client:
        db = client.zimuzu

        db.detail.update({'m_id': items['m_id']},
                         items,
                         upsert=True)

        find_result = exist_check(items['m_id'])
        # print('find_result: ', find_result)
        if find_result is None:
            return False

            # for item in find(items['m_id']):
            #     if item is None:
            #         return False
    return True


def find(page):
    """ 找到 page id 对应的剧集信息"""
    if page is None:
        return None

    with pymongo.MongoClient(host, port) as client:
        db = client.zimuzu
        items = db.detail.find({'m_id': '{}'.format(page)})

        # print(items)
        for item in items:
            # print(item)
            return item


def exist_check(page):
    """ 找到 page id 对应的剧集信息"""
    if page is None:
        return None

    with pymongo.MongoClient(host, port) as client:
        db = client.zimuzu
        items = db.detail.find({'m_id': '{}'.format(page)}, {"_id": 0, 'm_id': 1})

        # print(items)
        for item in items:
            # print(item)
            return item


def find_update_time(page):
    if page is None:
        return None

    with pymongo.MongoClient(host, port) as client:
        db = client.zimuzu

        db.detail.find({'m_id': page}, {'m_update_time': 1, "_id": 0})
        # db.detail.find({'m_id': page}, {'m_update_time': 1, "_id": 0})


if __name__ == "__main__":
    page = 34425
    find(34425)
