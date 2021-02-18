#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/02/04
# file: test.py
# Email:
# Author: 唐政 
# -*- coding: utf-8 -*-
import datetime

import requests
import time
import csv
import pandas as pd

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
  "Cookie": "appmsglist_action_3944211161=card; appmsglist_action_3018314530=card; appmsglist_action_3230269139=card; ua_id=moQauNiEVx1wULjDAAAAAKCtXoU4eJuIk5AxaG5kGD8=; cert=aIj09aWHv8VDLqVM3jlhbswWBVxVSUvv; pgv_info=ssid=s8041013640; pgv_pvid=5286490692; sig=h01cde969a9065a00fbb85692099930e77ba3744bc454449695c782b5a2320b486b0404cc5612f706d3; ptui_loginuin=972631576; uin=o0972631576; skey=@AVXOZovfk; RK=KQT8dFNKWI; ptcz=70262106281b7aa4fab1246f6e98e85f81c7dbf8fe3fd74881b33b7dbf3eec80; master_key=jELG8yXogqW3k9PN4aI/N/1VU/BsG8yav1FY3kisFIg=; media_ticket=121bc542d51d311af160bce0dc9f08f4c7947151; media_ticket_id=3944211161; openid2ticket_oItPns5DRbmzcdwWz3R35xZBwF8s=; mm_lang=zh_CN; uuid=b91935d381350dfff32b9c86eb26ab5b; rand_info=CAESIAtWyYpdLJAYM4kzcQWfhZRUe92Y8iHT8LVAZUE69BHg; slave_bizuin=3230269139; data_bizuin=3230269139; bizuin=3230269139; data_ticket=ii5ULK4e9sfNmfML/geSJwA0klAp4hNag11mOfZsa18yW+iN/eigOUv2NEeClKDz; slave_sid=Q2RYWUd3bDJiQ2c0SmpLWlY4U2VGZUM3NVo4QWMyMWJydWpSVUY2WlJpX1V4RkZyMDhnUWVEV0paRXNoTWhRVkRtczF6WHlRUmtDbVN5ZENWX3ljWmdMVDdwTkdWc29FbWhSU3g5QkphN3RKc0t6TlNycWl6RzQyVWZ5a2YwNzdjcnkwVzhBOHlMcXFvYXdl; slave_user=gh_cafe34fff218; xid=a8f441e3217b918cb8af2873e5472c29; openid2ticket_o0_6JwCdKSuRoy9ASrCTWHN-TYfI=",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

data = {
    "token": "1643033575",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "MzA4NjcyMDU1NQ==",
    "type": "9",
}

content_list = []
for i in range(84, 313):
    data["begin"] = i*5
    time.sleep(30)
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    if content_json.get('app_msg_list', None) is None:
        break
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        dateArray = datetime.datetime.utcfromtimestamp(item["update_time"])
        otherStyleTime = dateArray.strftime("%Y%m%d")
        string = '{} 《{}》'.format(otherStyleTime, item["title"])
        with open('test.txt', mode='a', encoding='utf-8') as filename:
            filename.write(string)
            filename.write('\n')  # 换行
    print(i)
print('结束')
