#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: opc_trims_deal.py
# Email:
# Author: 唐政 

import requests
import datetime
import json


def query_opc_dict(flag_string, start_time, end_time):

    url = 'http://192.168.4.50/data_acquisition/query_opc_data_by_influx_db_list'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Token': '4ac7ab3d-af24-4ed7-978e-0d9295545dcd',
    }

    data_param = {
        "opc_name_flag_list": flag_string,
        "time_interval": "{},{}".format(start_time, end_time),
        "max_num": 7000,
    }
    response = requests.post(
        url=url,
        json=data_param
    )

    content = response.content.decode('utf-8')
    content = json.loads(content)
    result_list = content['result']['list']
    print(result_list)

    trims_list = []
    if result_list is not None:
        for obj in result_list:
            try:
                obj['time'] = datetime.datetime.strptime(obj['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                obj['time'] = datetime.datetime.strptime(obj['time'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            trims_list.append(obj)

    return trims_list


opc_start_time = datetime.datetime(2020, 12, 18, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
opc_end_time = datetime.datetime(2020, 12, 18, 23, 59, 59).strftime("%Y-%m-%d %H:%M:%S")

query_plc_flag_list = [
    'LG.PLC1_1.BH1_C_SJZ',
    # 'LG.PLC1_1.BH2_C_SJZ',
    # 'LG.PLC1_1.SBYSC_SJZ',
    # 'LG.PLC1_1.WNQC_SJZ',
    # 'LG.PLC1_1.QSBYSC_SJZ',
    #
    # 'LG.PLC2_1.BH1_C_SJZ',
    # 'LG.PLC2_1.BH2_C_SJZ',
    # 'LG.PLC2_1.SBYSC_SJZ',
    # 'LG.PLC2_1.FZC_SJZ',
    # 'LG.PLC2_1.WNQC_SJZ',
    # 'LG.PLC2_1.QSBYSC_SJZ',
    #
    # 'LG.PLC3.BH1_C_SJZ',
    # 'LG.PLC3.SBYSC_SJZ',
    # 'LG.PLC3.FZC_SJZ',
]
query_plc_flag_str = ','.join(query_plc_flag_list)

query_opc_dict(query_plc_flag_str, opc_start_time, opc_end_time)