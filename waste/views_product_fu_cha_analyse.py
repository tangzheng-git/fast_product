#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/01/05
# file: views_product_fu_cha_analyse.py
# Email:
# Author: 唐政
import datetime
import json

from liyu_organization.models import Organization
from liyu_organization.org_tools import check_org_relation
from material_storage.models import SteelType
from production_manage.models import ProductItem, ProductionRecord, ProductGongYi, PlanItem, ProductionRecordItem, \
    PlanExcelImportSetting
from roller.models import RollerSpecification
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required, check_permissions_and_log
from util.model_tools import page_obj_query

@check_request_parmes(
    org_id=("org_id", "r,liyu_organization.Organization__pk"),
    aim_org_id=("org_id", "liyu_organization.Organization__pk"),
    bind_no=("捆号", ""),
    truck_no=("装车单号", ""),
    time_interval=("时间区间", "r,[date]"),
    steel_type_id=("钢种id", "material_storage.SteelType__pk"),
    prod_thick=("口径", ""),
    roll_no=("轧制序号", ""),
    shift_name=("班别", ""),
    shift_flag=("班次", ""),
    page_index=("页码", "int", 1),
    page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
@check_permissions_and_log(is_normal_api=True, template_name='default_template.html')
def analyse_product_fu_cha_result(request, org_id, aim_org_id, bind_no, truck_no, time_interval, steel_type_id,
                                  prod_thick, roll_no, shift_name, shift_flag, page_index, page_size, person):
    """

    :param request:
    :param org_id:
    :param aim_org_id:
    :param bind_no:
    :param truck_no:
    :param time_interval:
    :param steel_type_id:
    :param prod_thick:
    :param roll_no:
    :param shift_name:
    :param shift_flag:
    :param page_index:
    :param page_size:
    :param person:
    :return:

    by:唐政 at:2021-1-05
    """

    if not time_interval[0] or not time_interval[1]:
        return get_result(False, u"请提供正确的时间区间")
    if time_interval[1] < time_interval[0]:
        return get_result(False, u"结束时间不能小于起始时间")

    if aim_org_id is None:
        aim_org_id = org_id

    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__heat_no', 'plan_item__gongyi__name',
        'plan_item__prod_thick', 'plan_item__weight', 'plan_item__num', 'plan_item__trade_no_id',
        'plan_item__trade_no__name',
    ). \
        filter(
        org_id=aim_org_id,
        create_time__gte=time_interval[0],
        create_time__lte=time_interval[1] + datetime.timedelta(days=1),
        is_active=True).order_by("-create_time")

    if steel_type_id:
        record_query = record_query.filter(plan_item__trade_no_id=steel_type_id)
    if prod_thick:
        record_query = record_query.filter(plan_item__prod_thick=prod_thick)
    if roll_no:
        record_query = record_query.filter(plan_item__roll_no=roll_no)

    roller_query = RollerSpecification.objects.values(
        'id', 'name', 'diameter',
    ).filter(org__id=org_id)

    flag_list = ['zha_gang_fu_cha_target_{}_{}'.format(int(roller['diameter']), org_id) for roller in roller_query]

    setting_query = PlanExcelImportSetting.objects.filter(is_active=True, flag__in=flag_list)

    diameter_dict = {}
    for setting in setting_query:
        try:
            diameter_dict[str(setting.flag.split('_')[-2])] = json.loads(setting.content)
        except:
            diameter_dict[str(setting.flag.split('_')[-2])] = None

    result_list = []
    update_list = []
    dis_list = []
    for i, record in enumerate(record_query):


        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'heat_no', 'product_time', 'shift_name', 'shift_flag', 'num',
            'diameter', 'fixed_length', 'status', 'shape_code', 'truck_no', 'bind_status'). \
            using(aim_org_id).filter(is_active=True, org_id=aim_org_id, roll_no=record['plan_item__roll_no'])

        if bind_no:
            item_query = item_query.filter(bind_no=bind_no)
        if truck_no:
            item_query = item_query.filter(truck_no=truck_no)
        if shift_name:
            item_query = item_query.filter(shift_name=shift_name)
        if shift_flag:
            item_query = item_query.filter(shift_flag=shift_flag)

        record_item_query = ProductionRecordItem.objects.values(
            'id',
            'real_weight'
        ).using(aim_org_id). \
            filter(org_id=aim_org_id, production_record_id=record['id'], is_active=True). \
            exclude(conclusion=ProductionRecordItem.Conclusion_None, )

        for item, record_item in zip(item_query, record_item_query):
            result_dict = {}
            truck_query = ProductItem.objects.values('bind_no').using(aim_org_id).filter(truck_no=item['truck_no'], is_active=True)
            result_dict['product_record_id'] = record['id']
            result_dict['roll_no'] = record['plan_item__roll_no']
            result_dict['steel_type_id'] = record['plan_item__trade_no_id']
            result_dict['steel_type_name'] = record['plan_item__trade_no__name']
            result_dict['gongyi'] = record['plan_item__gongyi__name']
            result_dict['ll_weight'] = record['plan_item__weight'] / record['plan_item__num'] if record['plan_item__num'] else 0
            result_dict['item_id'] = item['id']
            result_dict['record_item_id'] = record_item['id']
            result_dict['bind_no'] = item['bind_no']
            result_dict['merge_no'] = item['merge_no']
            result_dict['product_time'] = item['product_time']
            result_dict['shift_name'] = item['shift_name']
            result_dict['shift_flag'] = item['shift_flag']
            result_dict['num'] = item['num']
            result_dict['diameter'] = int(item['diameter'])
            result_dict['fixed_length'] = item['fixed_length']
            result_dict['status'] = item['status']
            result_dict['shape_code'] = item['shape_code']
            result_dict['sj_weight'] = record_item['real_weight']

            fc_calculate = (result_dict['ll_weight'] - result_dict['sj_weight']) * 100 / result_dict['sj_weight'] if \
            result_dict['sj_weight'] else 0
            result_dict['diff'] = round(fc_calculate, 2)

            result_dict['diff_standard'] = diameter_dict.get(str(result_dict['diameter']), None)

            if result_dict['diff_standard']:
                if result_dict['diff_standard'].get('min_value', 0) <= result_dict['diff'] <= result_dict['diff_standard'].get('max_value', 0):
                    bind_status = 0
                else:
                    bind_status = 1
            else:
                bind_status = 0

            if item['id'] == 4648155:
                print item['fc_remark']
                print item['fc_remark'] is None

            if bind_status != item['bind_status'] and item['fc_remark'] is None:
                obj = ProductItem.objects.using(aim_org_id).get(pk=item['id'], is_active=True)
                obj.bind_status = bind_status
                update_list.append(obj)
                result_dict['bind_status'] = bind_status
            else:
                result_dict['bind_status'] = item['bind_status']
            result_dict['fc_remark'] = item['fc_remark']
            result_dict['truck_no'] = item['truck_no']

            result_dict['truck_no_list'] = [truck['bind_no'] for truck in truck_query]

            if result_dict['item_id'] in dis_list:
                pass
            else:
                dis_list.append(result_dict['item_id'])
                result_list.append(result_dict)

    from util.django_bulk_update.helper import bulk_update
    from django.db import transaction
    with transaction.atomic():
        bulk_update(update_list, update_fields=['bind_status'], using=str(aim_org_id))

    return get_result(True, u'分析数据成功', page_obj_query(result_list, page_index, page_size))


