#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/03/02
# file: story_tool.py
# Email:
# Author: 唐政 


import datetime

import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

# 目标url
url = "https://www.mibaoge.com/28_28320/840908.html"

# 使用Cookie，跳过登陆操作
headers = {
  "Cookie": "",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

data = {
}

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
print(len(soup.div.find_all(id="content")))
print(str(soup.div.find_all(id="content")[0]).replace('<br/>', '').replace(' ', '').replace('<div id="content">', ''))

