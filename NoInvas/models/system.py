#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : sys.py
# @Time    : 2019-9-28 17:08
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from NoInvas.models import db, Base
from NoInvas.models.api import ApiModel
from typing import List, Dict


class SystemModel(Base):
    sys_id = db.Column(db.String, primary_key=True)  # , comment="系统id")
    sys_name = db.Column(db.String)  # , comment="系统名")
    sys_desc = db.Column(db.String)  # , comment="系统描述")
    sys_img = db.Column(db.String)  # , comment="系统图片")
    su_account = db.Column(db.String)  # , comment="系统超级权限用户账号")
    su_password = db.Column(db.String)  # , comment="系统超级权限用户密码")

    def to_dict(self) -> Dict:
        return dict(
            sys_id=self.sys_id,
            sys_name=self.sys_name,
            sys_desc=self.sys_desc,
            sys_img=self.sys_img,
            su_account=self.su_account,
            su_password=self.su_password,
            update_time=self.date_modified.strftime("%Y-%m-%d %H:%S:%M"),
            insert_time=self.date_created.strftime("%Y-%m-%d %H:%S:%M")
        )

    @classmethod
    def query_one(cls, sys_id: str) -> "SystemModel":
        return cls.query.filter_by(sys_id=sys_id).scalar()

    @classmethod
    def add_one(cls, sys_id: str, sys_name: str, sys_desc: str, sys_img: str, su_account: str, su_password: str):
        one = cls()
        one.sys_id = sys_id
        one.sys_name = sys_name
        one.sys_desc = sys_desc
        one.sys_img = sys_img
        one.su_account = su_account
        one.su_password = su_password

        db.session.add(one)
        db.session.commit()

    @classmethod
    def query_all(cls) -> List["Dict"]:
        sys_list = cls.query.all()
        api_list = ApiModel.query_all()

        res = []
        for sys in sys_list:
            sys_dict = sys.to_dict()
            sys_dict['api_count'] = 0
            sys_dict['normal_api'] = 0
            sys_dict['error_api'] = 0
            for api in api_list:
                if api.sys_id == sys.sys_id:
                    sys_dict['api_count'] += 1
                    if api.running_status == 1:
                        sys_dict['normal_api'] += 1
                    else:
                        sys_dict['error_api'] += 1
            res.append(sys_dict)
        return res
