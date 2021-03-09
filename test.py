#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/17
# file: test.py
# Email:
# Author: 唐政


# import re
#
# item = "arrange_shift_id = models.IntegerField(default=0, verbose_name=u'生产班次')"
# default = None
# try:
#     default = re.match(r'.*?default=(.*?),', item).group(1)
# except AttributeError:
#     pass
# print(default)

# http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

# sample_name = '123456-4'
# #
# # if sample_name.find('-') != -1:
# #     try:
# #         cast = sample_name.split('-')[1]
# #         cast = int(cast)
# #         if cast in [1, 2, 3, 4]:
# #             print(cast)
# #             # data.cast = cast
# #     except:
# #         from util.tools import send_sentry
# #         send_sentry(u"{}:{}".format("cast", "la_data cast write error"))

# lis = "日期	时间	钢种	炉次	样号	C	Si	Mn	P	S	Cr	Ni	Ti	B	V	Al	Nb	Ceq	YL1	YL2"
# lis = lis.split('\t')
# for i, value in enumerate(lis):
#
#     print('"{}": ana.get("{}"),'.format(value, value))
# for i, value in enumerate(lis):
#
#     print('"{}": row["{}"],'.format(value, i))

# for i, value in enumerate(lis):
#     "ana['']"
#     print('ana["{}"],'.format(value, i))

# import re
#
# log = re.match(r'([\w]+?):(.*?)≤', 'Si:0.000000≤0.300')
# print('{}:{}'.format(log.group(1), log.group(2)))

# lis = [1, 2, 3, 4, 5, 6]
# li = [[5, 2], [6, 2], [4, 2], [3, 2], [2, 2], [1, 2]]
#
# li.sort(key=lambda x: x[0])
# print(list([1, 2]))
#

# 169193 <class 'str'> 1 <class 'str'> False

# print(list(map(lambda x, y: x + y[1], lis, li)))

# import chardet
#
#
# def get_encoding(filename):
#     """
#     返回文件编码格式
#     """
#     with open(filename, 'rb') as f:
#         return chardet.detect(f.read())['encoding']
#
#
# print(get_encoding('test.py'))

# import re
# pattern_api = re.compile(r"api\.(.*?)\.(.*?)\(")
# line = '        //         api.device.query_specification_by_org_and_id_zhaxian({  //'
#
# result_api = pattern_api.findall(line)
# print(line.find("//"))
# print(line.find(result_api[0][0]))

# class ProductItem():
#     BIND_DEAL = -1
#     BIND_NORMAL = 0
#     BIND_CONFIRMED = 1
#     BIND_FIRST_CONFIRMED = 2
#     BIND_ABNORMAL = 3
#     BIND_STATUS_CHOICE = (
#         (BIND_DEAL, u'待处理'),
#         (BIND_NORMAL, u'正常'),
#         (BIND_CONFIRMED, u'异常待确认'),
#         (BIND_FIRST_CONFIRMED, u'首件确认'),
#         (BIND_ABNORMAL, u'支数异常'),
#     )
#
#
# print(True, u'错误捆支数状态 < ProductItem#{} > need in {}'.format(1, [tup[0] for tup in ProductItem.BIND_STATUS_CHOICE]))
# import json
# state_api_json = json.dumps([])
#
# state_api_json = json.loads(state_api_json)
#
# if state_api_json is not None:
#     print(1)
#     for api_dict in state_api_json:
#         if api_dict['state'] != 1:
#             pass

# s = 'Level_CHOICES'
#
# print(s.upper())

# lhwd_opc_dict_list = [8, 9, 10, 7, 6, 5, 6, 4, 3, 1, 2]
# # lhwd_opc_dict_list = [temp_opc_dict for temp_opc_dict in lhwd_opc_dict_list if
# #                       1450 <= temp_opc_dict['opc_value'] <= 1650]
# lis = []
# all_lis = []
# for pre, nex in zip(lhwd_opc_dict_list, lhwd_opc_dict_list[1:]):
#     lis.append(pre)
#     if pre < nex:
#         all_lis.append([lis, max(lis) - min(lis), len(lis)])
#         lis = []
# else:
#     lis.append(lhwd_opc_dict_list[-1])
#     all_lis.append([lis, max(lis) - min(lis), len(lis)])
#
# print(all_lis)
#
# effective_lhwd_opc_dict_list = all_lis[0][0]
# for item in all_lis:
#     if item[1] > 50:
#         continue
#     if item[2] < 2:
#         continue
#     effective_lhwd_opc_dict_list = item[0]
#
# print(effective_lhwd_opc_dict_list)

