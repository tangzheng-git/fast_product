#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/01/13
# file: error_bind_deal.py
# Email:
# Author: 唐政
import datetime

from util.script_api import get_result_by_remote_consul_server, log_append


# 获取当前生产线称重数据

def get_influxdb_data(start_time, end_time, opc_name):
    from util.influx_client import influxdb_client
    from util.influxdb_tools import influx_get_points_fun, influx_get_points
    sql = "select value_f, opc_name from liyu_opc_data where opc_name='%s' and type='value' and time >= '%s' and time < '%s' tz('Asia/Shanghai');" % (
        opc_name, start_time, end_time)
    tmp = influxdb_client.query(sql)
    l = list(influx_get_points(tmp))
    l.sort(key=lambda x: x['time'])
    if l:
        return l
    else:
        return []





def query_opc_info_list(flag_string, start_time, end_time):
    error_str = None
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "opc_name_flag_list": flag_string,
        "time_interval": "{},{}".format(start_time_str, end_time_str),
        "max_num": 14400,
    }

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="liyumes",
                                           url="data_acquisition/query_opc_data_by_influx_db_list",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"opc称重信息获取匹配:query_opc_data_by_influx_db_list ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str



def query_error_bind_rule_list_api(_aim_org_id):
    error_str = None
    data_param = {
        'aim_org_id': _aim_org_id
    }

    code, error, result_dict = \
        get_result_by_remote_consul_server(
            service_name="liyumes_offline",
            url="production_manage/api/query_error_bind_rule_list_api",
            data_parms=data_param,
            timeout=180,
            is_log=False
        )

    if code != 0:
        error_str = u"错捆预警规则查询:query_error_bind_rule_list_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    if result_dict and result_dict.get('result', None):
        return result_dict['result'], error_str
    else:
        return result_dict, error_str


import datetime
from production_manage.models import ProductionRecord, ProductItem, ProductionRecordItem


def query_product_item_list_api(_aim_org_id):
    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__gongyi__name', 'plan_item__trade_no_id') \
        .filter(org_id=aim_org_id, is_active=True).order_by("-create_time")

    if record_query is None:
        return None

    if len(record_query) >= 2:
        record_query = record_query[:2]
    else:
        record_query = record_query[:1]

    result_list = []
    record_query.reverse()

    for record in record_query:

        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'num', 'diameter', 'fixed_length', 'truck_no', 'create_time') \
            .using(aim_org_id).filter(is_active=True, org_id=aim_org_id, roll_no=record['plan_item__roll_no'])

        record_item_query = ProductionRecordItem.objects.values('id', 'real_weight').using(aim_org_id) \
            .filter(org_id=aim_org_id, production_record_id=record['id'], is_active=True) \
            .exclude(conclusion=ProductionRecordItem.Conclusion_None, )

        for item, record_item in zip(item_query, record_item_query):
            result_dict = {
                'product_record_id': record['id'],
                'record_item_id': record_item['id'],
                'item_id': item['id'],
                'roll_no': record['plan_item__roll_no'],
                'bind_no': item['bind_no'],
                'merge_no': item['merge_no'],
                'num': item['num'],
                'steel_type_id': record['plan_item__trade_no_id'],
                'diameter': item['diameter'],
                'fixed_length': item['fixed_length'],
                'create_time': item['create_time'],
                'gongyi': record['plan_item__gongyi__name'],
                'real_weight': record_item['real_weight'],
            }
            result_list.append(result_dict)

    return result_list


now_datetime = datetime.datetime.now()
opc_start_time = now_datetime - datetime.timedelta(hours=1)
opc_end_time = now_datetime

start_time_str = opc_start_time.strftime("%Y-%m-%d %H:%M:%S")
end_time_str = opc_end_time.strftime("%Y-%m-%d %H:%M:%S")

