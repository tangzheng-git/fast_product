#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/21
# file: lg_product_deal.py
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
    for obj in need_list:
        if obj['supply_o_time_json']:

            print(obj['lh'], end='\t')
            print(obj['zl_id'], end='\t')
            print(obj['assay_start_datetime'], end='\t')
            for item in obj['supply_o_time_json']:

                try:
                    item['supply_o_end_time'] = datetime.datetime.strptime(item['supply_o_end_time'], "%Y-%m-%d %H:%M:%S")
                    if item['temp_time']:
                        item['temp_time'] = datetime.datetime.strptime(item['temp_time'], "%Y-%m-%d %H:%M:%S")
                except AttributeError:
                    pass
                print(item['supply_o_start_time'], end='\t')
                print(item['supply_o_end_time'], end='\t')
                print(item['temp'], end='\t')
                print(item['temp_time'], end='\t')
                if item.get('o2_usage', None):
                    print(item['o2_usage'], end='\t')
                else:
                    print('None', end='\t')
            print()
        else:
            print()

else:
    print(response.status_code)