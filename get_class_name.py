#!/usr/bin/env python
# encoding: utf-8
# Date: 2020/12/07
# file: get_class_name.py
# Email:
# Author: 唐政 

import inspect


def get_current_function_name():
    return inspect.stack()[1][3]


class MyClass:
    def function_one(self):
        print("%s.%s invoked" % (self.__class__.__name__, get_current_function_name()))


if __name__ == "__main__":
    myclass = MyClass()
    myclass.function_one()