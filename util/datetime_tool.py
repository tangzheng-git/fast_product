#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/03/02
# file: datetime_tool.py
# Email:
# Author: 唐政 

import datetime


def time_diff(end_t, start_t):
    start_time = datetime.datetime.strptime(start_t, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime(end_t, '%Y-%m-%d %H:%M:%S')
    seconds = (end_time - start_time).total_seconds()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


date_1 = '2021-03-01'
date_2 = '2021-03-01'
s_time_1 = '{} 18:33:40'.format(date_1)
e_time_1 = '{} 18:43:10'.format(date_1)
s_time_2 = '{} 18:47:40'.format(date_1)
e_time_2 = '{} 18:50:15'.format(date_1)

print('首段 ', time_diff(e_time_1, s_time_1))
print('间隔 ', time_diff(s_time_2, e_time_1))
print('次段 ', time_diff(e_time_2, s_time_2))
print('整段 ', time_diff(e_time_2, s_time_1))