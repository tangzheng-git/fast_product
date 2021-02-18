#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/01/13
# file: fragment.py
# Email:
# Author: 唐政 

class ProductionErrorBindRule(BaseModel):
    """
    生产记录错捆规则
    """
    diameter = models.FloatField(default=0, verbose_name=u'规格')
    weight_m = models.FloatField(default=0, verbose_name=u'米重')
    m_select = models.IntegerField(verbose_name=u'米重选择')
    weight_min = models.FloatField(default=0, verbose_name=u'当前米重最小值')
    weight_max = models.FloatField(default=0, verbose_name=u'当前米重最大值')

    class Meta:
        list_json = ['id', 'diameter', 'weight_m', 'm_select', 'weight_min', 'weight_max']
        detail_json = ['create_time', 'is_active']
        unique_together = ("diameter", "m_select")


#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/01/13
# file: views_product_error_bind_rule.py
# Email:
# Author: 唐政
from production_manage.models import ProductionErrorBindRule
from util.model_base_fun import model_delete_fun, model_recover_fun
from django.db import IntegrityError
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required
from django.db import transaction
from django.db import IntegrityError
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(
    org_id=("组织id", "r,liyu_organization.Organization__pk"),
    diameter=("规格", "r"),
    weight_m=("米重", ""),
    m_select=("米重选择", "r"),
    weight_min=("当前米重最小值", "r"),
    weight_max=("当前米重最大值", "r"),
)
@client_login_required
def create_product_error_bind_rule(request, org_id, diameter, weight_m, m_select, weight_min, weight_max, person):
    try:
        obj = ProductionErrorBindRule()
        obj.diameter = diameter

        diameter_obj = ProductionErrorBindRule.objects.filter(diameter=diameter, is_active=True).first()

        if weight_m and diameter_obj:
            return get_result(False, u'对应规格 米重已定义')
        elif not weight_m and diameter_obj:
            obj.weight_m = diameter_obj.weight_m
        elif not weight_m and not diameter_obj:
            return get_result(False, u'对应规格 米重未定义')
        else:
            obj.weight_m = weight_m

        obj.m_select = m_select
        obj.weight_min = weight_min
        obj.weight_max = weight_max

        obj.save()
        return get_result(True, u'创建标签信息成功', obj)
    except IntegrityError:
        return get_result(False, u'对应规格 {}米重已存在'.format(m_select))


@check_request_parmes(
    org_id=("组织id", "r,liyu_organization.Organization__pk"),
    error_bind_rule_id=("错捆规则id", "r,production_manage.ProductionErrorBindRule__pk"),
    diameter=("规格", ""),
    weight_m=("米重", ""),
    m_select=("米重选择", ""),
    weight_min=("当前米重最小值", ""),
    weight_max=("当前米重最大值", ""),
)
@client_login_required
def update_product_error_bind_rule(request, org_id, error_bind_rule_id, diameter, weight_m, m_select, weight_min, weight_max, person):
    try:
        if diameter and weight_m:
            query = ProductionErrorBindRule.objects.filter(diameter=diameter, is_active=True)

        update_list = []
        if weight_m:
            for q in query:
                q.weight_m = weight_m
                update_list.append(q)

        obj = query.filter(m_select=m_select).first()

        obj.weight_min = weight_min
        obj.weight_max = weight_max

        obj.save()
        return get_result(True, u'创建标签信息成功', obj)
    except IntegrityError:
        return get_result(False, u'对应规格 {}米重已存在'.format(m_select))