# lhwd_opc_dict_list = [
#     {'opc_value': 1650},
#     {'opc_value': 1640},
#     {'opc_value': 1640},
#     {'opc_value': 1630},
#     {'opc_value': 1620},
#     {'opc_value': 1610},
#     {'opc_value': 1610},
#     {'opc_value': 1660},
#     {'opc_value': 1550}
# ]
# # lhwd_opc_dict_list = [temp_opc_dict for temp_opc_dict in lhwd_opc_dict_list if
# #                       1450 <= temp_opc_dict['opc_value'] <= 1650]
#
# effective_lhwd_opc_dict_list = []
#
# for temp_opc_dict in lhwd_opc_dict_list:
#     if 1550 > temp_opc_dict['opc_value'] or temp_opc_dict['opc_value'] > 1650:
#         continue
#     if not effective_lhwd_opc_dict_list:
#         effective_lhwd_opc_dict_list.append(temp_opc_dict)
#     else:
#         if temp_opc_dict['opc_value'] <= effective_lhwd_opc_dict_list[-1]['opc_value']:
#             effective_lhwd_opc_dict_list.append(temp_opc_dict)
#
# print(effective_lhwd_opc_dict_list)

# def get_weight_time_list(weight_opc_dict_list, unit_factor):
#     # 获得辅料加料信息
#     # 将负值设置成0
#     for weight_opc_dict in weight_opc_dict_list:
#         if weight_opc_dict["opc_value"] < 0:
#             weight_opc_dict["opc_value"] = 0
#
#     lis = []
#     for pre_weight, next_weight in zip(weight_opc_dict_list, weight_opc_dict_list[1:]):
#         if pre_weight['opc_value'] <= next_weight['opc_value']:
#             dic = {
#                 "time": str(next_weight['opc_time'])[:19],
#                 "weight": (next_weight['opc_value'] - pre_weight['opc_value']) * unit_factor,
#             }
#             if dic['weight']:
#                 lis.append(dic)
#         else:
#             if next_weight['opc_value']:
#                 dic = {
#                     "time": str(next_weight['opc_time'])[:19],
#                     "weight": next_weight['opc_value'] * unit_factor,
#                 }
#                 if dic['weight']:
#                     lis.append(dic)
#     return lis
#
#
# weight_opc_dict_list = [
#   {
#     "opc_time": "2021-03-04 08:21:36.440779",
#     "opc_value": 6982.060546875,
#     "pre_data": True
#   },
#   {
#     "opc_time": "2021-03-04 08:35:13.949247",
#     "opc_value": 6982.060546875
#   },
#   {
#     "opc_time": "2021-03-04 08:37:51.942271",
#     "opc_value": 7364.0048828125
#   },
#   {
#     "opc_time": "2021-03-04 08:38:41.447529",
#     "opc_value": 7769.09765625
#   },
#   {
#     "opc_time": "2021-03-04 08:39:40.578816",
#     "opc_value": 8158.27587890625
#   },
#   {
#     "opc_time": "2021-03-04 08:40:17.129590",
#     "opc_value": 8158.27587890625
#   },
#   {
#     "opc_time": "2021-03-04 08:47:37.261539",
#     "opc_value": 8559.0283203125
#   },
#   {
#     "opc_time": "2021-03-04 08:48:57.255622",
#     "opc_value": 8969.908203125
#   },
#   {
#     "opc_time": "2021-03-04 08:50:00.747589",
#     "opc_value": 9383.681640625
#   },
#   {
#     "opc_time": "2021-03-04 08:51:28.865484",
#     "opc_value": 9787.3271484375,
#     "pre_data": True
#   }
# ]
# unit_factor = 1
# bai_hui_1 = get_weight_time_list(weight_opc_dict_list, unit_factor)
#
# for bai_hui in bai_hui_1:
#     print(bai_hui)

import datetime
import json
from comparison import result
from reservation import reservation
from formate_datetime import formate_datetime

YANG_QI_YONG_LIANG = reservation['YANG_QI_YONG_LIANG']
ZHONG_DIAN_WEN_DU = reservation['ZHONG_DIAN_WEN_DU']

lu_dict = result["lu_list"][0]


# 获取某段时间内的温度opc（用来辅助判定是否存在补吹测温）
def get_temp_opc_dict_list_by_range(odl, start_datetime, end_datetime=None):
    if end_datetime:
        return [od for od in odl if start_datetime <= formate_datetime(od["opc_time"]) <= end_datetime]
    else:
        return [od for od in odl if start_datetime <= formate_datetime(od["opc_time"])]


