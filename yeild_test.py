#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: yeild_test.py
# Email:
# Author: 唐政 


def consumer():
    r = '开始cmd '
    i = 0
    while True:
        get = yield r
        if not get:
            return
        print("检测获取 {}".format(get))
        i += 1
        print('分配 {} OK'.format(i))
        r = i


def produce(c):
    print(c.send(None))
    n = 0
    while n < 5:
        n += 1
        print('获取编号 {}'.format('get'))
        num = c.send('get')
        print('得到编号 {}'.format(num))
        print()
    c.close()


c = consumer()
produce(c)