product_plc_flag_dict = {
    # 高线a
    'gaoxianA.chengpinkun_chengzhong': 1,
    # 高线b
    'gaoxianB.chengpinkun_chengzhong': 2,
    # 二轧
    'er_zha.chengpinkun_chengzhong': 4,
    # 三轧
    'san_zha.chengpinkun_chengzhong': 5,
    # 小棒生产线
    'xiaobang.chengpinkun_chengzhong': 15,
    # 高棒
    'gaobang.chengpinkun_chengzhong': 19,
}

query_plc_flag_string = 'gaobang.chengpinkun_chengzhong'

result_opc_list = get_influxdb_data(start_time_str, end_time_str, query_plc_flag_string)

log_append('opc', result_opc_list, '', '')
# 没有opc数据不操作

if result_opc_list:
    aim_org_id = product_plc_flag_dict[query_plc_flag_string]

    # 获取数据库中捆数
    database_bind_count = 3
    # opc与数据库匹配时间范围
    bind_time_match_min = -600
    bind_time_match_max = 600
    # opc与数据库匹配重量范围
    bind_weight_match_min = -50
    bind_weight_match_max = 50
    # 停工时间范围
    stop_work_time_min = -300
    stop_work_time_max = 300

    start_flag = 0
    up_item = {}
    _list = []
    deal_weight_list = []
    # 处理opc数据 获取opc称重数据
    for item in result_opc_list:

        try:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f").replace(
                microsecond=0)
        except AttributeError:
            pass

        except:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S").replace(
                microsecond=0)

        if start_flag == 0 and item.get('value', None) != 0 and up_item.get('value', None) == 0:
            # print('开始')
            # print('...')
            start_flag = 1
            _list = []

        if start_flag == 1 and item.get('value', None) != 0:

            _list.append(item)

        if start_flag == 1 and item.get('value', None) == 0 and up_item.get('value', None) != 0:
            # print('结束')
            start_flag = 0
            _dict = {}
            for obj in _list:
                if _dict.get(obj['value'], None):
                    _dict[obj['value']] += 1
                else:
                    _dict[obj['value']] = 1

            weight = 0
            for key, value in _dict.items():
                if value == max(_dict.values()):
                    weight = key

            time_list = []
            for obj in _list:
                if obj.get('value', None) == weight and obj.get('time', None):
                    time_list.append(obj['time'])
            if time_list:
                time = time_list[int(len(time_list) / 2)]

                deal_weight_list.append({
                    'weight': weight,
                    'time': time,
                })
        up_item = item

    log_append('weight', deal_weight_list, '', '')

    # 获取生产信息
    database_product_list = query_product_item_list_api(aim_org_id)

    if database_product_list:

        # 查看 数据库源数据
        for item in database_product_list:
            log_append('product', item['diameter'], item['fixed_length'], '')

        deal_product_list = []
        # 处理最近指定 捆数 数据
        if len(database_product_list) >= database_bind_count:
            deal_product_list = database_product_list[-database_bind_count:]

        # 查看 数据库处理数据
        # for item in deal_product_list:
        #     print(item)

        # 获取规则
        database_rule_dict, error_rule = query_error_bind_rule_list_api(aim_org_id)
        database_rule_list = database_rule_dict.get('list', [])

        # 查看 数据库源规则数据
        # for item in database_rule_list:
        #     print(item)

        deal_rule_dict = {}
        # 处理规则
        for item in database_rule_list:
            deal_rule_dict.setdefault(item['diameter'], {}).setdefault(item['dingchi'], [item['weight_max'], item['weight_min']])

        # 查看 数据库处理规则数据
        # for item in deal_rule_dict.items():
        #     print(item)

        # 匹配数据库中对应捆 无匹配则选择最后
        new_weight_data = {}
        new_product_data = database_product_list[-1]
        if deal_weight_list:
            new_weight_data = deal_weight_list[-1]
            for item in deal_product_list:
                item['create_time'] = datetime.datetime.strptime(item['create_time'], "%Y-%m-%d %H:%M:%S")

                if bind_time_match_min < (item['create_time'] - new_weight_data.get('time')).seconds < bind_time_match_max:
                    if bind_weight_match_min < (item['real_weight'] - new_weight_data.get('weight')).seconds < bind_weight_match_max:
                        new_product_data = item

        # 错捆比较报警
        up_item = {}
        for item in deal_product_list:
            item['create_time'] = datetime.datetime.strptime(item['create_time'], "%Y-%m-%d %H:%M:%S")

            if item.get('record_item_id', None) == new_product_data.get('record_item_id', None):
                # 首件
                if item['steel_type_id'] != up_item['steel_type_id'] or item['diameter'] != up_item['diameter'] or item['fixed_length'] != up_item['fixed_length'] and item['gongyi'] != up_item['gongyi']:
                    print(item['steel_type_id'], item['diameter'], item['fixed_length'], item['gongyi'])
                    print(up_item['steel_type_id'], up_item['diameter'], up_item['fixed_length'], up_item['gongyi'])
                    # 首件报警
                    print('首件确认')
                    pass
                else:
                    print(item)
                    print(up_item)
                    _weight_list = deal_rule_dict.get(int(item['diameter']), {}).get(item['fixed_length'], [])
                    print(_weight_list)
                    # 超出范围
                    if _weight_list:
                        min_weight = _weight_list[0] if _weight_list[0] else 0
                        max_weight = _weight_list[1] if _weight_list[1] else 0

                        print(min_weight)
                        print(max_weight)

                        if item.get('real_weight', None) and up_item.get('real_weight', None):
                            diff = item.get('real_weight', None) - up_item.get('real_weight', None)
                            if min_weight < diff < 0:
                                pass
                            elif 0 < diff < max_weight:
                                pass
                            else:
                                # 超出范围报警
                                print('异常报警')
                                pass
                    # 停工太久
                    diff_time = (item.get('create_time', None) - up_item.get('create_time', None)).seconds
                    if stop_work_time_min < diff_time < stop_work_time_max:
                        pass
                    else:
                        print('停工太久报警')
                        pass

            up_item = item

