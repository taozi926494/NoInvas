#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : interfaces.py
# @Time    : 2019-9-28 17:14
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from NoInvas.models import db, Base
from typing import List, Dict


class ApiModel(Base):
    api_id = db.Column(db.String, primary_key=True)  # , comment="接口id")
    sys_id = db.Column(db.String, primary_key=True)  # , comment="系统id")
    api_name = db.Column(db.String)  # , comment="接口名称")
    api_url = db.Column(db.String)  # , comment="api地址"
    api_desc = db.Column(db.String, default='')  # , comment="接口描述")
    api_script = db.Column(db.Text)  # , comment="接口代码")
    driver_type = db.Column(db.SmallInteger, default=0)  # , comment="请求驱动类型 0:常规请求 1:无头浏览器请求")
    login_require = db.Column(db.SmallInteger, default=0)  # , comment="是否需要登录 0:不需要 1:需要")
    req_type = db.Column(db.SmallInteger, default=0)  # , comment="请求类型 0:GET 1:POST")
    get_params = db.Column(db.Text, default='')  # , comment="GET请求参数")
    post_params = db.Column(db.Text, default='')  # , comment="POST请求参数")
    res_type = db.Column(db.SmallInteger, default=0)  # , comment="返回类型 0:json 1: xml")
    res_data = db.Column(db.Text, default='')  # , comment="返回数据")
    running_status = db.Column(db.SmallInteger, default=1)  # , comment="接口运行状态 1:正常 0:异常")
    using_status = db.Column(db.SmallInteger, default=1)  # , comment="接口启用状态 1:启用 0:停用")
    call_times = db.Column(db.Integer, default=0)  # , comment="接口调用次数")

    def to_dict(self):
        return dict(api_id=self.api_id,
                    sys_id=self.sys_id,
                    api_name=self.api_name,
                    api_url=self.api_url,
                    api_desc=self.api_desc,
                    api_script=self.api_script,
                    driver_type=self.driver_type,
                    login_require=self.login_require,
                    req_type=self.req_type,
                    get_params=self.get_params,
                    post_params=self.post_params,
                    res_type=self.res_type,
                    res_data=self.res_data,
                    running_status=self.running_status,
                    using_status=self.using_status,
                    call_times=self.call_times,
                    update_time=self.date_modified.strftime("%Y-%m-%d %H:%S:%M"),
                    insert_time=self.date_created.strftime("%Y-%m-%d %H:%S:%M")
                    )

    @classmethod
    def query_all(cls) -> List["ApiModel"]:
        return cls.query.all()

    @classmethod
    def query_by_sys(cls, sys_id)->List["ApiModel"]:
        return cls.query.filter(cls.sys_id == sys_id).all()

    @classmethod
    def query_one(cls, sys_id: str, api_id: str) -> "ApiModel":
        return cls.query.filter(cls.sys_id == sys_id, cls.api_id == api_id).first()

    @classmethod
    def check_params(cls, **kwargs):
        ret = {'status': True, 'msg': 'ok'}
        if kwargs.get('sys_id') is None or kwargs.get('name') is None:
            ret['status'] = False
            ret['message'] = 'missing params sys_id or name'
        return ret

    @classmethod
    def add_one(cls, **kwargs):
        one = cls()
        for key in kwargs:
            setattr(one, key, kwargs[key])

        db.session.add(one)
        db.session.commit()
