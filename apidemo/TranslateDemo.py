import time

import requests

from apidemo.utils.AuthV3Util import addAuthParams
from seting.seting import YouDaoSettings


def createRequest(content):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    data = {'q': content, 'from': YouDaoSettings.lang_from, 'to': YouDaoSettings.lang_to}

    addAuthParams(YouDaoSettings.APP_KEY, YouDaoSettings.APP_SECRET, data)

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
