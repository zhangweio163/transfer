# encoding:utf-8
import json

import requests


class AiClient:
    def __init__(self, url, token):
        self.url = url
        self.body = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "请翻译这个英文hello"
                }
            ],
            "temperature": 0.7
        }
        self.header = {
            "Authorization": "Bearer " + token,
            "Content-Type" : "application/json; charset=utf-8",
            "User-Agent" : "Mozilla/5.0 (Macintosh;)"
        }

    def sendRequest(self, content):
        self.body["messages"][0][
            "content"] = f"""You are a translation api, and when I pass parameters in English, you output them in Chinese.
Now pass in the parameter '{content}'"""
        res = requests.post(url=self.url, data=json.dumps(self.body, sort_keys=False), headers=self.header)
        print(res.json())
        if "errors" in res.json():
            print(res.json()['errors'])
        return res.json()["choices"][0]["message"]["content"]


    def getTranslation(self,content):
        try:
            return self.sendRequest(content)
        except Exception as e:
            print(e)
            return self.getTranslation(content)