#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: query_oxygen_use_list.py
# Email:
# Author: 唐政 

import datetime


def query_opc_dict(flag_str, start_time, end_time):
    error_str = ''
    query_start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    query_end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "opc_name_flag_list": flag_str,
        "time_interval": "{},{}".format(query_start_time_str, query_end_time_str),
        "max_num": 7000,
    }

    log_append('oxygen', query_start_time_str.split(' ')[1], query_end_time_str.split(' ')[1], '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="data_acquisition/query_opc_data_by_influx_db_list",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"生产信息吹氧时间匹配:query_opc_data_by_influx_db_list ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict['result'], error_str


def result_opc_deal(result_dict, flag_list):
    yq_dict = {}

    not_false_flag = False
    symmetry_flag = True
    for item in result_dict['list']:

        try:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f").replace(
                microsecond=0)
        except AttributeError:
            pass
        except:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S").replace(
                microsecond=0)

        if item['opc_name'] == flag_list:

            if item['value'] is True and not_false_flag is False:
                not_false_flag = True
            elif item['value'] is False and not_false_flag is False:
                continue

            if item['value'] is True and symmetry_flag is True:

                symmetry_flag = False
                yq_dict.setdefault("true", []).append(item['time'])
            elif item['value'] is False and symmetry_flag is False:

                symmetry_flag = True
                yq_dict.setdefault("false", []).append(item['time'])
            elif item['value'] is True and symmetry_flag is False:

                yq_dict["true"] = yq_dict["true"][:-1]
                yq_dict.setdefault("true", []).append(item['time'])
            elif item['value'] is False and symmetry_flag is True:
                continue

    if symmetry_flag is False:
        yq_dict["true"].pop()

    return yq_dict


num = 1
query_plc_flag_yq = 'LG.PLC{}.YQYL'.format(num)

now_datetime = datetime.datetime.now()
opc_start_time = now_datetime - datetime.timedelta(days=1)


result_yq, error_yq = query_opc_dict(query_plc_flag_yq, opc_start_time, now_datetime)

log_append("result_yq", result_yq, '', '')