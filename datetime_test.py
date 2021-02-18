#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/28
# file: datetime_test.py
# Email:
# Author: 唐政 

import datetime
from dateutil import relativedelta


# 获取前一天, 本周, 上周, 本月一号, 上月一号
def datetime_delta_contrast(deal_datetime):
    # 昨天
    yestoday = deal_datetime - datetime.timedelta(days=1)
    # 本月一号
    this_month_start = deal_datetime.replace(day=1)
    # 上月一号
    last_month_start = deal_datetime.replace(day=1) - relativedelta.relativedelta(months=1)

    # 周一 1 -- 周日 7
    day_num = deal_datetime.isoweekday()
    # 本周日
    on_sunday = deal_datetime - datetime.timedelta(days=day_num - 7)
    # 上周日
    last_sunday = deal_datetime - datetime.timedelta(days=day_num)
    # 上上周日
    before_last_sunday = deal_datetime - datetime.timedelta(days=day_num + 7)

    dic = {7: 0, 6: 6, 5: 5, 4: 4, 3: 3, 2: 2, 1: 1}
    day_num = dic[day_num]
    # 周日 0 -- 周六 6
    # 本周日
    on_sunday = deal_datetime - datetime.timedelta(days=day_num)
    # 上周日
    last_sunday = deal_datetime - datetime.timedelta(days=day_num + 7)


# datetime 方法测试
def datetime_func_test():
    now = datetime.datetime.now()

    now_datetime = now
    now_date = now.date()
    now_time = now.time()

    now_datetime_test = now.isocalendar()
    now_date_test = now.date().isoweekday()
    now_time_test = now.time()

    test_datetime = datetime.datetime.isoweekday(now_datetime)
    test_date = datetime.date.isoweekday(now_date)
    test_time = datetime.time

    print(now_datetime, type(now_datetime))
    print(now_date, type(now_date))
    print(now_time, type(now_time))
    print()

    print(now_datetime_test, type(now_datetime_test))
    print(now_date_test, type(now_date_test))
    print(now_time_test, type(now_time_test))
    print()

    print(test_datetime, type(test_datetime))
    print(test_date, type(test_date))
    print(test_time, type(test_time))
    print()

    print(datetime.datetime.now())
    print(datetime.datetime.today())
    print(datetime.date.today())


# 返回指定区间的datetime list
def date_range(beginDate, endDate):
    date_list = []
    date = beginDate.date()
    endDate = endDate.date()

    while date <= endDate:
        date_list.append(date.strftime("%Y-%m-%d"))
        date = date + datetime.timedelta(days=1)

    return date_list