else:
    log_append('没有可操作的opc数据', '', '', '')








































import datetime
import json
from production_manage.models import ProductionRecord, ProductItem, PlanExcelImportSetting


def query_product_item_list_api(_aim_org_id):
    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__gongyi__name', 'plan_item__trade_no_id', 'org_id') \
        .filter(org_id=_aim_org_id, is_active=True).order_by("-create_time")

    if record_query is None:
        return None

    if len(record_query) >= 2:
        record_query = record_query[:2]
    else:
        record_query = record_query[:1]

    result_list = []
    record_query.reverse()

    for record in record_query:

        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'num', 'diameter', 'fixed_length', 'truck_no', 'create_time', 'product_type', 'real_weight') \
            .using(_aim_org_id).filter(is_active=True, org_id=_aim_org_id, roll_no=record['plan_item__roll_no'])

        for item_q in item_query:
            result_dict = {
                'product_record_id': record['id'],
                'item_id': item_q['id'],
                'roll_no': record['plan_item__roll_no'],
                'bind_no': item_q['bind_no'],
                'merge_no': item_q['merge_no'],
                'num': item_q['num'],
                'steel_type_id': record['plan_item__trade_no_id'],
                'diameter': item_q['diameter'],
                'fixed_length': item_q['fixed_length'],
                'create_time': item_q['create_time'],
                'product_type': item_q['product_type'],
                'gongyi': record['plan_item__gongyi__name'],
                'org_id': record['org_id'],
                'real_weight': item_q['real_weight'],
            }
            result_list.append(result_dict)

    return result_list


def query_error_bind_rule_list_api(_aim_org_id):
    flag = 'error_bind_{}'.format(_aim_org_id)
    try:
        setting = PlanExcelImportSetting.objects.get(is_active=True, flag=flag)

        if setting.content:
            result_list = json.loads(setting.content)
        else:
            result_list = []

        return result_list

    except PlanExcelImportSetting.DoesNotExist:
        return []
# now_datetime = datetime.datetime.now()
# opc_start_time = now_datetime - datetime.timedelta(hours=1)
# opc_end_time = now_datetime


