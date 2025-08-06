# CodeLitmus - Code Quality Analyzer 🧪

A web application that analyzes code quality using various metrics and provides feedback in a "litmus test" style format.

## Features

- **File Upload**: Upload code files for storage
- **Code Analysis**: Analyze code quality using:
  - Cyclomatic Complexity
  - Maintainability Index
  - Comment Coverage
- **Interactive UI**: Clean, modern interface with tabbed navigation
- **Real-time Results**: Get instant feedback on code quality

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the application**:
   Open your browser and go to: `http://localhost:8000`

## Usage

### Upload Files
1. Click on the "📁 Upload File" tab
2. Select a file from your computer
3. Click "Upload" to store the file

### Analyze Code
1. Click on the "🔍 Analyze Code" tab
2. Select a code file (supports .py, .js, .ts, .java, .cpp, .c, .cs)
3. Click "Analyze Code"
4. View the results:
   - **Basic**: Good code quality (green)
   - **Neutral**: Average code quality (orange)
   - **Acidic**: Poor code quality (red)

## Project Structure

```
CodeLitmus/
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── analyzer.py         # Code analysis logic
│   ├── utils.py           # Utility functions (empty)
│   ├── requirements.txt   # Python dependencies
│   ├── static/           # CSS and static files
│   ├── templates/        # HTML templates
│   └── uploads/          # Uploaded files directory
└── frontend/             # Original frontend files (legacy)
```

## API Endpoints

- `GET /`: Home page with upload and analysis interface
- `POST /upload`: Upload a file
- `POST /analyze/`: Analyze code quality of uploaded file

## Code Quality Metrics

1. **Cyclomatic Complexity**: Measures code complexity
2. **Maintainability Index**: Overall maintainability score
3. **Comment Coverage**: Ratio of comments to code lines

## Development

To run in development mode with auto-reload:
```bash
uvicorn app:app --reload
```

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Uvicorn**: ASGI server
- **Jinja2**: Template engine
- **Radon**: Code metrics analysis
- **python-multipart**: File upload support
