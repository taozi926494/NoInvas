#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2019-9-28 9:02
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from NoInvas import db, app


class Base(db.Model):
    __abstract__ = True
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


from NoInvas.models.system import SystemModel
from NoInvas.models.api import ApiModel


def init_databases():
    db.init_app(app)
    db.create_all()
