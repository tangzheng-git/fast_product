#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: __init__.py.py
# Email:
# Author: 唐政


RAW_MATERIAL_FACTORY_MODEL = './material_model.txt'

ID_DICT = {
        "steel_type_id": "r,zlsmart.SteelType__pk",
        "zl_id": "r,zlsmart.ZLInfo__pk",
        "tsg_id": "r,zlsmart.TSGInfo__pk",
        "lt_id": "r,zlsmart.LTInfo__pk",
        "template_id": "r,zlsmart.ExcelTemplateVersion__pk",

}

PARAM_DICT = {
        "org_id": "组织id",
        "is_active": "状态",
        "page_index": "页号",
        "page_size": "页大小",
}

from api_product.dosing import process_lis
from api_product.dosing import process_params
from api_product.dosing import process_str
from api_product.dosing import process_param
from api_product.dosing import process_foreignkey
from api_product.dosing import process_foreign_list
from api_product.dosing import process_foreignget
from api_product.dosing import process_foreigntry
from api_product.dosing import process_json
from api_product.dosing import process_if
from api_product.dosing import process_query
from api_product.dosing import process_check
from api_product.material_api import api

