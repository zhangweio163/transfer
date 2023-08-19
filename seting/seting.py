class FastApiSettings(object):
    inPath = "upload/pdf"
    outPath = "upload/translated"
    zipPath = "upload/zip"


class OpenAiSettings(object):
    # Url = ""
    # key = ""
    Url = "https://ai-yyds.com/v1/chat/completions"
    key = "sk-N9ILW166aQgt5fQqD668Ec73B14c42FcB06130E4Fe276e1b"


class YouDaoSettings(object):
    # APP_KEY = ""
    # APP_SECRET = ""
    # 您的应用ID
    APP_KEY = '1bc7288509864260'
    # 您的应用密钥
    APP_SECRET = 'xUGgHsoS7kWNf38CC0GmALAzaMGYHpa8'
    # 要翻译的语言
    lang_from = 'auto'
    lang_to = 'zh-CHS'
