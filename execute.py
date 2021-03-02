#!/usr/bin/env python
# encoding: utf-8
# Date: 2021/02/22
# file: execute.py
# Email:
# Author: 唐政

from __future__ import print_function
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():

    import os

    os.system('chcp 65001')

    fp = os.popen('netstat -a -b -n -o')

    tcp_list = fp.read().split('\n')[3:-1]

    dic = {
        'TCP': {
            'ESTABLISHED': {
                'NOTE': '已连接',
                'DICT': {
                    'name': {
                        'PID': '',
                        'Local Address': '',
                        'Foreign Address': '',
                    },
                },
                'COUNT': 0,
            }
        },
        'UDP': {

        },

    }

    for tcp in tcp_list:
        print(tcp)


else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        # in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)