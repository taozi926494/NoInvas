#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : project.py
# @Time    : 2019-11-8 14:15
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from flask import Blueprint, request, jsonify, json
from NoInvas.models import SystemModel, ApiModel
from flask_restful import Resource, abort


class SystemView(Resource):
    def get(self, sys_id):
        one = SystemModel.query_one(sys_id=sys_id)
        if one is None:
            abort(400, message="System {} doesnt exist".format(sys_id))
        res = one.to_dict()
        res['api_list'] = []
        api_list = ApiModel.query_by_sys(one.sys_id)
        for api in api_list:
            res['api_list'].append(api.to_dict())

        return {'data': res}, 200


class SystemListView(Resource):
    def get(self):
        return {"data": SystemModel.query_all()}, 200

    def post(self):
        req_data = json.loads(request.get_data())
        SystemModel.add_one(sys_id=req_data.get('sys_id'),
                       sys_name=req_data.get('sys_name'),
                       sys_desc=req_data.get('sys_desc', ''),
                       sys_img=req_data.get('sys_img', ''),
                       su_account=req_data.get('su_account', ''),
                       su_password=req_data.get('su_password', ''))
        return {'message': '新建系统成功'}, 200


