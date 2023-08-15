import sys
import time
import fitz
from fitz import Font
from bs4 import BeautifulSoup as BS
from client.AIclient import AiClient


def progress_bar(i):
    i = int(i)
    sys.stdout.flush()
    print("\r", end="")
    print("正在翻译: {}%: ".format(i), "▋" * (i // 2), end="\n")
    time.sleep(0.05)


def translate_and_generate_pdf(input_pdf_path, output_pdf_path):
    a = AiClient("https://ai-yyds.com/v1/chat/completions", "sk-N9ILW166aQgt5fQqD668Ec73B14c42FcB06130E4Fe276e1b")
    doc = fitz.open(input_pdf_path)
    output_doc = fitz.open()
    total = 1
    start = 0
    step = 100 / (total - start)
    progress_bar(1)

    for page_num in range(start, total):
        page = doc.load_page(page_num)
        mediabox = page.mediabox
        new_page = output_doc.new_page(width=mediabox.width * 2, height=mediabox.height)

        # Extract text blocks and their positions
        blocks = page.get_text("blocks")
        for block in blocks:
            print(block)
            rect = block[:4]  # Extract coordinates
            block_text = block[4]  # Extract text content
            new_page.insert_textbox(rect=rect,fontsize=11,fontfile='font/simsun.ttc',buffer=block_text)

        # Insert images
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_x = img[0]
            image_y = img[1]
            width = base_image["width"] / 5
            height = base_image["height"] / 5
            image_rect = fitz.Rect(image_x, image_y, image_x + width, image_y + height)
            new_page.insert_image(image_rect, stream=base_image["image"])

        progress_bar(step * (page_num + 1))

    output_doc.save(output_pdf_path)
    output_doc.close()


input_pdf_path = "斯坦福小镇：生成式人类行为交互模拟体.pdf"
output_pdf_path = "output.pdf"
translate_and_generate_pdf(input_pdf_path, output_pdf_path)
