#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: time_interval.py
# Email:
# Author: 唐政 
import datetime
import query


get_result = print
time_interval=("日期区间", "r,[datetime]")

start_time = time_interval[0]
end_time = time_interval[1]
if start_time and end_time:
    if start_time > end_time:
        print(u'开始日期不能大于结束日期')
    query = query.filter(create_time__gte=start_time, create_time__lte=end_time + datetime.timedelta(days=1))
else:
    if start_time:
        query = query.filter(create_time__gte=start_time)
    if end_time:
        query = query.filter(create_time__lte=end_time + datetime.timedelta(days=1))