@check_request_parmes(
    org_id=("org_id", "r,liyu_organization.Organization__pk"),
    aim_org_id=("org_id", "liyu_organization.Organization__pk"),
    bind_no=("捆号", ""),
    truck_no=("装车单号", ""),
    time_interval=("时间区间", "r,[date]"),
    steel_type_id=("钢种id", "material_storage.SteelType__pk"),
    prod_thick=("口径", ""),
    roll_no=("轧制序号", ""),
    shift_name=("班别", ""),
    shift_flag=("班次", ""),
    page_index=("页码", "int", 1),
    page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
@check_permissions_and_log(is_normal_api=True, template_name='default_template.html')
def query_product_bind_result(request, org_id, aim_org_id, bind_no, truck_no, time_interval, steel_type_id,
                                  prod_thick, roll_no, shift_name, shift_flag, page_index, page_size, person):
    """

    :param request:
    :param org_id:
    :param aim_org_id:
    :param bind_no:
    :param truck_no:
    :param time_interval:
    :param steel_type_id:
    :param prod_thick:
    :param roll_no:
    :param shift_name:
    :param shift_flag:
    :param page_index:
    :param page_size:
    :param person:
    :return:

    by:唐政 at:2021-1-08
    """

    if not time_interval[0] or not time_interval[1]:
        return get_result(False, u"请提供正确的时间区间")
    if time_interval[1] < time_interval[0]:
        return get_result(False, u"结束时间不能小于起始时间")

    if aim_org_id is None:
        aim_org_id = org_id

    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__heat_no', 'plan_item__gongyi__name',
        'plan_item__prod_thick', 'plan_item__weight', 'plan_item__num', 'plan_item__trade_no_id',
        'plan_item__trade_no__name',
    ). \
        filter(
        org_id=aim_org_id,
        create_time__gte=time_interval[0],
        create_time__lte=time_interval[1] + datetime.timedelta(days=1),
        is_active=True).order_by("-create_time")

    if steel_type_id:
        record_query = record_query.filter(plan_item__trade_no_id=steel_type_id)
    if prod_thick:
        record_query = record_query.filter(plan_item__prod_thick=prod_thick)
    if roll_no:
        record_query = record_query.filter(plan_item__roll_no=roll_no)

    result_list = []
    dist_list = []
    for i, record in enumerate(record_query):

        if record['plan_item__roll_no'] in dist_list:
            continue
        else:
            dist_list.append(record['plan_item__roll_no'])

        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'heat_no', 'product_time', 'shift_name', 'shift_flag', 'num',
            'diameter', 'fixed_length', 'status', 'shape_code', 'truck_no', 'bind_status'). \
            using(aim_org_id).filter(is_active=True, org_id=aim_org_id, roll_no=record['plan_item__roll_no'])
        if bind_no:
            item_query = item_query.filter(bind_no=bind_no)
        if truck_no:
            item_query = item_query.filter(truck_no=truck_no)
        if shift_name:
            item_query = item_query.filter(shift_name=shift_name)
        if shift_flag:
            item_query = item_query.filter(shift_flag=shift_flag)

        record_item_query = ProductionRecordItem.objects.values(
            'id',
            'real_weight'
        ).using(aim_org_id). \
            filter(org_id=aim_org_id, production_record_id=record['id'], is_active=True). \
            exclude(conclusion=ProductionRecordItem.Conclusion_None, )

        for item, record_item in zip(item_query, record_item_query):
            result_dict = {}
            truck_query = ProductItem.objects.values('bind_no').using(aim_org_id).filter(truck_no=item['truck_no'], is_active=True)
            result_dict['product_record_id'] = record['id']
            result_dict['item_id'] = item['id']
            result_dict['record_item_id'] = record_item['id']
            result_dict['roll_no'] = record['plan_item__roll_no']
            result_dict['bind_no'] = item['bind_no']
            result_dict['merge_no'] = item['merge_no']
            result_dict['product_time'] = item['product_time']
            result_dict['shift_name'] = item['shift_name']
            result_dict['shift_flag'] = item['shift_flag']
            result_dict['num'] = item['num']
            result_dict['steel_type_id'] = record['plan_item__trade_no_id']
            result_dict['steel_type_name'] = record['plan_item__trade_no__name']
            result_dict['diameter'] = int(item['diameter'])
            result_dict['fixed_length'] = item['fixed_length']
            result_dict['gongyi'] = record['plan_item__gongyi__name']
            result_dict['sj_weight'] = record_item['real_weight']
            result_dict['ll_weight'] = record['plan_item__weight'] / record['plan_item__num'] if record['plan_item__num'] else 0

            fc_calculate = (result_dict['ll_weight'] - result_dict['sj_weight']) * 100 / result_dict['sj_weight'] if result_dict['sj_weight'] else 0
            result_dict['bind_fu_cha'] = round(fc_calculate, 2)

            result_dict['bind_status'] = item['bind_status']
            result_dict['truck_no'] = item['truck_no']
            result_dict['truck_no_list'] = [truck['bind_no'] for truck in truck_query]

            result_list.append(result_dict)

    return get_result(True, u'查询数据成功', page_obj_query(result_list, page_index, page_size))

