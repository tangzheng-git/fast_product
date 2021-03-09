#!/usr/bin/env python
# encoding: utf-8
# Date: 2018/8/9 上午11:39
# file: formate_datetime.py
# Email: wangjian2254@icloud.com
# Author: 王健
import datetime



def formate_datetime(value):
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
    if value.find("+"):
        try:
            return datetime.datetime.strptime(value.split("+")[0], "%Y-%m-%dT%H:%M:%S.%f")
        except:
            try:
                return datetime.datetime.strptime(value.split("+")[0], "%Y-%m-%dT%H:%M:%S")
            except:
                pass
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
    except:
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d")
            except:

                try:
                    return datetime.datetime.strptime(value, "%Y%m%d")
                except:
                    try:
                        return datetime.datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")
                    except:
                        try:
                            return datetime.datetime.strptime(value, "%Y%m%d %H:%M:%S")
                        except:
                            try:
                                return datetime.datetime.strptime(value, "%Y%m%d%H%M%S")
                            except:
                                try:
                                    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
                                except Exception as e:
                                    raise e


def diff_seconds(start_time, end_time):
    """
    计算时间差值秒数
    :param start_time:
    :param end_time:
    :return:
    """
    return (end_time - start_time).days * 24 * 3600 + (end_time - start_time).seconds


def check_time_format_str(time_interval):
    if not time_interval[1]:
        import datetime
        end_time = datetime.datetime.now()
    else:
        end_time = time_interval[1]
    start_time = time_interval[0]
    return format_str_type(start_time, end_time)


def format_str_type(start_time, end_time):
    if start_time.year != end_time.year:
        return "%Y-%m-%d %H:%M:%S"
    elif start_time.month != end_time.month or start_time.day != end_time.day:
        return "%m-%d %H:%M:%S"
    else:
        return "%H:%M:%S"


def get_unit_by_seconds(seconds):
    if seconds / (60 * 60 * 24 * 7):
        return "%s周" % (seconds / (60 * 60 * 24 * 7))
    elif seconds / (60 * 60 * 24):
        return "%s天" % (seconds / (60 * 60 * 24))
    elif seconds / (60 * 60):
        return "%s小时" % (seconds / (60 * 60))
    elif seconds / 60:
        return "%s分钟" % (seconds / 60)
    else:
        return "%s秒钟" % seconds
