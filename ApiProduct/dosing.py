#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: dosing.py
# Email:
# Author: 唐政
import re

from api_product import PARAM_DICT


def deal_list_to_str(_list, _start,  _middle, _end):
    return _start + _middle.join(_list) + _end


def deal_param_func(var_list, params_dict, _start, _end):
    result_list = []
    if _start is not None:
        _start.format()
        result_list.extend(_start)
    for var_str in var_list:
        param_create_str = """    :param {}: {}""".format(var_str, params_dict.get(var_str))
        result_list.append(param_create_str)
    if _end is not None:
        result_list.extend(_end)
    return result_list


def get_model_list(RAW_MATERIAL_FACTORY_MODEL):
    """
    从文件从获取model
    :return:
    """
    with open(RAW_MATERIAL_FACTORY_MODEL, 'r', encoding='UTF-8') as f:
        model_txt = f.read()
    model_list = [line.strip() for line in model_txt.split('\n')]

    return model_list


def get_model_info_dict(model_list):
    """
    生成字段字典
    :param model_list:
    :return:
    """
    model_info_dict = {}

    chinese_model_flag = False
    for line in model_list:
        if 'class' in line:
            model_info_dict['model_upper_str'] = line.replace('class ', '').replace('(BaseModel):', '')
            model_info_dict['model_lower_str'] = model_info_dict['model_upper_str'].lower()
            model_info_dict['model_id_str'] = model_info_dict['model_lower_str'] + '_id'
        elif '"""' in line:
            chinese_model_flag = not chinese_model_flag
        elif chinese_model_flag:
            model_info_dict['model_chinese_str'] = line
        elif len(line.split('=')[0].strip()) > 0 and len(line.split('=')) > 2:
            attribute_dict = {
                'name': None,
                'field': None,
                'default': None,
                'choices': None,
                'verbose': None,
                'foreign': None,
            }
            try:
                attribute_dict['name'] = line.split('=')[0].strip()
            except AttributeError:
                pass
            try:
                attribute_dict['field'] = line.split('=')[1][8:].split('(')[0]
            except AttributeError:
                pass
            try:
                attribute_dict['default'] = re.match(r'.*?default=(.*?),', line).group(1)
            except AttributeError:
                pass
            try:
                attribute_dict['choices'] = re.match(r'.*?choices=(.*?),', line).group(1)
            except AttributeError:
                pass
            try:
                verbose = re.match(r".*?verbose_name=(.*?)[,)]", line).group(1)
                if verbose[0] == 'u':
                    verbose = verbose[1:]
                attribute_dict['verbose'] = verbose.replace('"', '').replace("'", '')
            except AttributeError:
                pass
            try:
                attribute_dict['foreign'] = re.match(r".*?ForeignKey\((.*?),", line).group(1)
            except AttributeError:
                pass
            # field处理
            if attribute_dict['field'] == "DecimalField":
                attribute_dict['type'] = "decimal"
            elif attribute_dict['field'] == "IntegerField":
                attribute_dict['type'] = "int"
            elif attribute_dict['field'] == "ForeignKey" and attribute_dict.get('name', None):
                attribute_dict['type'] = attribute_dict['name'] + "_id"
            model_info_dict.setdefault('model_params', []).append(attribute_dict)
            model_info_dict.setdefault('model_params_list', []).append(attribute_dict['name'])
            model_info_dict.setdefault('model_params_dict', {}).update({attribute_dict['name']:attribute_dict['verbose']})

    return model_info_dict


def get_field_info_dict(model_info_dict):
    field_info_dict = {
        'request': '',
        'org_id': '',
        model_info_dict['model_id_str']: model_info_dict.get('model_chinese_str', ''),
        'is_active': PARAM_DICT.get('is_active'),
        'page_index': PARAM_DICT.get('page_index'),
        'page_size': PARAM_DICT.get('page_size'),
        'person': '',
    }
    field_info_dict.update(model_info_dict['model_params_dict'])
    return field_info_dict


