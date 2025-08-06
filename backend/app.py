from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from analyzer import analyze_code

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": ""})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file.filename:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "❌ No file selected or invalid filename!"
        })
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": f"✅ File '{file.filename}' uploaded successfully!"
    })

@app.post("/analyze/")
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename:
        return JSONResponse(
            status_code=400,
            content={"error": "No file selected or invalid filename!"}
        )
    
    # Read file content
    content = await file.read()
    try:
        code = content.decode('utf-8')
    except UnicodeDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "File must be a text file with valid UTF-8 encoding!"}
        )
    
    # Analyze the code
    try:
        result = analyze_code(code)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error analyzing code: {str(e)}"}
        )
