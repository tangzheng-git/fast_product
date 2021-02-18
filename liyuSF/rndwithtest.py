#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/14
# file: rndwithtest.py
# Email:
# Author: 唐政 


"""
@check_request_parmes(org_id=("组织id", "r,liyu_organization.Organization__pk"),
                      pre_dir=("父路径", "r"),
                      file_id=("文件id", "r"))
@client_login_required
@check_org_relation()
@check_permissions_and_log(template_name='default_template.html')
def upload_staticfiles_by_fileid(request, org_id, pre_dir, file_id, person):
    import zipfile
    import cStringIO
    import json

    flag, file_obj = get_file_data_by_id(file_id)

    if not flag:
        return get_result(False, file_obj)

    if hasattr(file_obj, 'read'):
        file_read = file_obj.read()
    else:
        file_read = file_obj

    cs = cStringIO.StringIO(file_read)
    z_file_list = zipfile.ZipFile(cs, "r")

    file_name_list = []
    for file_dir in z_file_list.namelist():
        if not file_dir.endswith("/"):
            new_filename = pre_dir + '/' + file_dir

            dir_list = new_filename.strip('/').split('/')
            dir_list.pop()

            if len(dir_list) == 0:
                return get_result(False, u'文件不能上传到根目录')
            file_name_list.append(file_dir)

    file_list = []
    for file_dir in file_name_list:

        if not file_dir.endswith("/"):
            content = z_file_list.read(file_dir)
            sign = hashlib.md5(content).hexdigest()

            new_filename = pre_dir + '/' + file_dir

            dir_list = new_filename.strip('/').split('/')
            dir_list.pop()
            
            parent_id = None

            for i, dir_name in enumerate(dir_list):

                try:
                    obj = StaticDir.objects.get(name=dir_name, parent_id=parent_id, is_active=True)
                except StaticDir.DoesNotExist:
                    obj = StaticDir(name=dir_name)
                    if i != 0:
                        obj.parent_id = parent_id

                    obj.display_name = '/' + dir_name
                    if parent_id is not None:
                        parent = StaticDir.objects.get(pk=parent_id, is_active=True)
                        obj.display_name = parent.display_name + obj.display_name
                        obj.parent_id = parent_id

                    obj.save(using=STATICFILE_DB)

                parent_id = obj.id

            file_type = None
            try:
                json.dumps(content)
            except:
                import base64
                content = base64.b64encode(content)
                file_type = StaticFile.FILE_TYPE_BINARY
            file_list.append(dict(dir_id=parent_id, content=content, sign=sign, new_filename=new_filename, file_type=file_type))

        try:
            with transaction.atomic():
                for file_obj in file_list:
                    obj = StaticFile(name=file_obj['new_filename'])
                    if file_obj['content'] is not None:
                        obj.content = file_obj['content']
                    if file_obj['file_type'] is not None:
                        obj.file_type = file_obj['file_type']
                    obj.is_current = True
                    obj.sign = file_obj['sign']
                    obj.save(using=STATICFILE_DB)
                    key = StaticFile.CACHE_KEY % (obj.name,)
                    cache.delete(key)
                    StaticFile.objects.using(STATICFILE_DB).filter(is_active=True, name=obj.name).exclude(
                        pk=obj.id).update(is_current=False)
        except Exception as e:
            return get_result(False, e.message)

    return get_result(True, u'批量上传成功')
"""
# !/usr/bin/python
# import re
#
# name = "1     "
# try:
#     name_ends = re.match(r'(^[^\s].*)', name).group(1)
# except AttributeError:
#     name_ends = ''
#
#
# print "name_ends : ", name_ends, len(name_ends)


dir_list = ['1']
print ['/' + '/'.join(dir_list[:i + 1]) for i in range(0, len(dir_list))][-1]