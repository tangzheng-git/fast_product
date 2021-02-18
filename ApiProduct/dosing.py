#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: dosing.py
# Email:
# Author: 唐政
import re


from api_product import PARAM_DICT


def process_lis(RAW_MATERIAL_FACTORY_MODEL):
    """
    从文件从获取model
    :return:
    """
    model_list = []
    s = ''
    with open(RAW_MATERIAL_FACTORY_MODEL, 'r', encoding='UTF-8') as f:
        s = f.read()
    model_list = s.split('\n')
    return model_list


def process_params(model_list):
    """
    生成字段字典
    :param model_list:
    :return:
    """
    para_list = []
    model = ''

    for item in model_list:
        # 符合要求的是字段
        # 否则是model
        if len(item.split('=')[0].strip()) > 0 and len(item.split('=')) > 2:
            var = item.split('=')[0].strip()
            field = item.split('=')[1][8:].split('(')[0]
            default = None
            choices = None
            verbose = ''
            foreign = None
            try:
                default = re.match(r'.*?default=(.*?),', item).group(1)
            except AttributeError:
                pass
            try:
                choices = re.match(r'.*?choices=(.*?),', item).group(1)
            except AttributeError:
                pass
            try:
                verbose = re.match(r".*?verbose_name=u'(.*?)'", item).group(1)
            except AttributeError:
                pass
            try:
                foreign = re.match(r".*?ForeignKey\((.*?),", item).group(1)
            except AttributeError:
                pass
            # field处理
            if field == "DecimalField":
                field = "decimal"
            elif field == "IntegerField":
                field = "int"
            elif field == "ForeignKey":
                var = var + "_id"
            para_list.append(dict(var=var, field=field, choices=choices, default=default, verbose=verbose, foreign=foreign))
        else:
            try:
                model = re.match(r'.*?class (.*?)\(BaseModel\)', item).group(1)
            except AttributeError:
                pass

    return model, para_list, [dic['var'] for dic in para_list]


def process_str(para_list, model_id, flag=0):
    var_list = ['request', 'org_id']

    if flag == 1:
        var_list.append(model_id)

    if flag == 2:
        for dic in para_list:
            if dic['field'] == "decimal":
                continue
            elif dic['field'] == "int" and dic['choices'] is None:
                continue
            var_list.append(dic['var'])
    else:
        for dic in para_list:
            var_list.append(dic['var'])

    if flag == 2:
        var_list.append('is_active')
        var_list.append('page_index')
        var_list.append('page_size')
    var_list.append('person')
    return ', '.join(var_list)


def process_param(para_list, model_id, model_str, flag=0):
    lis = []

    s = """:param request: """
    lis.append(s)
    s = """    :param org_id: {}""".format(PARAM_DICT.get('org_id'))
    lis.append(s)
    if flag == 1:
        s = """    :param {}: {}id""".format(model_id, model_str)
        lis.append(s)

    if flag == 2:
        for item in para_list:
            if item['field'] == "decimal":
                continue
            elif item['field'] == "int" and item['choices'] is None:
                continue
            s = """    :param {}:{}""".format(item['var'], item['verbose'])
            lis.append(s)
    else:
        for item in para_list:
            s = """    :param {}:{}""".format(item['var'], item['verbose'])
            lis.append(s)

    if flag == 2:
        s = """    :param is_active: {}""".format(PARAM_DICT.get('is_active'))
        lis.append(s)
        s = """    :param page_index: {}""".format(PARAM_DICT.get('page_index'))
        lis.append(s)
        s = """    :param page_size: {}""".format(PARAM_DICT.get('page_size'))
        lis.append(s)

    s = """    :param person:""".format(PARAM_DICT.get('page_size'))
    lis.append(s)
    s = """    :return:""".format(PARAM_DICT.get('page_size'))
    lis.append(s)

    var_param = '\n'.join(lis)
    return var_param


def process_foreignkey(para_list):
    foreign_list = []
    for item in para_list:
        if item['foreign'] is not None:
            foreign_list.append(item)
    return foreign_list


def process_foreign_list(foreign_dict_list):
    foreign_list = []
    for item in foreign_dict_list:
        foreign_list.append(item['foreign'])
    return ', '.join(foreign_list)


def process_foreignget(foreign_list):
    lis = []

    for item in foreign_list:
        s = """
        {}.objects.get(pk={}, is_active=True)""".format(item["foreign"], item["var"])
        lis.append(s)
    foreign_get_str = ''.join(lis)
    return foreign_get_str


def process_foreigntry(foreign_list):
    lis = []
    for item in foreign_list:
        s = """
    except {}.DoesNotExist:
        return get_result(False, u"{}信息不存在") """.format(item["foreign"], item["verbose"])
        lis.append(s)
    foreign_get_str = ''.join(lis)
    return foreign_get_str


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
                    s = '  {}=("{}", "{}", None, {}.{})'.format(dic['var'], dic['verbose'], dic['field'], model, dic['choices'])
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