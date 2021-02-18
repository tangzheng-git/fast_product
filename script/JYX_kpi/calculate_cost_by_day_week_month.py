#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/22
# file: calculate_cost_by_day_week_month.py
# Email:
# Author: 唐政

import datetime
import json
from dateutil import relativedelta


def get_cost_data_by_ids_api(cost_node_ids, start_datetime, end_datetime):
    error_str = ''
    cost_node_ids_str = json.dumps(cost_node_ids)
    query_start_time_str = start_datetime.replace(second=0, minute=0, hour=0).strftime("%Y-%m-%d %H:%M:%S")
    query_end_time_str = end_datetime.replace(second=0, minute=0, hour=0).strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "org_id": 1,
        "cost_node_ids": cost_node_ids_str,
        "start_datetime": query_start_time_str,
        "end_datetime": query_end_time_str,
    }

    # log_append('query interval', start_datetime.date(), end_datetime.date(), '')
    #
    # log_append('cost_node_ids', cost_node_ids_str, '', '')

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="kpi/api/get_cost_data_by_ids_api",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"获取成本 产量:get_cost_data_by_ids_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict['result'], error_str


def save_kpi_data_list_by_date_api(kpi_data_list, data_date):
    error_str = ''
    kpi_data_json = json.dumps(kpi_data_list)
    time_str = data_date.strftime("%Y-%m-%d %H:%M:%S")

    data_param = {
        "kpi_data_list": kpi_data_json,
        "data_date": time_str
    }

    # log_append('save data', kpi_data_list, 'data_date', time_str)

    code, error, result_dict = \
        get_result_by_remote_consul_server(service_name="jyx_kpi",
                                           url="kpi/api/save_kpi_data_list_by_date_api",
                                           data_parms=data_param, timeout=180, is_log=False)

    if code != 0:
        error_str = u"保存成本 产量:save_kpi_data_list_by_date_api ERROR code-{} error-{}".format(code, error)
        return result_dict, error_str

    return result_dict, error_str


def diff_value(money_list, num_list, last_money_list, last_num_list):
    if int(sum(num_list)) == 0:
        now = 0
    else:
        now = sum(money_list) / sum(num_list)
    if int(sum(last_num_list)) == 0:
        last = 0
    else:
        last = sum(last_money_list) / sum(last_num_list)
    if int(now) == 0 or int(last) == 0:
        result = 0
    else:
        result = now - last

    return result


def date_range(beginDate, endDate):
    date_list = []
    date = beginDate.date()
    endDate = endDate.date()

    while date <= endDate:
        date_list.append(date.strftime("%Y-%m-%d"))
        date = date + datetime.timedelta(days=1)

    return date_list


def template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id):

    cost_node_id_list = [cost_id, yield_id]
    now_month_yes = now_datetime - datetime.timedelta(days=1)
    now_month_1 = now_month_yes.replace(day=1)
    front_month_1 = now_month_1 - relativedelta.relativedelta(months=1)

    month_sub = (now_month_yes - now_month_1).days + 1
    week_sub = now_month_yes.isoweekday()
    last_week_sub = now_month_yes.isoweekday() + 7

    result, error_get = get_cost_data_by_ids_api(cost_node_id_list, front_month_1, now_month_yes)

    cost_dict = {date: 0 for date in date_range(front_month_1, now_month_yes)}
    yield_dict = {date: 0 for date in date_range(front_month_1, now_month_yes)}

    if result is not None:
        cost_dict_query = {key: value['day_money'] for key, value in result[str(cost_id)].items()}

        yield_dict_query = {key: value['day_num'] for key, value in result[str(yield_id)].items()}

        for data, value in cost_dict_query.items():
            cost_dict[data] += value

        for data, value in yield_dict_query.items():
            yield_dict[data] += value

        # 成本
        cost_list = [[key, value] for key, value in cost_dict.items()]
        # 产量
        yield_list = [[key, value] for key, value in yield_dict.items()]

        cost_list.sort(key=lambda lis: lis[0])
        yield_list.sort(key=lambda lis: lis[0])

        # log_append('yes start', 'yes end', 'bef start', 'bef end')
        # log_append('{}'.format(cost_list[-1:][0][0]),
        #            '{}'.format(yield_list[-1:][-1][0]),
        #            '{}'.format(cost_list[-2:-1][0][0]),
        #            '{}'.format(yield_list[-2:-1][-1][0]))
        #
        # log_append('week start', 'week end', 'up start', 'up end')
        # log_append('{}'.format(cost_list[-week_sub:][0][0]),
        #            '{}'.format(cost_list[-week_sub:][-1][0]),
        #            '{}'.format(yield_list[-last_week_sub:-week_sub][0][0]),
        #            '{}'.format(yield_list[-last_week_sub:-week_sub][-1][0]))
        #
        # log_append('month start', 'month end', 'up start', 'up end')
        # log_append('{}'.format(yield_list[-month_sub:][0][0]),
        #            '{}'.format(yield_list[-month_sub:][-1][0]),
        #            '{}'.format(cost_list[:-month_sub][0][0]),
        #            '{}'.format(cost_list[:-month_sub][-1][0]))
        #
        # log_append('result cost', cost_list, 'result yield', yield_list)

        cost_list = [item[1] for item in cost_list]
        yield_list = [item[1] for item in yield_list]

        day_diff_value = diff_value(cost_list[-1:],
                                    yield_list[-1:],
                                    cost_list[-2:-1],
                                    yield_list[-2:-1])

        week_diff_value = diff_value(cost_list[-week_sub:],
                                     yield_list[-week_sub:],
                                     cost_list[-last_week_sub:-week_sub],
                                     yield_list[-last_week_sub:-week_sub])

        month_diff_value = diff_value(cost_list[-month_sub:],
                                      yield_list[-month_sub:],
                                      cost_list[:-month_sub],
                                      yield_list[:-month_sub])

        # log_append('result_diff', day_diff_value, week_diff_value, month_diff_value)

        data_list = [
            {'kpi_index_id': day_diff_id,
             'total_data': 0,
             'daily_data': day_diff_value,
             },
            {'kpi_index_id': week_diff_id,
             'total_data': 0,
             'daily_data': week_diff_value,
             },
            {'kpi_index_id': month_diff_id,
             'total_data': 0,
             'daily_data': month_diff_value,
             },
        ]
        data_datetime = now_month_yes

        save_kpi_data_list_by_date_api(data_list, data_datetime)


