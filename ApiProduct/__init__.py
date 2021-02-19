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

from ApiProduct.dosing import get_model_list
from ApiProduct.dosing import get_model_info_dict
from ApiProduct.dosing import get_var_info_dict
from ApiProduct.dosing import get_param_info_dict
from ApiProduct.dosing import get_foreign_info_dict
from ApiProduct.dosing import get_field_info_dict
from ApiProduct.dosing import process_json
from ApiProduct.dosing import process_if
from ApiProduct.dosing import process_query
from ApiProduct.dosing import process_check
from ApiProduct.material_api import api

