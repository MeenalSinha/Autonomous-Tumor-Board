# Setup & Installation Guide

This guide provides detailed instructions for setting up the **Autonomous Tumor Board** development environment.

## 1. Environment Requirements
- **Python**: 3.10 to 3.14
- **OS**: Windows, Linux, or macOS
- **Disk Space**: ~1GB (for model weights and FAISS index)

## 2. Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/MeenalSinha/Autonomous-Tumor-Board.git
cd Autonomous-Tumor-Board
```

### Step 2: Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
The installation will automatically handle OpenCV, PyDICOM, FAISS, and Sentence-Transformers.

```bash
pip install -r requirements.txt
```

## 3. Configuration

### Knowledge Base Initialization
The system uses a RAG engine located in `utils/rag_engine.py`. On first run, it will look for `knowledge_base/guidelines.json`. Ensure this file is populated with valid treatment options.

### Database
The system uses **SQLite** by default (`tumor_board.db`). No external database setup is required for the default configuration.

## 4. Running the Application

### Option A: Complete System (Web UI)
Launch both the backend and frontend simultaneously:

```bash
# Terminal 1: Backend
uvicorn api:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
streamlit run app.py
```

### Option B: Command Line Test
Verify the entire pipeline from the CLI:

```bash
python test_system.py
```

## 5. Troubleshooting

**Missing 'reportlab' error:**
Ensure you have the latest version of pip: `python -m pip install --upgrade pip` and re-run installation.

**FAISS errors on Windows:**
If you encounter DLL issues with FAISS, ensure you have the Microsoft Visual C++ Redistributable installed.

**OpenCV Video Loading error:**
On some Linux systems, you may need `libgl1`: `sudo apt-get install libgl1-mesa-glx`
