#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: acquire.py
# Email:
# Author: 唐政
from api_product import process_lis
from api_product import process_params
from api_product import process_str
from api_product import process_param
from api_product import process_foreignkey
from api_product import process_foreign_list
from api_product import process_foreignget
from api_product import process_foreigntry
from api_product import process_json
from api_product import process_if
from api_product import process_query
from api_product import process_check
from api_product import RAW_MATERIAL_FACTORY_MODEL
from api_product import api
import datetime

app_name = "custom_monitor"
model_str = "常规监控脚本日志"
user = "唐政"
var_dot = '"""'
now = datetime.datetime.now().date()
do_thing = """by:{} at:{}""".format(user, now)

# 获取原料
model_list = process_lis(RAW_MATERIAL_FACTORY_MODEL)


# # 获取二次加工
# model_upper, para_list, var_list = process_params(model_list)
#
# model_low = model_upper.lower()
# model_id = model_low + '_id'
#
# # 获取外键dict列表
# foreign_dict_list = process_foreignkey(para_list)
#
# # 获取外键
# foreign_str = process_foreign_list(foreign_dict_list)
# # 外键get
# foreign_get_str = process_foreignget(foreign_dict_list)
# # 外键捕获
# foreign_except_str = process_foreigntry(foreign_dict_list)
#
#
# # 获取 参数var, var, var...
# var_str_create = process_str(para_list, model_id)
# # 获取 参数var, var, var... update
# var_str_update = process_str(para_list, model_id, 1)
# # 获取 参数var, var, var... query
# var_str_query = process_str(para_list, model_id, 2)
#
#
# # 获取函数解释 创建
# var_param_create = process_param(para_list, model_id, model_str)
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
