#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: acquire.py
# Email:
# Author: 唐政
from ApiProduct import get_model_list
from ApiProduct import get_model_info_dict
from ApiProduct import get_var_info_dict
from ApiProduct import get_param_info_dict
from ApiProduct import get_foreign_info_dict
from ApiProduct import get_field_info_dict
from ApiProduct import get_var_if_dict
from ApiProduct import get_param_check_dict
from ApiProduct import RAW_MATERIAL_FACTORY_MODEL
from ApiProduct import api
import datetime

DEBUG = True
app_name = ""
user = "唐政"
var_dot = '"""'
now = datetime.datetime.now().date()
do_thing = """by:{} at:{}""".format(user, now)

# 获取原料
model_list = get_model_list(RAW_MATERIAL_FACTORY_MODEL)
# model信息
model_info_dict = get_model_info_dict(model_list)
if DEBUG:
    print()
    for item in model_info_dict.items():
        print(item)

# 字段对应名称
field_info_dict = get_field_info_dict(model_info_dict)
if DEBUG:
    print()
    for item in field_info_dict.items():
        print(item)

# 外键相关处理
foreign_info_dict = get_foreign_info_dict(model_info_dict['model_params'])
if DEBUG:
    print()
    for item in foreign_info_dict.items():
        print(item)

# 参数信息dict
var_str_dict = get_var_info_dict(model_info_dict)
if DEBUG:
    print()
    for item in var_str_dict.items():
        print(item)

# 注释信息dict
param_str_dict = get_param_info_dict(field_info_dict, var_str_dict)
if DEBUG:
    print()
    for item in param_str_dict.items():
        print(item)

# if信息dict
var_if_dict = get_var_if_dict(model_info_dict)
if DEBUG:
    print()
    for item in var_if_dict.items():
        print(item)

# 参数校验dict
param_check_dict = get_param_check_dict(model_info_dict, field_info_dict, var_str_dict)
if DEBUG:
    print()
    for item in param_check_dict.items():
        print(item)

para_dict = {
    "app_name": app_name,
    "user": user,
    "now": now,
    "now_year": now.year,
    "now_month": now.month,
    "now_day": now.day,
    "do_thing": do_thing,
    "model_str": model_info_dict['model_chinese_str'],
    "model_upper_str": model_info_dict['model_upper_str'],
    "model_lower_str": model_info_dict['model_lower_str'],
    "model_id_str": model_info_dict['model_id_str'],
    "foreign_get_str": foreign_info_dict['foreign_get_str'],
    "foreign_dot_str": foreign_info_dict['foreign_dot_str'],
    "foreign_try_str": foreign_info_dict['foreign_try_str'],
    "var_create_str": var_str_dict['var_create_str'],
    "var_update_str": var_str_dict['var_update_str'],
    "var_query_str": var_str_dict['var_query_str'],
    "param_create_str": param_str_dict['param_create_str'],
    "param_update_str": param_str_dict['param_update_str'],
    "param_query_str": param_str_dict['param_query_str'],
    "var_dot": var_dot,
    "var_if_common_str": var_if_dict['var_if_common_str'],
    "var_if_query_str": var_if_dict['var_if_query_str'],
    "var_check_create": param_check_dict['check_create_str'],
    "var_check_update": param_check_dict['check_update_str'],
    "var_check_query": param_check_dict['check_query_str'],
}


with open('../views_{}.py'.format(para_dict['model_lower_str']), 'w+', encoding='UTF-8') as f:
    f.write(api.format(**para_dict))


