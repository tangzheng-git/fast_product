#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/11
# file: staticfile.py
# Email:
# Author: 唐政 

import zipfile


def upload_staticfiles_by_url(pre_dir, url):
    import requests
    import zipfile
    import cStringIO
    import os
    res = requests.get(url=url)
    if res.status_code != 200:
        from util.tools import send_sentry_message
        send_sentry_message(u'自动根据url下载更新记录，失败')
        return

    # 保存临时文件目录
    bc_dir = './test/'
    cs = cStringIO.StringIO(res.content)
    z_file_list = zipfile.ZipFile(cs, "r")

    file_dir_list = []
    for file_dir in z_file_list.namelist():
        if not file_dir.endswith("/"):
            file_dir_list .append((pre_dir + '/' + file_dir, file_dir, file_dir.split('/')[-1]))

    z_file_list.extractall(bc_dir.strip('/'))

    # 保存临时文件
    # for i in file_dir_list:
    #     print i
    #     with open(bc_dir + '{}'.format(i[2]), 'w+') as f:
    #         content = z_file_list.read(i[1])
    #         f.write(content)

    # 写入数据库
    print os.listdir(bc_dir.strip('/'))
    for i in file_dir_list:
        with open(bc_dir + i[2], 'rb+') as f:
            content = f.read()
            print content
        # try:
        #     with transaction.atomic():
        #         obj = StaticFile(name=i[0])
        #         if content is not None:
        #             obj.content = content
        #         obj.is_current = True
        #         sign = hashlib.md5(content).hexdigest()
        #         obj.sign = sign
        #         if not obj.save(using=STATICFILE_DB):
        #             return get_result(False, u'文件不能上传到根目录')
        #         key = StaticFile.CACHE_KEY % (obj.name,)
        #         cache.delete(key)
        #         StaticFile.objects.using(STATICFILE_DB).filter(is_active=True, name=obj.name).exclude(
        #             pk=obj.id).update(is_current=False)
        # except Exception as e:
        #     return get_result(False, e.message)

    # 删除临时文件
    # un_delete = []
    # for i in file_dir_list:
    #     try:
    #         file_path = bc_dir + i[2]
    #         os.remove(file_path)
    #     except WindowsError:
    #         if i[2] in os.listdir(bc_dir.strip('/')):
    #             un_delete.append(i[2])
    # if len(un_delete):
    #     return True, u'批量上传成功,{}下临时文件{}未删除'.format(bc_dir.strip('/'), un_delete)
    # else:
    #     return True, u'批量上传成功'


print upload_staticfiles_by_url('/test', 'http://127.0.0.1:9090/jetbrains-agent-latest.zip')

# # 保存临时文件目录
# bc_dir = './test/'
# cs = cStringIO.StringIO(content)
# z_file_list = zipfile.ZipFile(cs, "r")
#
# file_dir_list = []
# for file_dir in z_file_list.namelist():
#     if not file_dir.endswith("/"):
#         file_dir_list.append((pre_dir + '/' + file_dir, file_dir, file_dir.split('/')[-1]))
#
# # 保存临时文件
# for i in file_dir_list:
#     file_dir = bc_dir + i[2]
#     try:
#         with open(file_dir, 'wb+') as f:
#             file_content = z_file_list.read(i[1])
#             f.write(file_content)
#     except IOError:
#         return get_result(False, u'保存临时文件失败')
#
# # 写入数据库
# for i in file_dir_list:
#     with open(bc_dir + i[2], 'rb+') as f:
#         file_content = f.read()
#
#     with transaction.atomic():
#         obj = StaticFile(name=i[0])
#         if file_content is not None:
#             obj.content = file_content
#         obj.is_current = True
#         sign = hashlib.md5(file_content).hexdigest()
#         obj.sign = sign
#         if not obj.save(using=STATICFILE_DB):
#             return get_result(False, u'文件不能上传到根目录')
#         key = StaticFile.CACHE_KEY % (obj.name,)
#         cache.delete(key)
#         StaticFile.objects.using(STATICFILE_DB).filter(is_active=True, name=obj.name).exclude(
#             pk=obj.id).update(is_current=False)
#
# # 删除临时文件
# un_delete = []
# for i in file_dir_list:
#     try:
#         file_path = bc_dir + i[2]
#         os.remove(file_path)
#     except WindowsError:
#         if i[2] in os.listdir(bc_dir.strip('/')):
#             un_delete.append(i[2])
# if len(un_delete):
#     return get_result(True, u'批量上传成功,{}下临时文件{}未删除'.format(bc_dir.strip('/'), un_delete))
# else:
#     return get_result(True, u'批量上传成功')