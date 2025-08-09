<div align="center">

# 🧪 **CodeLitmus** 
## *Advanced Code Quality Analyzer*

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&width=600&lines=🚀+Analyze+Code+Quality;✨+Beautiful+Animations;📊+Detailed+Metrics;🌐+Live+Demo+Available!" alt="Typing SVG" />

[![Live Demo](https://img.shields.io/badge/🌐_LIVE_DEMO-Try_Now!-FF6B6B?style=for-the-badge&logoColor=white)](https://codelitmus.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-View_Source-181717?style=for-the-badge&logo=github)](https://github.com/prathamesh9930/CodeLitmus)

![CodeLitmus Banner](https://img.shields.io/badge/CodeLitmus-Code%20Quality%20Analyzer-4ECDC4?style=for-the-badge&logo=python&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Render](https://img.shields.io/badge/Hosted_on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-FFC107?style=flat-square)](LICENSE)

</div>

---

## 🎯 **What is CodeLitmus?**

**CodeLitmus** is a beautiful, modern web application that analyzes your code quality with stunning visualizations and comprehensive metrics. Built with **FastAPI** and featuring gorgeous animations, it makes code analysis both powerful and enjoyable!

---

## 🚀 **✨ LIVE DEMO - Try It Now!**

<div align="center">

### **🌟 No Installation Required - Just Click & Analyze!**

[![Launch Live Demo](https://img.shields.io/badge/🚀_LAUNCH_LIVE_DEMO-codelitmus.onrender.com-FF6B6B?style=for-the-badge&logoColor=white&logo=rocket)](https://codelitmus.onrender.com)

**💡 Experience the full power of CodeLitmus instantly!**

🎨 **Beautiful Gradient Animations** • 📱 **Mobile Responsive** • ⚡ **Lightning Fast Analysis**

</div>

---

## ✨ **Features That Make CodeLitmus Special**

<table>
<tr>
<td width="50%">

### 🎯 **Core Functionality**
- 🔍 **Multi-Language Support** - Python, JavaScript, TypeScript, Java, C++, C, C#
- 📊 **Comprehensive Metrics** - Cyclomatic complexity, maintainability index
- 🏆 **Smart Verdict System** - Clear ratings with detailed explanations
- 📈 **Visual Progress Indicators** - Beautiful progress bars and feedback

</td>
<td width="50%">

### 🎨 **Modern UI/UX**
- 🌈 **Gradient Animations** - Eye-catching rainbow effects
- 🌙 **Dark/Light Mode** - Seamless theme switching
- 📱 **Responsive Design** - Perfect on all devices
- 🎭 **Interactive Animations** - Hover effects and smooth transitions

</td>
</tr>
</table>

### 🚀 **Advanced Features**
- 📄 **PDF Report Generation** - Download comprehensive analysis reports
- 📂 **Drag & Drop Upload** - Intuitive file upload with progress tracking
- ⚡ **Real-time Analysis** - Instant feedback with loading animations
- 🎨 **Glassmorphism Design** - Modern aesthetic with backdrop blur effects

---

## 🖼️ **Screenshots**

<div align="center">

### 🌟 **Main Interface**
*Beautiful gradient background with floating animations*

### 📊 **Analysis Results** 
*Comprehensive metrics with visual progress indicators*

### 📱 **Mobile Experience**
*Perfectly responsive design for all devices*

</div>

---

## 🛠️ **Quick Installation**

### **Prerequisites**
- Python 3.8+
- pip (Python package installer)

### **🚀 Get Started in 30 Seconds**

```bash
# 1️⃣ Clone the repository
git clone https://github.com/prathamesh9930/CodeLitmus.git
cd CodeLitmus

# 2️⃣ Navigate to backend
cd backend

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Launch the app
python app.py

# 5️⃣ Open browser → http://localhost:8000
```

### **🐳 Docker Setup (Optional)**

```bash
# Build and run with Docker
docker build -t codelitmus .
docker run -p 8000:8000 codelitmus
```

---

## 🏗️ **Project Architecture**

```
CodeLitmus/
├── 🔧 backend/
│   ├── 📱 app.py                 # FastAPI main application
│   ├── 🧠 analyzer.py            # Core analysis engine
│   ├── 📋 requirements.txt       # Python dependencies
│   ├── 🎨 static/
│   │   └── style.css            # Beautiful animations & styling
│   ├── 🖼️ templates/
│   │   └── index.html           # Modern responsive interface
│   └── 📁 uploads/              # File storage directory
├── 🌐 render.yaml               # Render deployment config
├── ⚡ start.sh                  # Render startup script
├── 📸 screenshots/              # Project screenshots
└── 📖 README.md                 # This file
```

---

## 📊 **API Reference**

### **Upload & Analyze Endpoint**

```http
POST /analyze/
Content-Type: multipart/form-data

Parameters:
- file: Upload file (Python, JS, TS, Java, C++, C, C#)

Response:
{
  "verdict": "Excellent",
  "score": 8.5,
  "complexity": 3.2,
  "maintainability": 85.4,
  "comments": 15.8,
  "verdict_explanation": "Your code demonstrates excellent quality...",
  "feedback": ["Use more descriptive variable names", "..."]
}
```

---

## 📊 **Quality Metrics Explained**

<div align="center">

| Metric | Scale | Target | Description |
|--------|-------|--------|-------------|
| **🔄 Cyclomatic Complexity** | 1-5 (Simple) \| 6-10 (Moderate) \| 11+ (Complex) | < 5 | Decision points and code paths |
| **🔧 Maintainability Index** | 0-49 (Poor) \| 50-69 (Average) \| 70-100 (Excellent) | > 70 | Overall code maintainability |
| **💬 Comment Coverage** | <10% (Poor) \| 10-20% (Good) \| >20% (Excellent) | > 10% | Documentation quality |

</div>

---

## 🌐 **Live Deployment**

### 🚀 **Production Instance**

**🔗 Live URL:** [https://codelitmus.onrender.com](https://codelitmus.onrender.com)

### ⚡ **Deployment Features**
- ✅ **Free Hosting** - Powered by Render's free tier
- ✅ **Auto-Deploy** - Automatic deployments from GitHub
- ✅ **HTTPS Enabled** - Secure SSL certificate included
- ✅ **All Animations Preserved** - Full UI/UX experience maintained

### 🛠️ **Deploy Your Own Instance**

1. **Fork this repository**
2. **Sign up at [render.com](https://render.com)**
3. **Connect your GitHub repository**
4. **Use these settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
5. **Deploy!** - Your instance will be live in minutes

---

## 🛠️ **Development**

### **Running in Development Mode**

```bash
# Enable auto-reload for development
uvicorn app:app --reload --port 8000

# With debugging
uvicorn app:app --reload --log-level debug
```

### **🧪 Testing**

```bash
# Run tests (when implemented)
pytest tests/

# Code quality check
flake8 backend/
black backend/
```

---

## 🤝 **Contributing**

We welcome contributions! 🎉

### **🚀 Quick Contribution Steps**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

---

## 📋 **Dependencies**

### **Core Technologies**
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server
- **[Radon](https://radon.readthedocs.io/)** - Code metrics analysis engine
- **[Jinja2](https://jinja.palletsprojects.com/)** - Powerful template engine

### **Frontend Libraries**
- **[jsPDF](https://github.com/parallax/jsPDF)** - PDF generation
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Modern styling with animations

---

## 🐛 **Troubleshooting**

<div align="center">

| Issue | Solution |
|-------|----------|
| **Port already in use** | Change port: `uvicorn app:app --port 8001` |
| **Module not found** | Install dependencies: `pip install -r requirements.txt` |
| **File upload fails** | Check file size (<5MB) and format |
| **Analysis stuck** | Refresh page and try smaller file |

</div>

---

## 📜 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Radon** team for excellent code metrics library
- **FastAPI** community for the amazing framework
- **Contributors** who helped improve this project

---

<div align="center">

## 🌟 **Star this repository if you found it helpful!**

### 🚀 **[Try Live Demo](https://codelitmus.onrender.com)** | **[View Source](https://github.com/prathamesh9930/CodeLitmus)**

**Made with ❤️ by [Prathamesh](https://github.com/prathamesh9930)**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-codelitmus.onrender.com-FF6B6B?style=for-the-badge&logoColor=white)](https://codelitmus.onrender.com)
[![GitHub Stars](https://img.shields.io/github/stars/prathamesh9930/CodeLitmus?style=for-the-badge&logo=github)](https://github.com/prathamesh9930/CodeLitmus/stargazers)

[⬆ Back to top](#-codelitmus)

</div>
