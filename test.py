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


