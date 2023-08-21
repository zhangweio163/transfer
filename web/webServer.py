import os
import shutil
import time
import uuid
import zipfile

from fastapi import FastAPI, File, UploadFile, Header, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from client.pdfDoler import translate, translateParams
from seting.seting import FastApiSettings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def testTran():
    tra = translate()
    pram = translateParams()
    pram.inPath = "F:\\transfer\client\斯坦福小镇：生成式人类行为交互模拟体.pdf"
    pram.outPath = f"output{time.time()}.pdf"
    pram.start = 0
    pram.end = 2
    tra.translate_and_generate_pdf(pram)


def check_auth(Authorization: str = Header(...)):
    token = Authorization.split()[1]  # Assuming the header is "Bearer <token>"
    if token != "1437213b-6ea4-4007-bce1-c8c91fa1c317":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )


def returnError(error):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error
    )


def removeFile(outPath, inPath):
    try:
        os.remove(outPath)
        os.remove(inPath)
    except Exception:
        pass


def upload_and_translate(token: dict = Depends(check_auth), start: int = 0, end: int = 1, trans: int = 2,
                         file: UploadFile = File(...)):
    if start == end or start > end:
        return {"error": "Invalid query pram. Only start lower than end"}
    if file.filename.endswith('.pdf'):
        input_pdf_path = os.path.join(FastApiSettings.inPath, str(uuid.uuid4()) + file.filename)
        outFilePre = "translated_" + str(uuid.uuid4())
        output_pdf_path = os.path.join(FastApiSettings.outPath, outFilePre + file.filename)
        try:
            tra = translate()
            with open(input_pdf_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            f.close()
            pram = translateParams()
            pram.inPath = input_pdf_path
            pram.outPath = output_pdf_path
            pram.start = start
            pram.end = end
            pram.trans = trans
            tra.translate_and_generate_pdf(pram)

            compressed_file_path = os.path.join(FastApiSettings.zipPath, outFilePre + ".zip")
            zipFile = zipfile.ZipFile(compressed_file_path, 'w')
            zipFile.write(output_pdf_path, outFilePre + file.filename, zipfile.ZIP_DEFLATED)
            zipFile.close()
            removeFile(output_pdf_path, input_pdf_path)
            return FileResponse(compressed_file_path, media_type="application/zip")
        except Exception as e:
            removeFile(output_pdf_path, input_pdf_path)
            returnError(e)
    else:
        returnError("Invalid file format. Only PDF files are allowed.")


@app.post("/upload_and_translate/")
async def upload_and_translate_route(
        token: dict = Depends(check_auth), start: int = 0, end: int = 1, trans: int = 2, file: UploadFile = File(...)
):
    result = upload_and_translate(token, start, end, trans, file)
    return result
