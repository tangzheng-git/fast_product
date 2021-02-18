#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: query_oxygen_switch_list.py
# Email:
# Author: 唐政 

import datetime


def query_opc_dict(flag_str, start_time, end_time):
    error_str = ''
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "opc_name_flag_list": flag_str,
        "time_interval": "{},{}".format(start_time_str, end_time_str),
        "max_num": 7000,
    }

    log_append('oxygen', start_time_str, end_time_str, '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="data_acquisition/query_opc_data_by_influx_db_list",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"opc数据查询:query_opc_data_by_influx_db_list ERROR code-{} error-{}".format(code, error)
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
query_plc_flag_yq = 'LG.PLC{}.YQKC'.format(num)

now_datetime = datetime.datetime.now()
opc_start_time = now_datetime - datetime.timedelta(days=1)


result_yq, error_yq = query_opc_dict(query_plc_flag_yq, opc_start_time, now_datetime)

plc_yq_dict = result_opc_deal(result_yq, query_plc_flag_yq)

lis = []
if plc_yq_dict.get('true') is not None:
    for i, value in enumerate(plc_yq_dict['true']):
        seconds = (plc_yq_dict['false'][i] - value).seconds
        if 10 < seconds < 90:

            log_append(value.time(), plc_yq_dict['false'][i].time(), seconds, True)

            lis.append((value.time(), plc_yq_dict['false'][i].time(), seconds))
else:
    log_append("plc_yq_dict", plc_yq_dict, '', '')

if lis:
    log_append("seconds lis", lis, '', '')