import asyncio
import concurrent
import io
import time
from functools import partial
from multiprocessing import Pool
import fastapi
import textract
import shutil
import uvicorn
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File
import base64
from PyPDF2 import PdfFileWriter
from PIL import Image
from threading import Thread
import PyPDF2
from bs4 import BeautifulSoup

import db
from db import get_file
import multiprocessing
import aiofiles
from fastapi.responses import JSONResponse

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

import string
import random
path = r"D:\file"











async def gen_id():
   letters = string.ascii_letters + string.digits

   return ''.join(random.choice(letters) for i in range(32))




async def search_html_in_pdf(file):
    print(file)
    pdf_reader = PyPDF2.PdfReader(file)
    texts = map(lambda page: page.extract_text(), pdf_reader.pages)
    soup = ' '.join(texts)
    return bool(BeautifulSoup(soup, "html.parser").find())





app = fastapi.FastAPI()



@app.get('/')
async def document(id):
    file = await get_file(id)
    return FileResponse(path=rf"{file[0]}", filename=f'{file[1]}')


@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.filename.endswith('pdf'):
        contents = await file.read()
        if contents:
            if not file.size/1024/1024 > 10:
                if not await search_html_in_pdf(io.BytesIO(contents)):
                    id = str(await gen_id())
                    print(path + chr(92) + id + '.pdf')
                    await db.insert_file(file_path=str(path + chr(92) + id + '.pdf'), id=id, name=file.filename)
                    async with aiofiles.open(path + chr(92) + id + '.pdf', 'wb') as f:
                        await f.write(contents)
                    return JSONResponse({'id': id}, status_code=200)
                else:
                    return JSONResponse({'error': 'HTML in file'}, status_code=500)
            else:
                return JSONResponse({'error': 'too much data'}, status_code=500)
        else:
            return JSONResponse({"error": "No pdf"}, status_code=500)
    else:
        JSONResponse({"error": "unsupported file"}, status_code=500)














    # Обработка загруженного файла




if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)