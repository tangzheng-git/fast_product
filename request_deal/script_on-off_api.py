#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: script_on-off_api.py
# Email:
# Author: 唐政 

import requests
import datetime
import json


def control_script_on_off(script_id, on_off=False):
    url = 'http://192.168.4.50/async_script_task/set_current_run_script_version'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Token': '4ac7ab3d-af24-4ed7-978e-0d9295545dcd',
        'sessionid': 'znoakpsbasl87q7hszujdxpanv26ig1v'
    }

    params = {
        'org_id': 1,
        'is_current': on_off,
        'script_version_id': script_id,
    }
    response = requests.post(
        url=url,
        data=params,
        headers=headers
    )

    try:
        result_dict = json.loads(response.content.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        result_dict = response.content.decode('utf-8')

    message = result_dict['message']
    success = result_dict['success']


script_id = 1373
control_script_on_off(script_id)