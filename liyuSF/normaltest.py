#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/11
# file: normaltest.py
# Email:
# Author: 唐政 

import itertools
import logging
from django.db import connections, models


def grouper(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def gen_update_sql(obj):
    # 目前不支持组合主键更新
    meta = obj.meta
    pk_field = meta.get_field(meta.pk.name)
    db_table = meta.db_table
    conditions = '{pk} = %s'.format(pk=pk_field.column)
    fields = [(f.column, f.attname) for f in meta.concrete_fields if not f.primary_key]
    values = ', '.join(['%s = %s' % (f[0], '%s') for f in fields])
    fields.append((pk_field.column, pk_field.attname))
    update_sql = 'update {db_table} set {values} where {conditions}'.format(db_table=db_table, values=values, conditions=conditions)
    return update_sql, fields


def bulk_update(objs, batch_size=10, using='db_tag'):
    flag = False
    if not objs:
        return flag
    connection = connections[using]
    try:
        with connection.cursor() as cursor:
            update_sql, fields = gen_update_sql(objs[0])
            params = []
            for objs_batch in grouper(objs, batch_size):
                params[:] = []
                for obj in objs_batch:
                    params.append([getattr(obj, f[1]) for f in fields])
                cursor.executemany(update_sql, params)
                connection.commit()
        flag = True
    except Exception as e:
        logging.error('batch update error, msg = %s', e.message)
    finally:
        connection.close()
    return flag

#

#
# # 当前目录下所有文件的name全修改
# # file_query = StaticFile.objects.detail_json().using(STATICFILE_DB).filter(dir_id=obj.id)
# # 待处理
# old_display_name = obj.display_name
#
# obj.display_name = '/' + name
#
# if obj.parent_id is not None:
#     parent = StaticDir.objects.get(pk=obj.parent_id, is_active=True)
#     obj.display_name = parent.display_name + obj.display_name
#
# obj.name = name
#
# StaticDir.objects.filter(name__startswith=old_display_name).update(display_name=)
#
#
#
# if parent_id:
#     dir_query = StaticDir.objects.detail_json().filter(parent_id=parent_id, is_active=True)
#
#     dirname_list = [q['name'] for q in dir_query]
#
#     if obj.name in dirname_list:
#         return get_result(False, u'目录已存在,移动失败')
#
#     obj.parent_id = parent_id
#
# if sort_rule is not None:
#     obj.sort_rule = sort_rule
# obj.save()