# 给定 氧气列表、温度列表，计算吹氧量、吹氧时长等
def get_supply_o_time_dict_and_end_datetime(o2_l, t_l):
    temp = 0
    temp_datetime = 0
    for temp_opc_dict in t_l:
        if temp_opc_dict['opc_value'] > temp:
            temp = temp_opc_dict['opc_value']
            temp_datetime = temp_opc_dict['opc_time']

    first_o2_point = o2_l[0]
    last_o2_point = o2_l[-1]
    # 氧量小于50的数据，计量差值时，该数据按0计算
    if first_o2_point['opc_value'] <= 50:
        o2_usage = last_o2_point['opc_value']
    else:
        o2_usage = last_o2_point['opc_value'] - first_o2_point['opc_value']

    sustain_time = 0
    if len(o2_l):
        for pre_o2_usage_dict, next_o2_usage_dict in zip(o2_l, o2_l[1:]):
            if next_o2_usage_dict['opc_time'] - pre_o2_usage_dict['opc_time'] < datetime.timedelta(seconds=30):
                sustain_time += (next_o2_usage_dict['opc_time'] - pre_o2_usage_dict['opc_time']).total_seconds()


    return {
               "supply_o_start_time": str(first_o2_point['opc_time'])[:19],
               "supply_o_end_time": str(last_o2_point['opc_time'])[:19],
               "sustain_time": sustain_time,
               "temp": temp,
               "temp_time": str(temp_datetime)[:19],
               "o2_usage": o2_usage
           }, last_o2_point['opc_time']


o2_opc_dict_list = lu_dict.get(YANG_QI_YONG_LIANG['flag'], [])
temp_opc_dict_list = lu_dict.get(ZHONG_DIAN_WEN_DU['flag'], [])
# 过滤无效值
effective_temp_opc_dict_list = [temp_opc_dict for temp_opc_dict in temp_opc_dict_list if
                                1550 <= temp_opc_dict['opc_value'] <= 1700]


supply_o_time_list = []
o2_usage_list = []
o2_end_datetime = None  # 结束供氧时间
# 序列是增加的
for i in range(len(o2_opc_dict_list)):
    if i == 0:
        current_o2_opc_dict = o2_opc_dict_list[0]
        # 第一个为value为0 是置零点无意义，忽略
        if current_o2_opc_dict['opc_value'] == 0:
            continue
        o2_usage_list.append(current_o2_opc_dict)
    else:
        previous_o2_opc_dict = o2_opc_dict_list[i - 1]
        current_o2_opc_dict = o2_opc_dict_list[i]

        previous_o2_opc_dict['opc_time'] = formate_datetime(previous_o2_opc_dict['opc_time'])
        current_o2_opc_dict['opc_time'] = formate_datetime(current_o2_opc_dict['opc_time'])

        # 先忽略补吹
        if current_o2_opc_dict['opc_time'] - previous_o2_opc_dict['opc_time'] < datetime.timedelta(seconds=30):
            # 两氧气点之间超过30s
            o2_usage_list.append(current_o2_opc_dict)
        else:
            # 检查两点之间，是否存在测温点；存在则有补吹，不存在不处理
            temp_opc_l = get_temp_opc_dict_list_by_range(effective_temp_opc_dict_list,
                                                         previous_o2_opc_dict['opc_time'],
                                                         current_o2_opc_dict['opc_time'])

            if temp_opc_l:
                if len(o2_usage_list) >= 2:
                    supply_o_time_dict, o2_end_datetime = get_supply_o_time_dict_and_end_datetime(o2_usage_list,
                                                                                                  temp_opc_l)
                    supply_o_time_list.append(supply_o_time_dict)
                # 重置o2_usage_list
                o2_usage_list = [current_o2_opc_dict]
            else:
                o2_usage_list.append(current_o2_opc_dict)


# 如果o2_usage_list 还有剩余氧气数据（转炉周期最后一段吹氧时间，过滤掉其中的零值点）
o2_usage_list = [d for d in o2_usage_list if d['opc_value'] > 0]
if len(o2_usage_list) >= 2:
    temp_opc_l = get_temp_opc_dict_list_by_range(effective_temp_opc_dict_list, o2_usage_list[-1]['opc_time'])
    supply_o_time_dict, o2_end_datetime = get_supply_o_time_dict_and_end_datetime(o2_usage_list, temp_opc_l)
    supply_o_time_list.append(supply_o_time_dict)


supply_o_time_json = json.dumps(supply_o_time_list)
for supply_o_time in supply_o_time_list:
    print(supply_o_time)