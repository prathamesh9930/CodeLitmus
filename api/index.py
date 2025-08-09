from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from mangum import Mangum
import re

app = FastAPI()

# Simplified analyzer - embedded directly in the file
def analyze_code_simple(code: str) -> dict:
    """Simple code analysis without external dependencies"""
    if not code.strip():
        return {
            "verdict": "Acidic",
            "verdict_explanation": "Code file is empty or contains only whitespace.",
            "score": 0,
            "feedback": ["Empty or whitespace-only code provided."]
        }
    
    score = 5  # Base score
    feedback = []
    
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith('#')]
    
    # Check code length
    if len(non_empty_lines) < 5:
        feedback.append("Code is very short. Consider adding more functionality.")
        score -= 1
    elif len(non_empty_lines) > 50:
        feedback.append("Code is quite long. Consider breaking it into smaller functions.")
        score -= 1
    else:
        feedback.append("Good code length.")
        score += 1
    
    # Check for comments
    comment_ratio = len(comment_lines) / max(len(non_empty_lines), 1)
    if comment_ratio > 0.1:
        feedback.append("Good use of comments for documentation.")
        score += 1
    else:
        feedback.append("Consider adding more comments to explain your code.")
        score -= 1
    
    # Check for functions
    function_count = len(re.findall(r'def\s+\w+', code))
    if function_count > 0:
        feedback.append(f"Good use of functions ({function_count} found).")
        score += 1
    else:
        feedback.append("Consider organizing code into functions.")
        score -= 1
    
    # Check for classes
    class_count = len(re.findall(r'class\s+\w+', code))
    if class_count > 0:
        feedback.append(f"Good use of classes ({class_count} found).")
        score += 1
    
    # Determine verdict
    if score >= 7:
        verdict = "Basic"
        verdict_explanation = "Your code shows good practices and structure."
    elif score >= 4:
        verdict = "Neutral"
        verdict_explanation = "Your code is acceptable but has room for improvement."
    else:
        verdict = "Acidic"
        verdict_explanation = "Your code needs significant improvement in structure and practices."
    
    return {
        "verdict": verdict,
        "verdict_explanation": verdict_explanation,
        "score": max(0, min(10, score)),
        "feedback": feedback
    }

@app.get("/")
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodeLitmus - Code Quality Analyzer</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white;
                min-height: 100vh;
            }
            .container { 
                max-width: 900px; 
                margin: 0 auto; 
                text-align: center; 
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.2em;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .upload-area { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 15px; 
                margin: 30px 0; 
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            textarea { 
                width: 100%; 
                height: 250px; 
                padding: 15px; 
                border-radius: 8px; 
                border: none; 
                font-family: 'Courier New', monospace;
                font-size: 14px;
                resize: vertical;
            }
            button { 
                background: linear-gradient(45deg, #ff6b6b, #ff8e8e); 
                color: white; 
                padding: 15px 40px; 
                border: none; 
                border-radius: 8px; 
                font-size: 18px; 
                cursor: pointer;
                margin-top: 20px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(255,107,107,0.4);
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255,107,107,0.6);
            }
            .result { 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                margin: 30px 0; 
                text-align: left;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            .verdict {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 15px;
            }
            .score {
                font-size: 1.5em;
                margin-bottom: 20px;
            }
            .feedback ul {
                list-style: none;
                padding: 0;
            }
            .feedback li {
                background: rgba(255,255,255,0.1);
                margin: 8px 0;
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid #ff6b6b;
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 1s ease-in-out infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 CodeLitmus</h1>
            <p class="subtitle">Advanced Code Quality Analyzer</p>
            
            <div class="upload-area">
                <h3>📝 Paste your Python code for analysis:</h3>
                <textarea id="codeInput" placeholder="# Paste your Python code here...
def example_function():
    '''This is an example function'''
    return 'Hello, CodeLitmus!'

class ExampleClass:
    def __init__(self):
        self.value = 42
        
    def get_value(self):
        return self.value"></textarea>
                <br>
                <button onclick="analyzeCode()">🔍 Analyze Code Quality</button>
            </div>
            
            <div id="result" class="result" style="display:none;">
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
                    resultContent.innerHTML = '<div class="loading"></div> Analyzing your code...';
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
                            <div class="verdict">🎯 Verdict: ${result.verdict}</div>
                            <div class="score">📊 Score: ${result.score}/10</div>
                            <p><strong>Analysis:</strong> ${result.verdict_explanation}</p>
                            <div class="feedback">
                                <h4>💡 Detailed Feedback:</h4>
                                <ul>
                                    ${result.feedback.map(f => `<li>• ${f}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    } else {
                        resultContent.innerHTML = `<p style="color: #ff6b6b;">❌ Error: ${result.error}</p>`;
                    }
                } catch (error) {
                    resultContent.innerHTML = `<p style="color: #ff6b6b;">❌ Error: ${error.message}</p>`;
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
    
    # Analyze the code using our embedded analyzer
    try:
        result = analyze_code_simple(code)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error analyzing code: {str(e)}"}
        )

# Vercel handler
handler = Mangum(app)
