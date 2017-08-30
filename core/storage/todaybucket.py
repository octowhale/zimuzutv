#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import pymongo
import json

with open('setting/mongo_auth.json', 'r', encoding='utf-8') as f:
    mongo_auth = json.load(f)
    host, port = mongo_auth['host'], mongo_auth['port']


def upsert(items):
    """将影片信息记录在 mongodb 中，如存在，则更新"""
    # with pymongo.MongoClient('ss.tangx.in', 9200) as client:
    with pymongo.MongoClient(host, port) as client:
        for item in items:
            db = client.zimuzu

            db.today.update({'m_title': item['m_title']},
                            item,
                            upsert=True)


def find(dt_date=None):
    """查找某日的影片信息"""
    if dt_date is None:
        dt_date = '08-29'
    with pymongo.MongoClient(host, port) as client:
        db = client.zimuzu

        items = [item for item in db.today.find({'m_date': dt_date}).sort('m_update_time', -1)]

        return items


def main():
    pass


if __name__ == '__main__':
    main()
