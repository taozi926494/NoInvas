#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : api.py
# @Time    : 2019-11-8 15:02
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from flask import request, jsonify, json

from NoInvas import db
from NoInvas.models import ApiModel
from flask_restful import Resource, abort


class ApiView(Resource):
    def get(self, sys_id, api_id):
        one = ApiModel.query_one(sys_id=sys_id, api_id=api_id)
        if one is None:
            abort(400, message="Api sys_id {} api id {} doesnt exist".format(sys_id, api_id))
        return {'data': one.to_dict()}, 200

    def put(self, sys_id, api_id):
        req_data = json.loads(request.get_data())
        one = ApiModel.query_one(sys_id, api_id)
        if one is None:
            abort(400, message="api is not existed")
        for key in req_data:
            setattr(one, key, req_data[key])
        db.session.commit()
        return {'message': '修改成功'}, 200


class ApiListView(Resource):
    def post(self):
        req_data = json.loads(request.get_data())
        one = ApiModel.query_one(req_data['sys_id'], req_data['api_id'])
        if one is not None:
            abort(400, message='Api is already exist')
        ApiModel.add_one(**req_data)
        return {'message': '上传API成功'}, 200





