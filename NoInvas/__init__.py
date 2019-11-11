#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2019-9-23 17:16
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Time    : 2019-9-23 8:37
# @Software: PyCharm
# @Author  : Taoz
# @contact : 371956576@qq.com

# ----------------------------------------------
import os
import pyppeteer
import requests
from lxml import etree
import asyncio
from flask_sqlalchemy import SQLAlchemy
# ----------------------------------------------

from flask import Flask, render_template, request, jsonify, json
from flask_cors import CORS
import flask_restful
from NoInvas.utils.browserdriver import patch_pyppeteer
from NoInvas import config
from urllib.parse import quote


patch_pyppeteer()
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)
restful_api = flask_restful.Api(app)

database_url = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'NoInvas.db')
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=database_url,
))
db = SQLAlchemy(app, session_options=dict(autocommit=False, autoflush=True))

loop = asyncio.get_event_loop()


async def init_browser():
    return await pyppeteer.launch({
        # "headless": False,
        "headless": True,
        "args": ['--window-size=1280,800']
    })

browser = loop.run_until_complete(init_browser())


def create_page(browser_, loop_):
    async def new_page():
        return await browser_.newPage()
    return loop_.run_until_complete(new_page())


# func_str = r"""
# def interface_function():
#     res = requests.get('http://www.shanghai.gov.cn/nw2/nw2314/nw2319/nw12344/u26aw62708.html')
#     res.encoding = 'gbk'
#     # print(res.text)
#     tree = etree.HTML(res.text)
#     result = tree.xpath('*//div[@id="ivs_content"]/p')
#     text = '\n'.join([x.text for x in result])
#     return text.encode(encoding='UTF-8').decode()
# result = interface_function()
# """
#
# login_str = """
# async def interface_function(page):
#     await page.goto('http://172.16.119.13/dgps/#/')
#     await page.waitForXPath('*//div[text()="用户登录"]')
#     await page.waitFor(500)
#     # 账号
#     await page.type('input:nth-child(1)', 'admin')
#     # 密码
#     await page.type('div input[type="password"]', 'admin')
#     # 验证码
#     await page.type('div input:nth-child(2)', 'admin')
#     loginbtn = await page.xpath('*//div[text()="登录"]')
#     await loginbtn[0].click()
# """


@app.route('/execute')
def execute():
    # page = create_page(browser, loop)
    # loc = locals()
    # exec(login_str)
    # interface_function = loc['interface_function']
    # loop.run_until_complete(interface_function(page))
    # return jsonify({"data": 0})
    page = int(request.args.get('page'))
    base_url = 'http://kjt.henan.gov.cn/kjjhglzd/index.html'
    base_url_recursive = 'http://kjt.henan.gov.cn/kjjhglzd/index{}.html'
    if page == 1:
        url = base_url
    else:
        url = base_url_recursive.format(page)
    func_str = r"""
def interface_function():
    res = requests.get('{}')
    res.encoding = 'gbk'
    print('res', res)
    tree = etree.HTML(res.text)
    title = tree.xpath('*//div[@class="list3_u1"]//a/font/text()')
    time = tree.xpath('*//div[@class="list3_u1"]//li/span/text()')
    result= []
    for x, y in zip(title, time):
        item = dict()
        item['name'] = x
        item['time'] = y
        result.append(item)
    return result
    """.format(url)
    loc = locals()
    exec(func_str)
    interface_function = loc['interface_function']
    result = interface_function()
    return jsonify({"data": result})


@app.route('/search')
def search():
    page = int(request.args.get('page'))
    keyword = request.args.get('keyword')
    keyword = quote(keyword, encoding='gbk', errors='replace')
    submit = quote("搜索", encoding='gbk', errors='replace')
    base_url = 'http://hnkjt.gov.cn:8080//search.do?rows=110&keyword={}&method=search&Submit1={}&page={}'.format(keyword, submit, page)

    func_str = r"""
def interface_function():
    res = requests.get("{}")
    res.encoding = 'gbk'
    tree = etree.HTML(res.text)
    title = tree.xpath('//td[@class="ssbt"]//a/text()')
    url = tree.xpath('//td[@class="ssbt"]//a/@href')
    result= []
    for x, y in zip(title, url):
        item = dict()
        item['name'] = x
        item['url'] = y
        result.append(item)
    return result
    """.format(base_url)
    loc = locals()
    exec(func_str)
    interface_function = loc['interface_function']
    result = interface_function()
    return jsonify({"data": result})




from NoInvas.models import init_databases, ApiModel
from NoInvas.router import regist_router


@app.route('/apiv1', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    get_params = request.args
    post_params = {}
    if request.get_data():
        post_params = json.loads(request.get_data())

    sys_id = get_params['_sys_id']
    api_id = get_params['_api_id']
    if not sys_id or not api_id:
        flask_restful.abort(400, message="Missing params __sys_id or __api_id")
    api_ins = ApiModel.query_one(sys_id=sys_id, api_id=api_id)
    loc = locals()
    exec(api_ins.api_script)
    api_function = loc['api_function']
    result = api_function(api_ins.api_url, get_params, post_params)
    return jsonify({"data": result})

def run_app():
    regist_router()
    init_databases()
    app.run(debug=True)
    # app.run(debug=True, port=config.app_port)
