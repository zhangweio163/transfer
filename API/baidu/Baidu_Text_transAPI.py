# -*- coding: utf-8 -*-
import random
from hashlib import md5

import requests

from seting.seting import BaiduSettings


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate(content):
    salt = random.randint(32768, 65536)
    sign = make_md5(BaiduSettings.appid + content + str(salt) + BaiduSettings.appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': BaiduSettings.appid, 'q': content, 'from': BaiduSettings.from_lang, 'to': BaiduSettings.to_lang,
               'salt': salt, 'sign': sign}
    # Send request
    r = requests.post(BaiduSettings.url, params=payload, headers=headers)
    result = r.json()
    return result["trans_result"][0]["dst"]