@check_request_parmes(
    org_id=("org_id", "r,liyu_organization.Organization__pk"),
    aim_org_id=("org_id", "liyu_organization.Organization__pk"),
    bind_no=("捆号", ""),
    truck_no=("装车单号", ""),
    time_interval=("时间区间", "r,[date]"),
    steel_type_id=("钢种id", "material_storage.SteelType__pk"),
    prod_thick=("口径", ""),
    roll_no=("轧制序号", ""),
    shift_name=("班别", ""),
    shift_flag=("班次", ""),
    page_index=("页码", "int", 1),
    page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
@check_permissions_and_log(is_normal_api=True, template_name='default_template.html')
def analyse_product_bind_result(request, org_id, aim_org_id, bind_no, truck_no, time_interval, steel_type_id,
                                  prod_thick, roll_no, shift_name, shift_flag, page_index, page_size, person):
    """
    错捆预警分析
    :param request:
    :param org_id:
    :param aim_org_id:
    :param bind_no:
    :param truck_no:
    :param time_interval:
    :param steel_type_id:
    :param prod_thick:
    :param roll_no:
    :param shift_name:
    :param shift_flag:
    :param page_index:
    :param page_size:
    :param person:
    :return:

    by:唐政 at:2021-1-08
    """

    if not time_interval[0] or not time_interval[1]:
        return get_result(False, u"请提供正确的时间区间")
    if time_interval[1] < time_interval[0]:
        return get_result(False, u"结束时间不能小于起始时间")

    if aim_org_id is None:
        aim_org_id = org_id

    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__gongyi__name', 'plan_item__prod_thick',
        'plan_item__weight', 'plan_item__num', 'plan_item__trade_no_id', 'plan_item__trade_no__name',
    ). \
        filter(
        org_id=aim_org_id,
        create_time__gte=time_interval[0],
        create_time__lte=time_interval[1] + datetime.timedelta(days=1),
        is_active=True).order_by("-create_time")

    if steel_type_id:
        record_query = record_query.filter(plan_item__trade_no_id=steel_type_id)
    if prod_thick:
        record_query = record_query.filter(plan_item__prod_thick=prod_thick)
    if roll_no:
        record_query = record_query.filter(plan_item__roll_no=roll_no)

    result_list = []
    dist_list = []
    up_item_dict = {}
    deal_flag = 0
    for i, record in enumerate(record_query):

        if record['plan_item__roll_no'] in dist_list:
            continue
        else:
            dist_list.append(record['plan_item__roll_no'])

        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'product_time', 'shift_name', 'shift_flag', 'num', 'diameter', 'fixed_length',
            'truck_no', 'bind_status'). \
            using(aim_org_id).filter(is_active=True, org_id=aim_org_id, roll_no=record['plan_item__roll_no'])
        if bind_no:
            item_query = item_query.filter(bind_no=bind_no)
        if truck_no:
            item_query = item_query.filter(truck_no=truck_no)
        if shift_name:
            item_query = item_query.filter(shift_name=shift_name)
        if shift_flag:
            item_query = item_query.filter(shift_flag=shift_flag)

        record_item_query = ProductionRecordItem.objects.values(
            'id',
            'real_weight'
        ).using(aim_org_id). \
            filter(org_id=aim_org_id, production_record_id=record['id'], is_active=True). \
            exclude(conclusion=ProductionRecordItem.Conclusion_None, )

        for item, record_item in zip(item_query, record_item_query):
            result_dict = {}
            truck_query = ProductItem.objects.values('bind_no').using(aim_org_id).filter(truck_no=item['truck_no'], is_active=True)
            result_dict['product_record_id'] = record['id']
            result_dict['item_id'] = item['id']
            result_dict['record_item_id'] = record_item['id']
            result_dict['roll_no'] = record['plan_item__roll_no']
            result_dict['bind_no'] = item['bind_no']
            result_dict['merge_no'] = item['merge_no']
            result_dict['product_time'] = item['product_time']
            result_dict['shift_name'] = item['shift_name']
            result_dict['shift_flag'] = item['shift_flag']
            result_dict['num'] = item['num']
            result_dict['steel_type_id'] = record['plan_item__trade_no_id']
            result_dict['steel_type_name'] = record['plan_item__trade_no__name']
            result_dict['diameter'] = int(item['diameter'])
            result_dict['fixed_length'] = item['fixed_length']
            result_dict['gongyi'] = record['plan_item__gongyi__name']
            result_dict['sj_weight'] = record_item['real_weight']
            result_dict['ll_weight'] = record['plan_item__weight'] / record['plan_item__num'] if record['plan_item__num'] else 0

            fc_calculate = (result_dict['ll_weight'] - result_dict['sj_weight']) * 100 / result_dict['sj_weight'] if result_dict['sj_weight'] else 0
            result_dict['bind_fu_cha'] = round(fc_calculate, 2)

            result_dict['bind_status'] = item['bind_status']
            result_dict['truck_no'] = item['truck_no']
            result_dict['truck_no_list'] = [truck['bind_no'] for truck in truck_query]

            if up_item_dict:

                if item['bind_status'] == ProductItem.BIND_DEAL:
                    # 待处理 转换首件确认
                    if up_item_dict['steel_type_id'] != result_dict['steel_type_id'] or up_item_dict['diameter'] != result_dict['diameter'] or up_item_dict['fixed_length'] != result_dict['fixed_length'] and up_item_dict['gongyi'] != result_dict['gongyi']:
                        # 首件处理
                        print up_item_dict['item_id'], up_item_dict['steel_type_id'], up_item_dict['diameter'], up_item_dict['fixed_length'], up_item_dict['gongyi']
                        print result_dict['item_id'], result_dict['steel_type_id'], result_dict['diameter'], result_dict['fixed_length'], result_dict['gongyi']

                        result_dict['bind_status'] = ProductItem.BIND_FIRST_CONFIRMED
                        obj = ProductItem.objects.using(aim_org_id).get(pk=item['id'], is_active=True)
                        obj.bind_status = ProductItem.BIND_FIRST_CONFIRMED
                        obj.save()
                    else:
                        deal_rule = [
                            {
                                'diameter': 10,
                                'weight_m': 0.617,
                                'weight_9m': 5.553,
                                'kg_range_9m': [-4, 4],
                                'weight_12m': 7.404,
                                'kg_range_12m': [-5, 5],
                            }
                        ]
                        # 非首件处理
                        # 无异常 ProductItem.BIND_NORMAL
                        # 异常待确认 ProductItem.BIND_CONFIRMED
                        pass

                elif item['bind_status'] == ProductItem.BIND_NORMAL:
                    # 正常
                    up_item_dict['item_id'] = item['id']
                    up_item_dict['steel_type_id'] = result_dict['steel_type_id']
                    up_item_dict['diameter'] = result_dict['diameter']
                    up_item_dict['fixed_length'] = result_dict['fixed_length']
                    up_item_dict['gongyi'] = result_dict['gongyi']

                    # 处理

                elif item['bind_status'] == ProductItem.BIND_CONFIRMED:
                    # 异常待确认不覆盖
                    pass
                elif item['bind_status'] == ProductItem.BIND_FIRST_CONFIRMED:
                    # 首件确认
                    up_item_dict['item_id'] = item['id']
                    up_item_dict['steel_type_id'] = result_dict['steel_type_id']
                    up_item_dict['diameter'] = result_dict['diameter']
                    up_item_dict['fixed_length'] = result_dict['fixed_length']
                    up_item_dict['gongyi'] = result_dict['gongyi']

                elif item['bind_status'] == ProductItem.BIND_ABNORMAL:
                    # 支数异常不覆盖
                    pass
                else:
                    return get_result(True, u'错误捆支数状态 < ProductItem#{} > need in {}'.format(item['id'], [tup[0] for tup in ProductItem.BIND_STATUS_CHOICE]))

            else:
                up_item_dict['item_id'] = item['id']
                up_item_dict['steel_type_id'] = result_dict['steel_type_id']
                up_item_dict['diameter'] = result_dict['diameter']
                up_item_dict['fixed_length'] = result_dict['fixed_length']
                up_item_dict['gongyi'] = result_dict['gongyi']

            result_list.append(result_dict)

    return get_result(True, u'查询数据成功', page_obj_query(result_list, page_index, page_size))


