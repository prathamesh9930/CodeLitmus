@echo off
echo Starting CodeLitmus Server...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting server at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000