#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: opc_product_deal.py
# Email:
# Author: 唐政

import requests
import datetime
import json


url = 'http://192.168.4.50/zlsmart/query_pr_by_time_list_api'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Token': '4ac7ab3d-af24-4ed7-978e-0d9295545dcd',
}

params = {
    'org_id': 1,
    'time_interval': '2020-12-18,2020-12-22',
}
response = requests.post(
    url=url,
    json=params
)

if response.status_code == 200:
    content = response.content.decode('utf-8')
    content = json.loads(content)
    result_list = content['result']['list']

    need_list = []
    if result_list is not None:
        for obj in result_list:
            try:
                obj['assay_start_datetime'] = datetime.datetime.strptime(obj['assay_start_datetime'].split('+')[0],
                                                                         "%Y-%m-%d %H:%M:%S").replace(microsecond=0)
            except AttributeError:
                pass

            try:
                obj['supply_o_time_json'] = json.loads(obj['supply_o_time_json'])
            except:
                pass
            deal_time = datetime.datetime(2020, 12, 18, 0, 0, 0)
            if deal_time <= obj['assay_start_datetime']:
                need_list.append(obj)

    from request_deal.opc_trims_deal import query_opc_dict

    opc_start_time = datetime.datetime(2020, 12, 18, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
    opc_end_time = datetime.datetime(2020, 12, 23, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

    query_plc_flag_list = [
        # 'LG.PLC1_1.BH1_C_SJZ',
        # 'LG.PLC1_1.BH2_C_SJZ',
        # 'LG.PLC1_1.SBYSC_SJZ',
        # 'LG.PLC1_1.WNQC_SJZ',
        'LG.PLC1_1.QSBYSC_SJZ',
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

    trims_list = query_opc_dict(query_plc_flag_str, opc_start_time, opc_end_time)
    for obj in need_list:
        if obj['zl_id'] == 1 and obj['zl_start_time']:
            print(obj['lh'], end='\t')
            print(obj['zl_id'], end='\t')
            print(obj['zl_start_time'], end='\t')
            print(obj['zl_end_time'], end='\t')
            # print(obj['bai_hui_usage'], end='\t')
            print(obj['qing_shao_usage'], end='\t')
            try:
                obj['zl_start_time'] = datetime.datetime.strptime(obj['zl_start_time'].split('+')[0], "%Y-%m-%d %H:%M:%S")
                obj['zl_end_time'] = datetime.datetime.strptime(obj['zl_end_time'].split('+')[0], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                obj['zl_start_time'] = datetime.datetime.strptime(obj['zl_start_time'].split('.')[0], "%Y-%m-%d %H:%M:%S")
                obj['zl_end_time'] = datetime.datetime.strptime(obj['zl_end_time'].split('.')[0], "%Y-%m-%d %H:%M:%S")
            total = 0
            for trims in trims_list:
                if obj['zl_start_time'] <= trims['time'] <= obj['zl_end_time']:
                    total += trims['value']
            print(total, end='\t')
            for trims in trims_list:
                if obj['zl_start_time'] <= trims['time'] <= obj['zl_end_time']:
                    print(trims['time'], end='\t')
                    print(trims['value'], end='\t')
                    total += trims['value']
            print()

else:
    print(response.status_code)