@check_request_parmes(org_id=("org_id", "r,liyu_organization.Organization__pk"),
                      aim_org_id=("目标组织id", "liyu_organization.Organization__pk"),
                      product_item_id=("成品捆id", "r,production_manage.ProductItem__pk"),
                      fc_remark=("负差备注", "r"),
                      bind_status=('负差状态', "int", None, ProductItem.BIND_STATUS_CHOICE))
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def update_product_item_fu_cha(request, org_id, aim_org_id, product_item_id, fc_remark, bind_status, person):
    """
    修改成品捆负差备注
    :param request:
    :param org_id:
    :param aim_org_id:
    :param product_item_id:
    :param fc_remark:
    :param bind_status:
    :param person:
    :return:
    by:唐政 at:2021-01-07
    """

    if not aim_org_id:
        aim_org_id = org_id

    obj = ProductItem.objects.using(aim_org_id).filter(is_active=True, pk=product_item_id).first()
    if not obj:
        return get_result(False, u'成品捆不存在')

    obj.bind_status = bind_status
    obj.fc_remark = fc_remark
    obj.save(update_fields=['bind_status', 'fc_remark'])

    return get_result(True, u'修改成品捆负差成功')


@check_request_parmes(aim_org_id=("目标组织id", "r,liyu_organization.Organization__pk"),
                      page_index=("页码", "int", 1),
                      page_size=("页长度", "int", 20)
                      )
