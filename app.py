from fastapi import FastAPI, UploadFile, File
import shutil
import os
import cv2
import base64

from src.portrait import extract_portrait
from src.ocr import extract_fields
from src.mrz import parse_mrz
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def save_temp_file(file):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return temp_path

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/extract/portrait")
async def portrait(file: UploadFile = File(...)):
    temp_path = save_temp_file(file)
    portrait_img = extract_portrait(temp_path)
    os.remove(temp_path)
    
    if portrait_img is None:
        return {"error": "No face detected"}
    
    _, buffer = cv2.imencode('.png', portrait_img)
    portrait_base64 = base64.b64encode(buffer).decode('utf-8')
    return {"portrait_base64": portrait_base64}

@app.post("/extract/fields")
async def fields(file: UploadFile = File(...)):
    temp_path = save_temp_file(file)
    result = extract_fields(temp_path)
    os.remove(temp_path)
    return result

@app.post("/extract/mrz")
async def mrz(file: UploadFile = File(...)):
    temp_path = save_temp_file(file)
    result = parse_mrz(temp_path)
    os.remove(temp_path)
    
    if result is None:
        return {"error": "No MRZ found"}
    return result