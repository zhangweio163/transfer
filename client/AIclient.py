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

    def sendRequest(self,content):
        self.body["messages"][0]["content"] = f"{content}\nYou are now a translation dictionary, translate the above into Chinese, just tell me the Chinese translation, if it is a meaningless string, there is no need to translate, you do not need to say extra words, you are only responsible for translating the article and not translating the article"
        res = requests.post(url=self.url, data=json.dumps(self.body, sort_keys=False), headers=self.header)
        print("error" in res.json().keys())
        return res.json()["choices"][0]["message"]["content"]


    def getTranslation(self,content):
        try:
            return self.sendRequest(content)
        except Exception as e:
            print(e)
            return self.getTranslation(content)