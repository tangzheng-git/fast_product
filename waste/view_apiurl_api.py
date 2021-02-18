#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/29
# file: views_apiurl_api.py
# Email:
# Author: 唐政

import os
from liyuMES import settings
from django.conf import settings

from liyu_permission import models
from util.jsonresult import get_result
from .models import ApiUrl
from util.loginrequired import check_request_parmes
from util.model_tools import page_obj_query

@check_request_parmes()
def query_api_url_list_api(request):
    query = ApiUrl.objects.values('id', 'name', 'url').filter(is_active=True)

    result_list = []

    for each_api_url in query:
        _dict = {
            'id': each_api_url['id'],
            'name': each_api_url['name'].strip(),
            'url': each_api_url['url'],
        }
        result_list.append(_dict)

    return get_result(True, u'查询url列表成功', page_obj_query(result_list, 1, False))

@check_request_parmes()
def auto_create_apiurl_api(request):
    api_func_list = get_all_url_views('^', settings.ROOT_URLCONF)

    update_list = []
    create_list = []
    result_list = []
    for url, views_ in api_func_list:
        if views_.find('django') == 0:
            continue
        # ('phonegap/get_latest_code', u'phonegap.views.get_latest_code')
        views_list = views_.split('.')
        func_name = views_list[-1]
        file_path = os.path.join(settings.BASE_DIR, *views_list[:-1])

        code_list = file('%s.py' % file_path).readlines()
        key_list = []
        # 找出关键点, 首行不缩进的 以 特定字符开头的 都是关键点
        for i, code in enumerate(code_list):
            code_first_char = code[0]
            if code_first_char in ['@', 'd', 'c', 'f', 'i']:
                key_list.append((i, code_first_char, code))

        # 找出函数体开始和结束的点, 重复函数要排除
        fun_end = 0
        fun_start = 0
        for i, (index, code_first_char, code) in enumerate(key_list):
            if code_first_char == 'd' and code.find('def %s(' % func_name) >= 0:
                if len(key_list) == i + 1:
                    fun_end = len(code_list)
                else:
                    fun_end = key_list[i + 1][0]
                    key_list = key_list[:i + 1]
                break
        key_list.reverse()
        for i, (index, code_first_char, code) in enumerate(key_list):
            if i > 0 and code_first_char in ['d', 'c', 'f', 'i']:
                fun_start = key_list[i - 1][0]
                key_list = key_list[:i]
                break
        key_list.reverse()

        # 找出doc信息的位置
        fun_doc_start = 0
        fun_doc_end = 0
        for i in range(fun_start, fun_end):
            code = code_list[i]
            if code.find('"""') > 0 or code.find("'''") > 0:
                if fun_doc_start == 0:
                    fun_doc_start = i + 1
                else:
                    fun_doc_end = i
                    break
        fun_doc = code_list[fun_doc_start: fun_doc_end]

        if len(fun_doc) > 0:
            api_name = fun_doc[0].decode('utf8').strip()
        else:
            api_name = ''

        url_part = url.split('/')
        if len(url_part) > 1:
            last_str = url_part[-1]
            auth = 0 if "query" in last_str else 1
        else:
            auth = 0

        api_url = ApiUrl.objects.filter(url=url).first()
        if api_url:
            api_url.copy_old()
            api_url.name = api_name
            api_url.is_auth = auth
            create, diff = api_url.compare_old()

            if diff:
                update_list.append(api_url)
        else:
            api_url = ApiUrl()
            api_url.name = api_name
            api_url.url = url
            api_url.is_auth = auth
            create_list.append(api_url)

        result_list.append({
            'id': api_url.id,
            'name': api_url.name,
            'url': api_url.url,
            'is_auth': api_url.is_auth,
        })

    from util.django_bulk_update.helper import bulk_update
    from django.db import transaction
    with transaction.atomic():
        bulk_update(update_list, update_fields=['name', 'is_auth'])
        models.ApiUrl.objects.bulk_create(create_list, batch_size=100)
        pass

    return get_result(True, u'同步接口成功', page_obj_query(result_list, 1, False))

def get_all_url_views(pattern, urlconf_name):
    if isinstance(urlconf_name, (str, unicode)):
        exec('import %s' % urlconf_name)
        url_mod = eval(urlconf_name)
    else:
        url_mod = urlconf_name

    url_all = []
    if hasattr(url_mod, "urlpatterns"):
        urlpatterns = url_mod.urlpatterns
        for url_pattern in urlpatterns:
            new_pattern = pattern + url_pattern.regex.pattern[1:]
            if new_pattern[0] == '^':
                new_pattern = new_pattern[1:]
            if new_pattern[-1] == '$':
                new_pattern = new_pattern[:-1]
            if hasattr(url_pattern, 'urlconf_name'):
                # 存在urls子模块，递归该方法
                url_all.extend(get_all_url_views(new_pattern, url_pattern.urlconf_name))
            else:
                url_all.append((new_pattern, url_pattern._callback_str))
    return url_all