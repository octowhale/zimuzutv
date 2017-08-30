#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import redis
import json


class RedisBucket(object):
    def __init__(self):
        with open('setting/redis_auth.json', 'r', encoding='utf-8') as f:
            redis_auth = json.load(f)

            redis_host, redis_port = redis_auth['host'], redis_auth['port']

            redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port)
            self.redis_client = redis.Redis(connection_pool=redis_pool)

    def get_update_detail_info(self, page, now_time):
        key = "r{}".format(page)
        update_time = self.redis_client.get(key)

        if update_time is None:
            return True

        if now_time - float(update_time) > 3600:
            return True
        else:
            return False

    def set_detail_update_info(self, page, update_time):
        key = 'r{}'.format(page)

        self.redis_client.set(key, update_time)

