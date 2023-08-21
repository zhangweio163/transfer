class FastApiSettings(object):
    inPath = "upload/pdf"
    outPath = "upload/translated"
    zipPath = "upload/zip"


class OpenAiSettings(object):
    Url = ""
    key = ""


class YouDaoSettings(object):
    APP_KEY = ""
    APP_SECRET = ""
    # 要翻译的语言
    lang_from = 'auto'
    lang_to = 'zh-CHS'


class GoogleSettings(object):
    service = ['translate.google.cn', 'translate.google.com']
    src = 'en'
    dest = 'zh-cn'


class BaiduSettings(object):
    # Set your own appid/appkey.
    appid = ''
    appkey = ''

    from_lang = 'en'
    to_lang = 'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
