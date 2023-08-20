import copy
import sys

import fitz

from API.openai.AIclient import AiClient
from API.youdao.TranslateDemo import createRequest
from seting import seting

BaseFontDir = "client/fonts/"


class translateParams(object):
    inPath: str
    outPath: str
    start: int
    end: int
    isAi: bool = 0


class translate:
    def __init__(self):
        self.i = 0
        self.new_page = None
        self.doc = None
        self.ai = None
        self.end = 0
        self.output_doc = None
        self.start = 0
        self.step = 0
        self.c = 0
        self.page = None
        self.parm: translateParams

    def progress_bar(self):
        sys.stdout.flush()
        print("\r", end="")
        print("正在翻译: {}%: ".format(int(self.i)), "▋" * (int(self.i) // 2), end="\n")

    def translate_and_generate_pdf(self, pram: translateParams):
        self.parm = pram
        print(self.parm.isAi)
        if self.parm.isAi == 1:
            print("选择AI翻译")
        elif self.parm.isAi == 0:
            print("选择有道翻译")
        self.ai = AiClient(seting.OpenAiSettings.Url, seting.OpenAiSettings.key)
        self.doc = fitz.open(pram.inPath)
        self.output_doc = fitz.open()
        self.end = pram.end
        self.start = pram.start
        self.step = 100 / (self.end - self.start)
        self.c = self.start
        self.i = 0
        self.progress_bar()
        for page_num in range(self.start, self.end):
            self.c += 1
            self.page = self.doc.load_page(page_num)
            mediabox = self.page.rect
            self.new_page = self.output_doc.new_page(width=mediabox.width, height=mediabox.height)
            self.insert_rect()
            self.insert_image()
            self.insert_text()
            self.i = (self.i + 1) * self.step
            self.progress_bar()
        self.output_doc.save(pram.outPath)
        self.output_doc.close()
        self.doc.close()

    def insert_rect(self):
        for i in self.page.get_drawings(True):
            if i["type"] == "group":
                continue
            temp = copy.deepcopy(i)
            if "items" in temp.keys():
                del temp["items"]
            del temp["type"]
            if "rect" in temp.keys():
                del temp["rect"]
            for j in i["items"]:
                if j[0] == "l":
                    self.drawL(temp, j)
                elif j[0] == 're':
                    self.drawRe(temp, j)
                # elif j[0] == 'c':
                #     drawC(temp, new_page, j)

    def insert_image(self):
        for img in self.page.get_images():
            xref = img[0]
            img_rect = self.page.get_image_bbox(img[7], transform=True)
            base_image = self.doc.extract_image(xref)
            try:
                self.new_page.insert_image(img_rect[0], stream=base_image["image"])
            except Exception as e:
                print(e)

    def insert_text(self):
        blocks = self.page.get_text("dict")
        count = 1
        for i in blocks["blocks"]:
            if "lines" in i:
                pc = 0
                fontsize = 0
                ascender = 0
                text = ""
                color = 0
                expandtabs = 8
                for j in i["lines"]:
                    for k in j["spans"]:
                        pc += 1
                        color += k["color"]
                        fontsize += k["size"]
                        ascender += k["ascender"]
                        text += k["text"]
                        if color > 1:
                            color = 1
                        elif color < 0:
                            color = 0
                        expandtabs = k["flags"]
                basename = "simsun.ttc"
                fontsize /= pc
                ascender /= pc
                color /= pc
                if self.parm.isAi == 1:
                    try:
                        text = u"{}".format(self.ai.getTranslation(text))
                    except Exception as e:
                        raise e
                elif self.parm.isAi == 0:
                    try:
                        text = u"{}".format(createRequest(text))
                    except Exception as e:
                        raise e
                font = "F0"
                self.new_page.insert_textbox(rect=i["bbox"], fill_opacity=ascender, buffer=text,
                                             fontsize=fontsize, expandtabs=expandtabs,
                                             fontfile=BaseFontDir + basename, fontname=font, color=color)
            count += 1

    def drawL(self, temp, j):
        value = copy.deepcopy(temp)
        del value["closePath"]
        del value["layer"]
        del value['seqno']
        del value['level']
        del value['fill']
        del value['even_odd']
        if value['fill_opacity'] is None:
            value['fill_opacity'] = 1
        if value['lineCap'] != 0:
            value['lineCap'] = 0
        if value["stroke_opacity"] is None:
            value["stroke_opacity"] = 1
        if value['color'] is None:
            value['color'] = 0
        if value['width'] is None:
            value['width'] = 1
        if value['lineJoin'] != 0:
            value['lineJoin'] = 0
        self.new_page.draw_line(p1=j[1], p2=j[2], **value)

    def drawRe(self, temp, j):
        value = copy.deepcopy(temp)
        del value['even_odd']
        if 'seqno' in value.keys():
            del value['seqno']
        del value["layer"]
        del value['level']
        del value["closePath"]
        if 'scissor' in value.keys():
            del value['scissor']
        if "stroke_opacity" in value.keys():
            if value["stroke_opacity"] is None:
                value["stroke_opacity"] = 1
        if 'lineCap' in value.keys():
            if value['lineCap'] != 0:
                value['lineCap'] = 0
        if 'lineJoin' in value.keys():
            if value['lineJoin'] != 0:
                value['lineJoin'] = 0
        self.new_page.draw_rect(rect=j[1], **value)

    def drawC(self, temp, j):
        value = copy.deepcopy(temp)
        del value["layer"]
        del value['level']
        del value['even_odd']
        del value["closePath"]
        if 'seqno' in value.keys():
            del value['seqno']
        value["radius"] = 0.1
        if value['fill_opacity'] is None:
            value['fill_opacity'] = 1
        if 'lineCap' in value.keys():
            if value['lineCap'] != 0:
                value['lineCap'] = 0
        if "stroke_opacity" in value.keys():
            if value["stroke_opacity"] is None:
                value["stroke_opacity"] = 1
        if 'lineJoin' in value.keys():
            if value['lineJoin'] != 0:
                value['lineJoin'] = 0
        self.new_page.draw_circle(center=j[1], **value)
