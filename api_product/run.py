#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/11/17
# file: run.py
# Email:
# Author: 唐政 

from api_product.acquire import para_dict
from api_product.acquire import write


para_dict['app_name'] = 'zlsmart'
para_dict['model_str'] = '基础元素含量'
para_dict['user'] = '唐政'

write(para_dict)