import time

import requests

from apidemo.utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '1bc7288509864260'
# 您的应用密钥
APP_SECRET = 'xUGgHsoS7kWNf38CC0GmALAzaMGYHpa8'


def createRequest(content):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    lang_from = 'auto'
    lang_to = 'zh-CHS'

    data = {'q': content, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    try:
        if res.json()["translation"][0] is not None:
            return res.json()["translation"][0]
        else:
            time.sleep(0.5)
            return createRequest(content)
    except Exception as e:
        time.sleep(0.5)
        return createRequest(content)


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
