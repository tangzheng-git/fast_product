#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: product_deal.py
# Email:
# Author: 唐政

import requests
import datetime
import json


def query_opc_dict(flag_string, start_time, end_time):
    error_str = ''
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "opc_name_flag_list": flag_string,
        "time_interval": "{},{}".format(start_time_str, end_time_str),
        "max_num": 7000,
    }

    log_append('opc time', start_time_str, end_time_str, '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="data_acquisition/query_opc_data_by_influx_db_list",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"opc信息吹氧时间匹配:query_opc_data_by_influx_db_list ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict['result'], error_str


def query_product_by_time_dict(start_time, end_time):
    error_str = ""
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "org_id": 1,
        "time_interval": "{},{}".format(start_time_str, end_time_str),
    }

    log_append('product time', start_time_str, end_time_str, '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="zlsmart/query_pr_by_time_list_api",
                                           data_parms=data_param,
                                           timeout=60, is_log=False)
    if code != 0:
        error_str = u"生产信息吹氧时间匹配:query_pr_by_time_list_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict['result'], error_str


def update_product_api(product_id, supply_o_time_json=None, o2_usage=None):
    error_str = ""

    data_param = {
        "org_id": 1,
        "product_id": product_id
    }

    if supply_o_time_json:
        data_param['supply_o_time_json'] = supply_o_time_json

    if o2_usage:
        data_param['o2_usage'] = o2_usage

    log_append('update param', data_param, '', '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="zlsmart/update_pr_api",
                                           data_parms=data_param,
                                           timeout=60, is_log=False)
    if code != 0:
        error_str = u"生产信息更新:update_pr_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict, error_str


def result_opc_deal(result_dict, flag_list):
    yq_dict = {}
    wd_dict = {}
    yl_dict = {}

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

        if item['opc_name'] == flag_list[0]:

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

        if item['opc_name'] == flag_list[1]:
            if 1200 < int(item['value']) <= 1800:
                wd_dict.setdefault("value", []).append(int(item['value']))
                wd_dict.setdefault("time", []).append(item['time'])

        if item['opc_name'] == flag_list[2] and item['type'] == "value":
            yl_dict.setdefault("value", []).append(item['value'])
            yl_dict.setdefault("time", []).append(item['time'])

    if symmetry_flag is False:
        yq_dict["true"].pop()

    return yq_dict, wd_dict, yl_dict


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


now_datetime = datetime.datetime.now()
pr_start_time = now_datetime - datetime.timedelta(minutes=30)
opc_start_time = pr_start_time - datetime.timedelta(hours=1.5)
deal_end_time = now_datetime

# 即时模式 1
# 回溯模式 0
pattern = 0
num = '1'
script_id = 1417

query_plc_flag_list = [
    'LG.PLC{}.YQKC'.format(num),
    'LG.PLC{}.ZDWD'.format(num),
    'LG.PLC{}.YQYL'.format(num)
]

query_plc_flag_string = ','.join(query_plc_flag_list)

if result and pattern == 1:
    # 即时
    pr_start_time_get = result.get('pr_start_time', None)

    if pr_start_time_get is not None:
        pr_start_time = pr_start_time_get
        opc_start_time = pr_start_time - datetime.timedelta(hours=1.5)

    log_append("result now", result, '', '')

elif result and pattern == 0 and result.get('Back_in_time_flag', None) == 1:
    # 回溯中
    deal_end_time = result.get('Back_in_time', deal_end_time) + datetime.timedelta(hours=3)
    max_product_time = result.get('max_product_time', deal_end_time)

    result['Back_in_time'] = deal_end_time

    if deal_end_time <= max_product_time:
        pr_start_time = deal_end_time - datetime.timedelta(hours=3.5)
        opc_start_time = deal_end_time - datetime.timedelta(hours=4)
    else:
        control_script_on_off(script_id)
        save_result_msg("回溯结束")
        result['Back_in_time_flag'] = 0

    log_append("result Backing", result, '', '')

elif result and pattern == 0 and result.get('Back_in_time_flag', None) == 0:
    # 开启回溯
    deal_end_time = datetime.datetime(2020, 12, 18, 0, 0, 0)

    result['Back_in_time'] = deal_end_time
    result['Back_in_time_flag'] = 1

    pr_start_time = deal_end_time - datetime.timedelta(hours=3.5)
    opc_start_time = deal_end_time - datetime.timedelta(hours=4)

    log_append("result Back", result, '', '')


result_product, error_product = query_product_by_time_dict(pr_start_time, deal_end_time)

