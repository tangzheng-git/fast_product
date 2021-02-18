#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/13
# file: filetest.py
# Email:
# Author: 唐政 




def auto_download_install_pc_data_by_url(url, md5):
    """
    自动上抛erp数据txm_su
    :return:
    """
    import requests
    import hashlib
    res = requests.get(url=url)
    if res.status_code != 200:
        from util.tools import send_sentry_message
        send_sentry_message(u'自动根据url下载更新记录，失败')
        return
    if md5:
        sign = hashlib.md5(res.content).hexdigest()
        if md5 != sign:
            from util.tools import send_sentry_message
            send_sentry_message(u'下载的文件指纹不对（%s:%s）' % (md5, sign))
            return

    import zipfile
    import json
    import cStringIO

    cs = cStringIO.StringIO(res.content)
    pre_dir = "pc/www/"

    z = zipfile.ZipFile(cs, "r")

    for filename in z.namelist():
        if not filename.endswith("sf_config.txt"):
            continue
        content = z.read(filename)
        try:
            arr = content.split("\n")
            if arr:
                pre_dir = arr[0].strip()
        except:
            pass

    import hashlib
    oldnames = []
    names = []
    for filename in z.namelist():
        if filename.endswith("/"):
            continue
        new_filename = "%s%s" % (pre_dir, filename)
        names.append(new_filename)
        oldnames.append(filename)

    num = 0
    while num < 3:

        class sf_api:
            def query_static_file_info_list(self, string):
                self.str = string
                pass

        success, status, res_json = sf_api.query_static_file_info_list(names=",".join(names))
        if success and res_json.get("success"):
            l = res_json.get("result", {}).get("list")

            f_dict = {x.get("name"): x.get("sign") for x in l}
            f_id_dict = {x.get("name"): x.get("id") for x in l}

            data_json = []
            for filename in z.namelist():
                if filename not in oldnames:
                    continue
                content = z.read(filename)
                sign = hashlib.md5(content).hexdigest()
                new_filename = "%s%s" % (pre_dir, filename)

                need_add = False
                if new_filename in f_dict:
                    if f_dict[new_filename] != sign:
                        need_add = True
                    else:
                        need_add = False
                else:
                    need_add = True
                if need_add:
                    print(new_filename)
                    json_obj = {"pk": f_id_dict.get(new_filename), "name": new_filename, "content": content}
                    try:
                        json.dumps(json_obj)
                    except:
                        import base64
                        json_obj['content'] = base64.b64encode(content)
                        json_obj['type'] = "base64"
                    data_json.append(json_obj)

            step = 40
            post_list = [data_json[x:x + step] for x in [i for i in range(0, len(data_json), step)]]

            success_upload = True
            for data_json_list in post_list:
                success, status, res_json = sf_api.create_staticfile_by_api(data_json=json.dumps(data_json_list))

                if not success or not res_json.get("success"):
                    success_upload = False
            if success_upload:
                break
        num += 1
