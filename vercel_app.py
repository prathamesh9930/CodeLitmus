from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import after adding to path
try:
    from analyzer import analyze_code
except ImportError:
    # Fallback import
    sys.path.append('backend')
    from analyzer import analyze_code

from mangum import Mangum

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple path handling for Vercel
templates = None
try:
    # Check if backend directory exists
    if os.path.exists("backend/static"):
        app.mount("/static", StaticFiles(directory="backend/static"), name="static")
    else:
        print("Static directory not found")
    
    if os.path.exists("backend/templates"):
        templates = Jinja2Templates(directory="backend/templates")
    else:
        print("Templates directory not found")
        # Try alternative path
        templates = Jinja2Templates(directory="./backend/templates")
except Exception as e:
    print(f"Error mounting static files: {e}")
    # Fallback
    try:
        templates = Jinja2Templates(directory="./backend/templates")
    except:
        templates = None

# Create uploads directory
os.makedirs("backend/uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("<h1>CodeLitmus</h1><p>Templates not found. Please check deployment.</p>")

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

# Vercel handler
handler = Mangum(app)
