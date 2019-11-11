#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : controller.py
# @Time    : 2019-9-28 16:56
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
from flask import Blueprint, request, jsonify
from NoInvas import app
from NoInvas.models import Projects
from NoInvas.utils.params_helper import params_check, param_rule

project_bp = Blueprint('project_bp', __name__)

@app.route('/add_project')
def add_project():
    params_checked = params_check(request.args, [param_rule('api_id'), param_rule('api_name')])
    if not params_checked['pass']:
        return jsonify({
            'status': 400,
            'msg': params_checked['msg']
        })

