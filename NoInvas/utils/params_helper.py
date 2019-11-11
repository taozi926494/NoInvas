#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : request_middleware.py
# @Time    : 2019-9-28 17:01
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com


def param_rule(param, required=True, type_func=str):
    return {
        "param": param,
        "required": required,
        "type_func": type_func
    }


def params_check(params, rules):
    """
    检查请求参数
    :param params: 请求参数
    :param rule: 规则
    :return:
    """
    ret = { "pass": True, "msg": "", "params": params.to_dict()}
    for item in rules:
        param = ret["params"].get(item['param'])
        if item['required']:
            if param is None:
                ret['pass'] = False
                ret['msg'] = "Error missing param %s" % item['param']
                return ret
        if param:
            try:
                ret["params"][item['param']] = item['type_func'](param)
            except Exception as err:
                ret['pass'] = False
                ret['msg'] = "TypeError param %s type is incorrect, error_msg: %s" % (item['param'], str(err))
                return ret
    return ret
