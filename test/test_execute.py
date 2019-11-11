#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : execute_test.py
# @Time    : 2019-9-25 0:54
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
import pytest
import requests
from lxml import etree

# from NoInvas import app
# from NoInvas import config

from NoInvas.models import Interfaces


def test_execute_python_str():
    func_str = r"""
def interface_function():
    res = requests.get('http://localhost:5000/page_for_crawl/normal_crawl')
    tree = etree.HTML(res.text)
    result = tree.xpath('*//div[@class="data"]//li')
    text = ','.join([x.text.strip() for x in result])
    return text
    """

    loc = locals()
    exec(func_str)
    interface_function = loc['interface_function']
    retval = interface_function()
    assert retval == '1,2,3'


def test_execute_from_db():
    one = Interfaces.query_one(project_name='test_project', interface_name='test_interface_normal')
    loc = locals()
    exec(one.code)
    interface_function = loc['interface_function']
    retval = interface_function()
    assert retval == '1,2,3'
