#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
import redis

import time

redis_host = '127.0.0.1'
redis_port = 6379

redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port)

redis_client = redis.Redis(connection_pool=redis_pool)

time_start = time.time()

print(type(time_start))

redis_client.set('r12345', time_start)

b_time_stop = redis_client.get('r12345')

print(type(b_time_stop))

time_stop = float(b_time_stop)

print(type(time_stop))

print(time_start, time_stop)


print(type(redis_client.get('adfkajsdf')))