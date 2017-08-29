#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
from core.storage import todaybucket, detailbucket
from datetime import datetime


class ZimuzuShow(object):
    def __init__(self):
        self.dt_date = datetime.strftime(datetime.now(), "%m-%d")

    def today_find(self, dt_date=None):
        """查询当日更新，返回一个列表"""
        if dt_date is None:
            dt_date = self.dt_date

        items = todaybucket.find(dt_date)

        return items

    def detail_find(self, page=None):
        if page is None:
            return None

        items = detailbucket.find(page)

        return items