def get_foreign_info_dict(model_params):
    foreign_info_dict = {
        'foreign_list': [],
        'foreign_dot_str': '',
        'foreign_get_str': '',
        'foreign_try_str': '',
    }
    for item in model_params:
        if item['foreign'] is not None:
            foreign_get_str = """
        {}.objects.get(pk={}, is_active=True)""".format(item["foreign"], item["type"])
            foreign_try_str = """
        except {}.DoesNotExist:
                return get_result(False, u"{}信息不存在") """.format(item["foreign"], item["verbose"])

            foreign_info_dict['foreign_list'].append(item['foreign'])
            if foreign_info_dict['foreign_dot_str'] == '':
                foreign_info_dict['foreign_dot_str'] = item['foreign']
            else:
                foreign_info_dict['foreign_dot_str'] = foreign_info_dict['foreign_dot_str'] + ', ' + item['foreign']
            foreign_info_dict['foreign_get_str'] = foreign_info_dict['foreign_get_str'] + foreign_get_str
            foreign_info_dict['foreign_try_str'] = foreign_info_dict['foreign_try_str'] + foreign_try_str

    return foreign_info_dict


def get_var_info_dict(model_info_dict):
    var_str_dict = {
        'var_create_list': ['request', 'org_id'],
        'var_update_list': ['request', 'org_id', model_info_dict['model_id_str']],
        'var_delete_list': ['request', 'org_id', model_info_dict['model_id_str'], 'person'],
        'var_recover_list': ['request', 'org_id', model_info_dict['model_id_str'], 'person'],
        'var_query_list': ['request'],
    }

    for item in model_info_dict['model_params']:

        var_str_dict['var_create_list'].append(item['name'])
        var_str_dict['var_update_list'].append(item['name'])

        if item.get('type') == "decimal":
            continue
        elif item.get('type') == "int" and item.get('choices') is None:
            continue
        var_str_dict['var_query_list'].append(item['name'])

    var_str_dict['var_query_list'].extend(['is_active', 'page_index', 'page_size'])

    var_str_dict['var_create_list'].append('person')
    var_str_dict['var_update_list'].append('person')
    var_str_dict['var_query_list'].append('person')

    var_str_dict['var_create_str'] = ', '.join(var_str_dict['var_create_list'])
    var_str_dict['var_update_str'] = ', '.join(var_str_dict['var_update_list'])
    var_str_dict['var_delete_str'] = ', '.join(var_str_dict['var_delete_list'])
    var_str_dict['var_recover_str'] = ', '.join(var_str_dict['var_recover_list'])
    var_str_dict['var_query_str'] = ', '.join(var_str_dict['var_query_list'])
    return var_str_dict


def get_param_info_dict(field_info_dict, var_str_dict):
    _dot = '    """'
    param_str_dict = {
        'param_create_list': [_dot],
        'param_update_list': [_dot],
        'param_delete_list': [_dot],
        'param_recover_list': [_dot],
        'param_query_list': [_dot],
    }
    param_list_end = ['    :return: ', '    """']
    param_str_dict['param_create_list'] = deal_param_func(var_str_dict['var_create_list'], field_info_dict, ['\t创建{}'], param_list_end)
    param_str_dict['param_update_list'] = deal_param_func(var_str_dict['var_update_list'], field_info_dict, ['\t更新{}'], param_list_end)
    param_str_dict['param_delete_list'] = deal_param_func(var_str_dict['var_delete_list'], field_info_dict, ['\t删除{}'], param_list_end)
    param_str_dict['param_recover_list'] = deal_param_func(var_str_dict['var_recover_list'], field_info_dict, ['\t恢复{}'], param_list_end)
    param_str_dict['param_query_list'] = deal_param_func(var_str_dict['var_query_list'], field_info_dict, ['\t查询{}'], param_list_end)

    param_str_start = ''
    param_str_middle = '\n'
    param_str_end = ''
    param_str_dict['param_create_str'] = deal_list_to_str(param_str_dict['param_create_list'], param_str_start, param_str_middle, param_str_end)
    param_str_dict['param_update_str'] = deal_list_to_str(param_str_dict['param_update_list'], param_str_start, param_str_middle, param_str_end)
    param_str_dict['param_delete_str'] = deal_list_to_str(param_str_dict['param_delete_list'], param_str_start, param_str_middle, param_str_end)
    param_str_dict['param_recover_str'] = deal_list_to_str(param_str_dict['param_recover_list'], param_str_start, param_str_middle, param_str_end)
    param_str_dict['param_query_str'] = deal_list_to_str(param_str_dict['param_query_list'], param_str_start, param_str_middle, param_str_end)

    return param_str_dict


