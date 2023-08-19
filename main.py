import os
import shutil
import time
import uuid
import zipfile

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from client.pdfDoler import translate, translateParams

app = FastAPI()


@app.post("/upload_and_translate/")
async def upload_and_translate(start: int, end: int, file: UploadFile = File(...)):
    if start == end or start > end:
        return {"error": "Invalid query pram. Only start lower than end"}
    if file.filename.endswith('.pdf'):
        input_pdf_path = os.path.join("upload/pdf", str(uuid.uuid4()) + file.filename)
        outFilePre = "translated_" + str(uuid.uuid4())
        output_pdf_path = os.path.join("upload/translated", outFilePre + file.filename)
        tra = translate()
        # 保存上传的文件到upload/pdf目录
        with open(input_pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        f.close()
        pram = translateParams()
        pram.inPath = input_pdf_path
        pram.outPath = output_pdf_path
        pram.start = start
        pram.end = end
        # 调用翻译和生成函数
        tra.translate_and_generate_pdf(pram)

        # 创建压缩文件
        compressed_file_path = os.path.join("upload/zip", outFilePre + ".zip")
        with zipfile.ZipFile(compressed_file_path, 'w') as zipf:
            zipf.write(output_pdf_path, os.path.basename(output_pdf_path))
        zipf.close()
        # 返回生成的PDF文件
        return FileResponse(compressed_file_path, media_type="application/zip")
    else:
        return {"error": "Invalid file format. Only PDF files are allowed."}


def testTran():
    tra = translate()
    pram = translateParams()
    pram.inPath = "F:\\transfer\client\斯坦福小镇：生成式人类行为交互模拟体.pdf"
    pram.outPath = f"output{time.time()}.pdf"
    pram.start = 0
    pram.end = 2
    tra.translate_and_generate_pdf(pram)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