if result_product is not None:
    product_list = result_product['list']

    for obj in product_list:
        try:
            obj['assay_start_datetime'] = datetime.\
                datetime.strptime(obj['assay_start_datetime'].split('+')[0], "%Y-%m-%d %H:%M:%S").replace(microsecond=0)
        except AttributeError:
            pass

    result_yq, error_yq = query_opc_dict(query_plc_flag_string, opc_start_time, deal_end_time)

    plc_yq_dict, plc_wd_dict, plc_yl_dict = result_opc_deal(result_yq, query_plc_flag_list)

    # if result_yq.get('list') is not None:
    #     log_append("result_opc", result_yq, "result_opc list", result_yq['list'])
    # else:
    #     log_append("result_opc", result_yq, '', '')
    #
    # if plc_yq_dict.get('true') is not None:
    #     log_append('yq_dict', plc_yq_dict, len(plc_yq_dict['true']), len(plc_yq_dict['false']))
    # else:
    #     log_append("yq_dict", plc_yq_dict, '', '')
    #
    # if plc_wd_dict.get('value') is not None:
    #     log_append("wd_dict wd", plc_wd_dict['value'], "wd_dict time", plc_wd_dict['time'])
    # else:
    #     log_append("wd_dict", plc_wd_dict, '', '')
    #
    # log_append("yl_dict", [[plc_yl_dict['time'][i], plc_yl_dict['value'][i]] for i, value in enumerate(plc_yl_dict['value'])], '', '')
    #
    # log_append("product", result_product, 'time list',
    #            [item['assay_start_datetime'] for item in product_list if item['zl__flag'] == num])

    def result_pr_deal(deal_list, yq_dict, wd_dict, yl_dict):

        t_list = yq_dict.get('true', [])
        f_list = yq_dict.get('false', [])

        wd_time_list = wd_dict.get('time', [])
        wd_value_list = wd_dict.get('value', [])

        o2_yl_time_list = yl_dict.get('time', [])
        o2_yl_value_list = yl_dict.get('value', [])

        oxygen_list_use = [0] * len(f_list)
        temp_list_use = [0] * len(wd_time_list)

        msg_dict = {
            'yq': [],
            'wd': [],
            'hb': []
        }

        for item in deal_list:

            item['id'] = str(item['id'])
            assay_time = item.get('assay_start_datetime', None)
            zl_flag = item.get('zl__flag', None)
            oxygen_use_index = 0
            supply_o_time_list = []

            if assay_time and zl_flag == num and len(f_list) != 0:
                up_true_value = min(t_list)
                up_false_value = min(f_list)

                for f_index, false_time in enumerate(f_list):

                    if (assay_time - up_false_value).seconds < 900 and oxygen_list_use[oxygen_use_index] == 0:
                        if item['id'] not in msg_dict['yq']:
                            msg_dict['yq'].append(item['id'])

                        oxygen_list_use[oxygen_use_index] = 1

                        supply_o_time_dict = {
                            "supply_o_start_time": up_true_value,
                            "supply_o_end_time": up_false_value,
                            "sustain_time": (up_false_value - up_true_value).seconds,
                            "temp": None,
                            "temp_time": None,
                            "o2_usage": None,
                        }

                        # 默认终点温度
                        if wd_dict.get('value', None) is not None:
                            up_wd_index = 0
                            for wd_index, temp_time in enumerate(wd_time_list):
                                if up_false_value <= temp_time <= up_false_value + datetime.timedelta(seconds=300) and 0 == temp_list_use[wd_index]:
                                    if supply_o_time_dict.get('temp', None):
                                        if supply_o_time_dict['temp'] < wd_value_list[wd_index]:
                                            supply_o_time_dict['temp'] = wd_value_list[wd_index]
                                            supply_o_time_dict['temp_time'] = wd_time_list[wd_index]
                                            temp_list_use[wd_index] = 1
                                            temp_list_use[up_wd_index] = 0
                                            up_wd_index = wd_index
                                    else:
                                        supply_o_time_dict['temp'] = wd_value_list[wd_index]
                                        supply_o_time_dict['temp_time'] = wd_time_list[wd_index]
                                        if item['id'] not in msg_dict['wd']:
                                            msg_dict['wd'].append(item['id'])
                                        temp_list_use[wd_index] = 1
                                        up_wd_index = wd_index

                        if supply_o_time_list and (supply_o_time_dict['supply_o_start_time'] - supply_o_time_list[-1]['supply_o_end_time']).seconds <= 30:
                            # 间隔时间过短处理
                            if item['id'] not in msg_dict['hb']:
                                msg_dict['hb'].append(item['id'])
                            supply_o_time_list[-1] = {
                                "supply_o_start_time": supply_o_time_list[-1]['supply_o_start_time'],
                                "supply_o_end_time": supply_o_time_dict['supply_o_end_time'],
                                "sustain_time": (supply_o_time_dict['supply_o_end_time'] - supply_o_time_list[-1]['supply_o_start_time']).seconds,
                                "temp": supply_o_time_dict['temp'] if supply_o_time_dict.get('temp', None) else supply_o_time_list[-1].get('temp', None),
                                "temp_time": supply_o_time_dict['temp_time'] if supply_o_time_dict.get('temp_time', None) else supply_o_time_list[-1].get('temp_time', None),
                                "o2_usage": None,
                            }
                        elif supply_o_time_list:
                            # 区间终点温度处理
                            if wd_dict.get('value', None):
                                up_wd_index = 0
                                supply_o_time_list[-1]['temp_time'] = None
                                supply_o_time_list[-1]['temp'] = None

                                for wd_index, temp_time in enumerate(wd_time_list):
                                    if supply_o_time_list[-1]['supply_o_end_time'] <= temp_time <= supply_o_time_dict['supply_o_start_time'] and 0 == temp_list_use[wd_index]:
                                        if supply_o_time_list[-1].get('temp', None):
                                            if supply_o_time_list[-1]['temp'] < wd_value_list[wd_index]:
                                                supply_o_time_list[-1]['temp'] = wd_value_list[wd_index]
                                                supply_o_time_list[-1]['temp_time'] = wd_time_list[wd_index]
                                                temp_list_use[wd_index] = 1
                                                temp_list_use[up_wd_index] = 0
                                                up_wd_index = wd_index
                                        else:
                                            supply_o_time_list[-1]['temp'] = wd_value_list[wd_index]
                                            supply_o_time_list[-1]['temp_time'] = wd_time_list[wd_index]
                                            if item['id'] not in msg_dict['wd']:
                                                msg_dict['wd'].append(item['id'])
                                            temp_list_use[wd_index] = 1
                                            up_wd_index = wd_index

                            supply_o_time_list.append(supply_o_time_dict)
                        else:
                            supply_o_time_list.append(supply_o_time_dict)

                        if result.get('pr_start_time', None):
                            result['pr_start_time'] = max(result['pr_start_time'], assay_time)
                        else:
                            result['pr_start_time'] = assay_time

                        if result.get('max_product_time', None):
                            result['max_product_time'] = max(result['max_product_time'], assay_time)
                        else:
                            result['max_product_time'] = assay_time

                    if (f_list[f_index] - t_list[f_index]).seconds < 900:
                        up_false_value = f_list[f_index]
                        up_true_value = t_list[f_index]
                        oxygen_use_index = f_index

            if supply_o_time_list:
                # 氧气用量处理
                # 时间处理
                for supply_o_index, supply_o_time in enumerate(supply_o_time_list):
                    start_time = supply_o_time['supply_o_start_time']
                    end_time = supply_o_time['supply_o_end_time']

                    supply_o_time['supply_o_start_time'] = supply_o_time['supply_o_start_time'].strftime("%Y-%m-%d %H:%M:%S")
                    supply_o_time['supply_o_end_time'] = supply_o_time['supply_o_end_time'].strftime("%Y-%m-%d %H:%M:%S")
                    if supply_o_time['temp_time']:
                        supply_o_time['temp_time'] = supply_o_time['temp_time'].strftime("%Y-%m-%d %H:%M:%S")

                    o2_yl_min_value = 0
                    o2_yl_max_value = 0
                    for i, yl_time in enumerate(o2_yl_time_list):
                        if start_time <= yl_time <= end_time:
                            if type(o2_yl_value_list[i]) != bool:
                                if o2_yl_min_value == 0:
                                    o2_yl_min_value = o2_yl_value_list[i]
                                else:
                                    o2_yl_min_value = min(o2_yl_min_value, o2_yl_value_list[i])
                                o2_yl_max_value = max(o2_yl_max_value, o2_yl_value_list[i])
                    if o2_yl_min_value < 200:
                        supply_o_time['o2_usage'] = o2_yl_max_value
                    else:
                        supply_o_time['o2_usage'] = o2_yl_max_value - o2_yl_min_value

                import json
                supply_o_time_json = json.dumps(supply_o_time_list)
                update_product_api(item['id'], supply_o_time_json=supply_o_time_json)

        msg_list = []
        if msg_dict['yq']:
            msg_list.append("氧气更新id {}".format(','.join(msg_dict['yq'])))
        if msg_dict['wd']:
            msg_list.append("温度更新id {}".format(','.join(msg_dict['wd'])))
        if msg_dict['hb']:
            msg_list.append("合并更新id {}".format(','.join(msg_dict['hb'])))

        if msg_list:
            save_result_msg(" ".join(msg_list))
        else:
            save_result_msg("当前无操作")

    result_pr_deal(product_list, plc_yq_dict, plc_wd_dict, plc_yl_dict)


