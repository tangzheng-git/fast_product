#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/17
# file: run.py
# Email:
# Author: 唐政 

from ApiProduct.acquire import para_dict
from ApiProduct.dosing import write


para_dict['app_name'] = 'zlsmart'
para_dict['model_str'] = '配置信息表'
para_dict['user'] = '唐政'

# print()
# for item in para_dict.items():
#     print(item)

write(para_dict)
print('完成')

