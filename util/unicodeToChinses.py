# encoding: utf-8
import sys

para_list = sys.argv

if len(para_list) == 2:
    help_list = ['--help', '-h', '--h']
    if para_list[1].lower() in help_list:
        print(u"""
# 使用帮助
方法 示例
    python unicodeToChinese.py unicode码
""")
    else:
        s = para_list[1].decode(encoding='unicode_escape', errors='ignore')
        print(s)
elif len(para_list) == 1:
    s = " python unicodeToChinese.py --help"
    s = s.encode(encoding='unicode_escape').decode(encoding='unicode_escape', errors='ignore')
    print(s)
else:
    print(u"错误操作。")
