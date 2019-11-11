#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : blueprint.py
# @Time    : 2019-9-27 17:42
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from NoInvas import restful_api
from NoInvas.pageforcrawl import page_for_crawl
from NoInvas.admin.system import SystemListView, SystemView
from NoInvas.admin.api import ApiListView, ApiView


def regist_router():
    # app.register_blueprint(page_for_crawl)
    restful_api.add_resource(SystemListView, '/admin/system')
    restful_api.add_resource(SystemView, '/admin/system/<sys_id>')

    restful_api.add_resource(ApiListView, '/admin/api')
    restful_api.add_resource(ApiView, '/admin/api/<sys_id>/<api_id>')