def cost_yield_deal(now_datetime, day_diff_id, week_diff_id, month_diff_id):

    now_month_yes = now_datetime - datetime.timedelta(days=1)
    now_month_1 = now_month_yes.replace(day=1)
    front_month_1 = now_month_1 - relativedelta.relativedelta(months=1)
    month_sub = (now_month_yes - now_month_1).days + 1
    week_sub = now_month_yes.isoweekday()
    last_week_sub = now_month_yes.isoweekday() + 7

    cost_node_id_list = [3613, 3615]
    result_1, error_get = get_cost_data_by_ids_api(cost_node_id_list, front_month_1, now_month_yes)
    cost_node_id_list = [3609, 3611]
    result_2, error_get = get_cost_data_by_ids_api(cost_node_id_list, front_month_1, now_month_yes)
    cost_node_id_list = [3605, 3607]
    result_3, error_get = get_cost_data_by_ids_api(cost_node_id_list, front_month_1, now_month_yes)

    cost_dict = {date: 0 for date in date_range(front_month_1, now_month_yes)}
    yield_dict = {date: 0 for date in date_range(front_month_1, now_month_yes)}

    if result_1 is not None:

        # 成本
        cost_dict_1 = {key: value['day_money'] for key, value in result_1['3613'].items()}

        # 产量
        yield_dict_1 = {key: value['day_num'] for key, value in result_1['3615'].items()}

        for data, value in cost_dict_1.items():
            cost_dict[data] += value

        for data, value in yield_dict_1.items():
            yield_dict[data] += value

    if result_2 is not None:

        # 成本
        cost_dict_2 = {key: value['day_money'] for key, value in result_2['3609'].items()}

        # 产量
        yield_dict_2 = {key: value['day_num'] for key, value in result_2['3611'].items()}

        for data, value in cost_dict_2.items():
            cost_dict[data] += value

        for data, value in yield_dict_2.items():
            yield_dict[data] += value

    if result_3 is not None:

        # 成本
        cost_dict_3 = {key: value['day_money'] for key, value in result_3['3605'].items()}

        # 产量
        yield_dict_3 = {key: value['day_num'] for key, value in result_3['3607'].items()}

        for data, value in cost_dict_3.items():
            cost_dict[data] += value

        for data, value in yield_dict_3.items():
            yield_dict[data] += value

    # 成本
    cost_list = [[key, value] for key, value in cost_dict.items()]
    # 产量
    yield_list = [[key, value] for key, value in yield_dict.items()]

    cost_list.sort(key=lambda lis: lis[0])
    yield_list.sort(key=lambda lis: lis[0])

    cost_list = [item[1] for item in cost_list]
    yield_list = [item[1] for item in yield_list]

    if sum(cost_list) != 0 and sum(yield_list) != 0:

        day_diff_value = diff_value(cost_list[-1:],
                                    yield_list[-1:],
                                    cost_list[-2:-1],
                                    yield_list[-2:-1])

        week_diff_value = diff_value(cost_list[-week_sub:],
                                     yield_list[-week_sub:],
                                     cost_list[-last_week_sub:-week_sub],
                                     yield_list[-last_week_sub:-week_sub])

        month_diff_value = diff_value(cost_list[-month_sub:],
                                      yield_list[-month_sub:],
                                      cost_list[:-month_sub],
                                      yield_list[:-month_sub])

        data_list = [
            {'kpi_index_id': day_diff_id,
             'total_data': 0,
             'daily_data': day_diff_value,
             },
            {'kpi_index_id': week_diff_id,
             'total_data': 0,
             'daily_data': week_diff_value,
             },
            {'kpi_index_id': month_diff_id,
             'total_data': 0,
             'daily_data': month_diff_value,
             },
        ]
        data_datetime = now_month_yes

        save_kpi_data_list_by_date_api(data_list, data_datetime)


