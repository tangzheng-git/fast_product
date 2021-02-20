#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/16
# file: material_api.py
# Email:
# Author: 唐政 

api = """#!/usr/bin/env python
# encoding: utf-8
# Date: {now_year}/{now_month}/{now_day}
# file: views_{model_lower_str}.py
# Email:
# Author: {user} 


from django.db import IntegrityError
from util.model_base_fun import model_delete_fun, model_recover_fun
from {app_name}.models import {model_upper_str}, {foreign_dot_str}
from util.jsonresult import get_result
from util.login_appapi import check_permissions_and_log
from util.login_org_person import check_org_relation
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes({var_check_create})
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def create_{model_lower_str}({var_create_str}):
    {var_dot}
    创建{model_str}信息
{param_create_str}
    创建{model_str}信息
    {do_thing}
    {var_dot}
    try:
    {foreign_get_str}
    
        obj = {model_upper_str}()
{var_if_common_str}

        obj.save()
        return get_result(True, u'创建{model_str}信息成功', obj)
{foreign_try_str}
    except IntegrityError:
        return get_result(False, u'{model_str}信息已存在，创建失败')


@check_request_parmes({var_check_update})
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def update_{model_lower_str}({var_update_str}):
    {var_dot}
    修改{model_str}信息
{param_update_str}
    修改{model_str}信息
    {do_thing}
    {var_dot}
    try:
        obj = {model_upper_str}.objects.get(pk={model_id_str}, is_active=True)
{var_if_common_str}
        
        obj.save()
        return get_result(True, u'修改{model_str}信息成功', obj)
    except {model_upper_str}.DoesNotExist:
        return get_result(False, u"{model_str}信息不存在")
{foreign_try_str}
    except IntegrityError:
        return get_result(False, u'{model_str}信息已存在，修改失败')


@check_request_parmes(org_id=("组织id", "r,liyu_organization.Organization__pk"),
                      {model_id_str}=("{model_str}id", "r,{app_name}.{model_upper_str}__pk"))
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def delete_{model_lower_str}(request, org_id, {model_id_str}, person):
    {var_dot}
    删除{model_str}信息
    :param request:
    :param org_id: 组织id
    :param {model_id_str}: {model_str}id
    :param person:
    :return:
    删除{model_str}信息
    {do_thing}
    {var_dot}
    
    return model_delete_fun({model_upper_str}, {model_id_str}, None, u'删除{model_str}信息成功')


@check_request_parmes(org_id=("组织id", "r,liyu_organization.Organization__pk"),
                      {model_id_str}=("{model_str}id", "r,{app_name}.{model_upper_str}__pk"))
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def recover_{model_lower_str}(request, org_id, {model_id_str}, person):
    {var_dot}
    恢复{model_str}信息
    :param request:
    :param org_id: 组织id
    :param {model_id_str}: {model_str}id
    :param person:
    :return:
    恢复{model_str}信息
    {do_thing}
    {var_dot}
    
    return model_recover_fun({model_upper_str}, {model_id_str}, None, u'恢复{model_str}信息成功')


@check_request_parmes(org_id=("组织id", "r,liyu_organization.Organization__pk"))
@client_login_required
@check_org_relation()
@check_permissions_and_log(is_normal_api=True, template_name='default_template.html')
def query_{model_lower_str}_select_list(request, org_id, person):
    {var_dot}
    {model_str}信息下拉选框
    :param request:
    :param org_id:组织id
    :param person:
    :return:
    {model_str}信息下拉选框
    {do_thing}
    {var_dot}
    query = {model_upper_str}.objects.values('id', 'name').filter(is_active=True)

    return get_result(True, u'查询{model_str}信息成功', query.get_page(1, False))


@check_request_parmes({var_check_query})
@client_login_required
@check_org_relation()
@check_permissions_and_log(is_normal_api=True, template_name='default_template.html')
def query_{model_lower_str}_list({var_query_str}):
    {var_dot}
    查询{model_str}信息
{param_query_str}
    查询{model_str}信息
    by:唐政 at:2020-11-16
    {var_dot}
    query = {model_upper_str}.objects.detail_json()
    
    if is_active is not None:
        query = query.filter(is_active=is_active)
{var_if_query_str}

    return get_result(True, u'查询{model_str}信息成功', query.get_page(page_index, page_size))

"""