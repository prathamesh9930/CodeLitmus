from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from mangum import Mangum
import os
import sys

# Simple approach: add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the analyzer directly
import backend.analyzer as analyzer

app = FastAPI()

@app.get("/")
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodeLitmus - Code Quality Analyzer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            .upload-area { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; margin: 20px 0; }
            textarea { width: 100%; height: 200px; padding: 10px; border-radius: 5px; border: none; }
            button { background: #ff6b6b; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
            button:hover { background: #ff5252; }
            .result { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; text-align: left; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 CodeLitmus - Code Quality Analyzer</h1>
            <p>Analyze your Python code for complexity, maintainability, and quality metrics</p>
            
            <div class="upload-area">
                <h3>Paste your Python code:</h3>
                <textarea id="codeInput" placeholder="# Paste your Python code here..."></textarea>
                <br><br>
                <button onclick="analyzeCode()">🔍 Analyze Code</button>
            </div>
            
            <div id="result" class="result" style="display:none;">
                <h3>Analysis Result:</h3>
                <div id="resultContent"></div>
            </div>
        </div>
        
        <script>
            async function analyzeCode() {
                const code = document.getElementById('codeInput').value;
                if (!code.trim()) {
                    alert('Please enter some code to analyze!');
                    return;
                }
                
                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');
                
                try {
                    resultContent.innerHTML = 'Analyzing...';
                    resultDiv.style.display = 'block';
                    
                    const formData = new FormData();
                    const blob = new Blob([code], { type: 'text/plain' });
                    formData.append('file', blob, 'code.py');
                    
                    const response = await fetch('/analyze/', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        resultContent.innerHTML = `
                            <h4>🎯 Verdict: ${result.verdict}</h4>
                            <p><strong>Score:</strong> ${result.score}/10</p>
                            <p><strong>Explanation:</strong> ${result.verdict_explanation}</p>
                            <h4>💡 Feedback:</h4>
                            <ul>
                                ${result.feedback.map(f => `<li>${f}</li>`).join('')}
                            </ul>
                        `;
                    } else {
                        resultContent.innerHTML = `<p style="color: #ff6b6b;">Error: ${result.error}</p>`;
                    }
                } catch (error) {
                    resultContent.innerHTML = `<p style="color: #ff6b6b;">Error: ${error.message}</p>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
        result = analyzer.analyze_code(code)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error analyzing code: {str(e)}"}
        )

# Vercel handler
handler = Mangum(app)
