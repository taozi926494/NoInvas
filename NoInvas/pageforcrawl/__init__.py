#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2019-9-27 17:31
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from flask import render_template, Blueprint
from NoInvas import app


page_for_crawl = Blueprint('page_for_crawl', __name__)


@app.route('/page_for_crawl/normal_crawl')
def normal_crawl():
    return render_template('for_normal_crawl.html')