now_datetime = datetime.datetime.now()

# 球团
cost_id = 2421
yield_id = 2422
day_diff_id = 5697
week_diff_id = 5699
month_diff_id = 5701

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 球团一期
cost_id = 737
yield_id = 738
day_diff_id = 5709
week_diff_id = 5711
month_diff_id = 5713

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 球团二期
cost_id = 1467
yield_id = 1469
day_diff_id = 5715
week_diff_id = 5717
month_diff_id = 5719

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 烧结id
cost_id = 2423
yield_id = 2424
day_diff_id = 5703
week_diff_id = 5707
month_diff_id = 5705

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 烧结一期id
cost_id = 815
yield_id = 816
day_diff_id = 5721
week_diff_id = 5723
month_diff_id = 5725

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 烧结二期id
cost_id = 1474
yield_id = 1475
day_diff_id = 5727
week_diff_id = 5729
month_diff_id = 5731

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼铁id
cost_id = 2425
yield_id = 2426
day_diff_id = 5745
week_diff_id = 5747
month_diff_id = 5749

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼铁一期id
cost_id = 1478
yield_id = 1479
day_diff_id = 5751
week_diff_id = 5753
month_diff_id = 5755

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼铁二期id
cost_id = 1483
yield_id = 1484
day_diff_id = 5757
week_diff_id = 5759
month_diff_id = 5761

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢
cost_id = 3493
yield_id = 3494
day_diff_id = 5771
week_diff_id = 5773
month_diff_id = 5775

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢Q195
cost_id = 1488
yield_id = 1489
day_diff_id = 5777
week_diff_id = 5789
month_diff_id = 5791

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢Q235
cost_id = 1493
yield_id = 1494
day_diff_id = 5779
week_diff_id = 5793
month_diff_id = 5795

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢HPB300
cost_id = 1498
yield_id = 1499
day_diff_id = 5781
week_diff_id = 5797
month_diff_id = 5799

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢HRB400
cost_id = 1508
yield_id = 1509
day_diff_id = 5783
week_diff_id = 5801
month_diff_id = 5803

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢Q235B
cost_id = 1503
yield_id = 1504
day_diff_id = 5785
week_diff_id = 5805
month_diff_id = 5807

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 炼钢Q195B
cost_id = 1613
yield_id = 1614
day_diff_id = 5787
week_diff_id = 5809
month_diff_id = 5811

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 板带
cost_id = 3617
yield_id = 3619
day_diff_id = 5813
week_diff_id = 5815
month_diff_id = 5817

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 板带Q195
cost_id = 2662
yield_id = 2663
day_diff_id = 5819
week_diff_id = 5821
month_diff_id = 5823
template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 板带Q235
cost_id = 2675
yield_id = 2676
day_diff_id = 5825
week_diff_id = 5827
month_diff_id = 5829

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 轧钢一
cost_id = 3613
yield_id = 3615
day_diff_id = 5837
week_diff_id = 5839
month_diff_id = 5841


template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 轧钢二
cost_id = 3609
yield_id = 3611
day_diff_id = 5843
week_diff_id = 5845
month_diff_id = 5847


template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 轧钢三
cost_id = 3605
yield_id = 3607
day_diff_id = 5849
week_diff_id = 5851
month_diff_id = 5853

template_cost_yield_deal(now_datetime, cost_id, yield_id, day_diff_id, week_diff_id, month_diff_id)

# 轧钢
day_diff_id = 5831
week_diff_id = 5833
month_diff_id = 5835
cost_yield_deal(now_datetime, day_diff_id, week_diff_id, month_diff_id)