def process_json(var_list):
    lis = []
    for item in var_list:
        s = """    "{}": "", """.format(item)
        lis.append(s)
    var_json = "{\n" + '\n'.join(lis)[:-2] + "  }"
    return var_json

def process_if(para_list):
    lis = []
    for i, dic in enumerate(para_list):
        if dic['field'] == 'ForeignKey':
            s = """
        if {1} is not None:
            {0}.objects.get(pk={1}, is_active=True)
            obj.{1} = {1}""".format(dic["foreign"], dic['var'])
            lis.append(s)
    for i, dic in enumerate(para_list):
        if dic['field'] == 'int':
            s = """
        if {0} is not None:
            obj.{0} = {0}""".format(dic['var'])
        elif dic['field'] == 'CharField':
            s = """
        if {0}:
            obj.{0} = {0}""".format(dic['var'])
        elif dic['field'] == 'ForeignKey':
            continue
        else:
            s = """
        if {0} is not None:
            obj.{0} = {0}""".format(dic['var'])
        lis.append(s)
    var_if = ''.join(lis)

    return var_if

def process_query(para_list):
    lis = []
    for i, dic in enumerate(para_list):
        if dic['field'] == 'ForeignKey':
            s = """
    if {0} is not None:
        query = query.field({0}={0})""".format(dic['var'])
            lis.append(s)
    for i, dic in enumerate(para_list):

        if dic['field'] == "decimal":
            continue
        elif dic['field'] == "int" and dic['choices'] is None:
            continue
        elif dic['field'] == "ForeignKey":
            continue
        else:
            pass
        if dic['field'] == 'int':
            s = """
    if {0} is not None:
        query = query.field({0}={0})""".format(dic['var'])
        elif dic['field'] == 'CharField' or dic['field'] == 'TextField':
            s = """
    if {0}:
        query = query.field({0}__icontains={0})""".format(dic['var'])
        else:
            s = """
    if {0} is not None:
        query = query.field({0}={0})""".format(dic['var'])
        lis.append(s)
    var_query = ''.join(lis)

    return var_query

def process_check(para_list, model, model_low, model_str, app_name, model_upper, flag=0):
    lis = ['org_id=("组织id", "r,liyu_organization.Organization__pk")']

    if flag == 1:
        lis.append('  {}_id=("{}id", "r,{}.{}__pk")'.format(model_low, model_str, app_name, model_upper))

    for i, dic in enumerate(para_list):
        s = ''
        # 外键处理
        if dic['foreign'] is not None:
            # 创建必传
            if flag == 0:
                s = '  {}=("{}id", "r,{}.{}__pk")'.format(dic['var'], dic['verbose'], app_name, dic['foreign'])
            else:
                s = '  {}=("{}id", "{}.{}__pk")'.format(dic['var'], dic['verbose'], app_name, dic['foreign'])
        elif dic['default'] is not None:
            if dic['field'] == 'int':
                if dic['choices'] is not None:
                    # 有选择的
                    s = '  {}=("{}", "{}", None, {}.{})'.format(dic['var'], dic['verbose'], dic['field'], model,
                                                                dic['choices'])
                else:
                    if flag == 2:
                        continue
                    s = '  {}=("{}", "{}", {})'.format(dic['var'], dic['verbose'], dic['field'], dic['default'])
            elif dic['field'] == 'decimal':
                if flag == 2:
                    continue
                s = '  {}=("{}", "{}", {})'.format(dic['var'], dic['verbose'], dic['field'], dic['default'])
        elif dic['default'] is None:
            # 无默认值的
            if dic['field'] == 'int':
                s = '  {}=("{}", "{}")'.format(dic['var'], dic['verbose'], dic['field'])
            elif dic['field'] == 'decimal':
                s = '  {}=("{}", "{}")'.format(dic['var'], dic['verbose'], dic['field'])
            else:
                s = '  {}=("{}", "")'.format(dic['var'], dic['verbose'])
        lis.append(s)
    if flag == 2:
        s = """  is_active=("状态", "b")"""
        lis.append(s)
        s = """  page_index=("页号", "int", 1)"""
        lis.append(s)
        s = """  page_size=("页大小", "int", 20)"""
        lis.append(s)
    var_check = ',\n\t\t\t\t\t'.join(lis)

    return var_check
