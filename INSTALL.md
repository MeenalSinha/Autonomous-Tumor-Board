# Installation Guide

Complete installation instructions for the Autonomous Tumor Board system.

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows 10/11
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 1GB free space
- **Internet**: Required for initial setup (optional after installation)

### Recommended Environment
- **Python**: 3.10 or 3.11
- **RAM**: 8GB or more
- **Processor**: Multi-core CPU
- **Display**: 1920x1080 or higher

## 📦 Installation Methods

### Method 1: Standard Installation (Recommended)

```bash
# 1. Clone or download the repository
git clone https://github.com/yourusername/autonomous-tumor-board.git
cd autonomous-tumor-board

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python test_system.py
```

### Method 2: Development Installation

```bash
# Follow steps 1-3 from Method 1, then:

# Install with development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .

# Verify installation
python test_system.py
```

### Method 3: Docker Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/autonomous-tumor-board.git
cd autonomous-tumor-board

# 2. Build Docker image
docker build -t tumor-board:latest .

# 3. Run Streamlit UI
docker run -p 8501:8501 tumor-board:latest

# Or use docker-compose for both UI and API
docker-compose up
```

## 🚀 Quick Start

After installation, run:

```bash
# Start Streamlit UI
streamlit run app.py

# Or start FastAPI backend
uvicorn api:app --reload
```

Then open your browser to:
- Streamlit UI: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs

## 🔍 Troubleshooting

### Common Issues

#### Issue: "Python version not supported"
```bash
# Check Python version
python --version

# Must be 3.10 or higher
# Install Python 3.10+ from python.org
```

#### Issue: "Module not found" errors
```bash
# Ensure virtual environment is activated
# Look for (venv) in your terminal prompt

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: "Permission denied" errors
```bash
# On Linux/macOS, use:
chmod +x app.py

# Or run with python explicitly:
python -m streamlit run app.py
```

#### Issue: "Port already in use"
```bash
# Use a different port for Streamlit
streamlit run app.py --server.port 8502

# Or for FastAPI
uvicorn api:app --port 8001
```

### Platform-Specific Notes

#### Windows
- Use `venv\Scripts\activate` (not `source`)
- May need to run as Administrator
- Use forward slashes `/` or double backslashes `\\` in paths

#### macOS
- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

#### Linux
- May need to install python3-venv:
  ```bash
  sudo apt-get install python3.10-venv
  ```

## 📋 Dependency Notes

### Core Dependencies
- **fastapi**: REST API backend
- **streamlit**: Interactive UI
- **pydantic**: Data validation
- **reportlab**: PDF generation

### Optional Dependencies
- **pydicom**: DICOM file support (future)
- **opencv-python**: Image processing (future)
- **sentence-transformers**: RAG support (future)

## 🧪 Verify Installation

Run the test suite to verify everything is working:

```bash
python test_system.py
```

Expected output:
```
================================
✓ ALL TESTS PASSED!
================================
✓ Data models
✓ Individual agents
✓ Orchestrator
✓ Report generation
```

## 🔒 Security Notes

### For Development
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Never commit `.env` files with sensitive data
- Use virtual environments to isolate dependencies

### For Production (If Ever Deployed)
⚠️ **This system is NOT approved for clinical use**

If you ever consider deployment:
1. Conduct security audit
2. Implement proper authentication
3. Use HTTPS/TLS encryption
4. Follow HIPAA/GDPR guidelines
5. Get regulatory approval
6. Conduct clinical validation

## 📞 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed usage
3. Check existing [GitHub Issues](https://github.com/yourusername/autonomous-tumor-board/issues)
4. Create a new issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce

## ✅ Next Steps

After successful installation:

1. Read [README.md](README.md) for overview
2. Try the [QUICKSTART.md](QUICKSTART.md) guide
3. Run a test case through the UI
4. Review [FEATURES.md](FEATURES.md) for capabilities
5. Check [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for presentation tips

---

**Installation complete? Time to explore the system!** 🚀
