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
from ApiProduct import process_json
from ApiProduct import process_if
from ApiProduct import process_query
from ApiProduct import process_check
from ApiProduct import RAW_MATERIAL_FACTORY_MODEL
from ApiProduct import api
import datetime

app_name = "custom_monitor"
model_str = "常规监控脚本日志"
user = "唐政"
var_dot = '"""'
now = datetime.datetime.now().date()
do_thing = """by:{} at:{}""".format(user, now)

# 获取原料
model_list = get_model_list(RAW_MATERIAL_FACTORY_MODEL)

model_info_dict = get_model_info_dict(model_list)

print()
for item in model_info_dict.items():
    print(item)

field_info_dict = get_field_info_dict(model_info_dict)

print()
for item in field_info_dict.items():
    print(item)


foreign_info_dict = get_foreign_info_dict(model_info_dict['model_params'])

# for item in foreign_info_dict.items():
#     print(item[1])

var_str_dict = get_var_info_dict(model_info_dict)

print()
for item in var_str_dict.items():
    print(item)

# 获取函数解释 创建
param_str_dict = get_param_info_dict(field_info_dict, var_str_dict)

print()
for item in param_str_dict.items():
    print(item[1])

# # 获取函数解释 修改
# var_param_update = process_param(para_list, model_id, model_str, 1)
# # 获取函数解释 查询
# var_param_query = process_param(para_list, model_id, model_str, 2)
#
# # 获取{"var":""}
# var_json = process_json(var_list)
#
# # 获取if {} is not None
# var_if = process_if(para_list)
# # 获取查询
# var_if_query = process_query(para_list)
#
# # 验证参数 var=("ver", "")
# var_check_create = process_check(para_list, model_upper, model_low, model_str, app_name, model_upper)
# # 验证参数 var=("ver", "") update
# var_check_update = process_check(para_list, model_upper, model_low, model_str, app_name, model_upper, 1)
# # 验证参数 var=("ver", "") query
# var_check_query = process_check(para_list, model_upper, model_low, model_str, app_name, model_upper, 2)
#
#
# para_dict = {
#     "app_name": app_name,
#     "user": user,
#     "now": now,
#     "now_year": now.year,
#     "now_month": now.month,
#     "now_day": now.day,
#     "do_thing": do_thing,
#     "model_str": model_str,
#     "model_upper": model_upper,
#     "model_low": model_low,
#     "model_id": model_id,
#     "foreign_get_str": foreign_get_str,
#     "foreign_str": foreign_str,
#     "foreign_except_str": foreign_except_str,
#     "var_str_create": var_str_create,
#     "var_str_update": var_str_update,
#     "var_str_query": var_str_query,
#     "var_param_create": var_param_create,
#     "var_param_update": var_param_update,
#     "var_param_query": var_param_query,
#     "var_dot": var_dot,
#     "var_if": var_if,
#     "var_if_query": var_if_query,
#     "var_check_create": var_check_create,
#     "var_check_query": var_check_query,
#     "var_check_update": var_check_update,
# }
#
#
#
# with open('../views_{}.py'.format(para_dict['model_low']), 'w+', encoding='UTF-8') as f:
#     f.write(api.format(**para_dict))
