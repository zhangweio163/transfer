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