def query_product_item_list_api(request, aim_org_id, page_index, page_size):

    record_query = ProductionRecord.objects.values(
        'id', 'plan_item_id', 'plan_item__roll_no', 'plan_item__gongyi__name', 'plan_item__prod_thick',
        'plan_item__weight', 'plan_item__num', 'plan_item__trade_no_id', 'plan_item__trade_no__name',
    ). \
        filter(
        org_id=aim_org_id,
        is_active=True).order_by("-create_time")

    if record_query is None:
        return get_result(False, u'对应ProductionRecord 不存在')

    if len(record_query) >= 2:
        record_query = record_query[:2]
    else:
        record_query = record_query[:1]

    result_list = []
    for i, record in enumerate(record_query):

        item_query = ProductItem.objects.values(
            'id', 'bind_no', 'merge_no', 'product_time', 'shift_name', 'shift_flag', 'num', 'diameter', 'fixed_length',
            'truck_no', 'create_time'). \
            using(aim_org_id).filter(is_active=True, org_id=aim_org_id, roll_no=record['plan_item__roll_no'])

        record_item_query = ProductionRecordItem.objects.values(
            'id',
            'real_weight'
        ).using(aim_org_id). \
            filter(org_id=aim_org_id, production_record_id=record['id'], is_active=True). \
            exclude(conclusion=ProductionRecordItem.Conclusion_None, )

        for item, record_item in zip(item_query, record_item_query):
            result_dict = {
                'product_record_id': record['id'],
                'record_item_id': record_item['id'],
                'item_id': item['id'],
                'roll_no': record['plan_item__roll_no'],
                'bind_no': item['bind_no'],
                'merge_no': item['merge_no'],
                'product_time': item['product_time'],
                'num': item['num'],
                'steel_type_id': record['plan_item__trade_no_id'],
                'steel_type_name': record['plan_item__trade_no__name'],
                'diameter': int(item['diameter']),
                'fixed_length': item['fixed_length'],
                'create_time': item['create_time'],
                'gongyi': record['plan_item__gongyi__name'],
                'sj_weight': record_item['real_weight'],
                'll_weight': record['plan_item__weight'] / record['plan_item__num'] if record['plan_item__num'] else 0, 'truck_no': item['truck_no']
            }

            result_list.append(result_dict)

    return get_result(True, u'查询数据成功', page_obj_query(result_list, page_index, page_size))
