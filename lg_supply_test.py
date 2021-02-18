#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/20
# file: lg_supply_test.py
# Email:
# Author: 唐政 


import datetime
from functools import reduce


# python2字符串转时间
# 列表前后差值
def time_change_and_front_later_diff():
    time_value_list = [
        ["2020-12-05 09:43:53.000000", 21690],
        ["2020-12-05 09:43:54.000000", 22749],
    ]

    for i in time_value_list:
        try:
            i[0] = datetime.datetime.strptime(i[0].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f").replace(
                microsecond=0)
        except AttributeError:
            pass
        except:
            i[0] = datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)

    for front, later in zip(time_value_list, time_value_list[1:]):
        print('{} {} {}'.format((later[1] + front[1]) / 2,
                                (later[0] - front[0]).seconds,
                                (later[0] - front[0]).seconds * (later[1] + front[1]) / 2))


# json和python对象转换
def json_dumps_loads_test():
    lis = [{
        "1": 1,
        "2": 2
    }]

    import json

    lis_json = json.dumps(lis)
    print(lis_json, type(lis_json))

    lis = json.loads(lis_json)
    print(lis[-1], type(lis[-1]))

    lis_json = json.dumps(lis)
    print(lis_json, type(lis_json))
