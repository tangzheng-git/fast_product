#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/21
# file: query_product_api.py
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
    'time_interval': '2020-12-20,2020-12-19',
}
response = requests.post(
    url=url,
    json=params
)

if response.status_code == 200:
    content = response.content.decode('utf-8')
    content = json.loads(content)
    result = content['result']
    print(result)