opc_start_time = datetime.datetime(2021, 1, 21, 6, 30)
opc_end_time = datetime.datetime(2021, 1, 21, 7, 30)

start_time_str = opc_start_time.strftime("%Y-%m-%d %H:%M:%S")
end_time_str = opc_end_time.strftime("%Y-%m-%d %H:%M:%S")

product_plc_flag_dict = {
    # 高线a
    1: 'gaoxianA.chengpinkun_chengzhong',
    # 高线b
    2: 'gaoxianB.chengpinkun_chengzhong',
    # 二轧
    4: 'er_zha.chengpinkun_chengzhong',
    # 三轧
    5: 'san_zha.chengpinkun_chengzhong',
    # 小棒生产线
    15: 'xiaobang.chengpinkun_chengzhong',
    # 高棒
    19: 'gaobang.chengpinkun_chengzhong',
}

aim_org_id = 15

query_plc_flag_string = product_plc_flag_dict[aim_org_id]

result_opc_list = get_influxdb_data(start_time_str, end_time_str, query_plc_flag_string)

_opc_list = [obj['value'] for obj in result_opc_list]

log_append('_opc_list', _opc_list, '', '')
log_append('opc', result_opc_list, '', '')
# 没有opc数据不操作

if result_opc_list:

    # 获取数据库中捆数
    database_bind_count = 3
    # opc与数据库匹配时间范围
    bind_time_match_min = -600
    bind_time_match_max = 600
    # opc与数据库匹配重量范围
    bind_weight_match_min = -50
    bind_weight_match_max = 50
    # 停工时间范围
    stop_work_time_min = -300
    stop_work_time_max = 300

    start_flag = 0
    up_item = {}
    _list = []
    deal_weight_list = []
    # 处理opc数据 获取opc称重数据
    for item in result_opc_list:

        try:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f").replace(
                microsecond=0)
        except AttributeError:
            pass

        except:
            item['time'] = datetime.datetime.strptime(item['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S").replace(
                microsecond=0)

        if start_flag == 0 and item.get('value', None) != 0 and up_item.get('value', None) == 0:
            # print('开始')
            # print('...')
            start_flag = 1
            _list = []

        if start_flag == 1 and item.get('value', None) != 0:

            _list.append(item)

        if start_flag == 1 and item.get('value', None) == 0 and up_item.get('value', None) != 0:
            # print('结束')
            start_flag = 0
            _dict = {}
            for obj in _list:
                if _dict.get(obj['value'], None):
                    _dict[obj['value']] += 1
                else:
                    _dict[obj['value']] = 1

            weight = 0
            for key, value in _dict.items():
                if value == max(_dict.values()):
                    weight = key

            time_list = []
            for obj in _list:
                if obj.get('value', None) == weight and obj.get('time', None):
                    time_list.append(obj['time'])
            if time_list:
                time = time_list[0]
                # time = time_list[int(len(time_list) / 2)]
                # time = time_list[int(len(time_list) / 2)]

                deal_weight_list.append({
                    'weight': weight,
                    'time': time,
                })
        up_item = item

    log_append('weight', deal_weight_list, '', '')

    # 获取生产信息
    database_product_list = query_product_item_list_api(aim_org_id)

    # log_append('product', database_product_list, aim_org_id, '')

    if database_product_list:

        deal_product_list = []
        # 处理最近指定 捆数 数据
        if len(database_product_list) >= database_bind_count:
            deal_product_list = database_product_list[-database_bind_count:]
        # 查看 数据库处理数据
        for item in deal_product_list:
            log_append('product', database_product_list, aim_org_id, '')

        database_rule_list = query_error_bind_rule_list_api(aim_org_id)
        deal_rule_dict = {}
        # 处理规则
        for item in database_rule_list:
            deal_rule_dict.setdefault(item['diameter'], {}).setdefault(item['dingchi'], [item['weight_max'], item['weight_min']])
        # 查看 数据库处理规则数据
        log_append('rule', deal_rule_dict, '', '')

