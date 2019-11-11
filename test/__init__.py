#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2019-9-23 17:54
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com


code = """
def f(g):
    g = 'safdsafdaf'
"""

n = None

exec(code, n)
print(n)