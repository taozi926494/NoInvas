#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : browserdriver.py
# @Time    : 2019-9-23 8:44
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
import pyppeteer.connection


def patch_pyppeteer():
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)
    pyppeteer.connection.websockets.client.connect = new_method
