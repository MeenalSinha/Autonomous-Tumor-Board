# Autonomous Tumor Board (ATB) - Agentic MDT Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Empowering clinicians with AI-driven multidisciplinary case preparation.**

---

## 🎯 Project Overview

The **Autonomous Tumor Board (ATB)** is a production-grade multi-agent system designed to optimize the preparation of Multidisciplinary Team (MDT) meetings. By orchestrating specialized agents for Pathology, Imaging, and Clinical Guidelines, ATB generates high-fidelity draft reports in seconds, enabling doctors to focus on complex decision-making rather than data gathering.

### ⚡ The Problem: Manual MDT Prep takes 5-10 Days
Traditional MDT preparation involves fragmented communication between radiologists, pathologists, and oncologists over several days.

### 💡 The Solution: AI-Assisted MDT Prep takes < 5 Seconds
ATB automates the synthesis of clinical data, radiological images, and histopathology findings into a unified, evidence-based draft report.

---

## 🏗️ Architecture & Tech Stack

### Functional Agent Orchestra
- **Agent A (Pathology)**: Real `OpenCV` vision analysis for nuclei density and atypia.
- **Agent B (Imaging)**: Real `pydicom` processing for mass measurement and metadata.
- **Agent C (Guidelines)**: Real `Sentence-Transformers` + `FAISS` RAG for NCCN grounding.
- **Agent D (MDT Synthesizer)**: Consensus reasoning engine for conflict detection.

### Modern Stack
- **Backend**: FastAPI (Python 3.12+ optimized)
- **Frontend**: Streamlit (Premium modern UI)
- **Database**: SQLAlchemy (SQLite) for persistent clinical records
- **Reporting**: ReportLab for dynamic PDF generation
- **ML**: FAISS, Sentence-Transformers, OpenCV, NumPy

---

## 🚀 Getting Started

### Installation

```bash
# 1. Clone & Setup
git clone https://github.com/MeenalSinha/Autonomous-Tumor-Board.git
cd Autonomous-Tumor-Board

# 2. Setup environment
python -m venv venv
source venv/bin/activate # windows: venv\Scripts\activate

# 3. Install core dependencies
pip install -r requirements.txt
```

### Running the System

```bash
# Launch the Backend API
uvicorn api:app --reload

# Launch the Front-end UI
streamlit run app.py
```

---

## 📁 Technical Documentation

- 📐 **[Architecture](docs/ARCHITECTURE.md)**: Deep dive into the agentic RAG and CV pipelines.
- 🔌 **[API Reference](docs/API.md)**: Documentation for REST endpoints and data models.
- 🛠️ **[Setup Guide](docs/SETUP.md)**: Advanced configuration and environment setup.
- 👨‍💻 **[Contributing](CONTRIBUTING.md)**: Guidelines for future enhancements.

---

## ✨ Primary Features

1.  **AI Image Processing**: Real pixel-level analysis of DICOM and Histology scans.
2.  **Semantic RAG**: Grounded treatment options matched via vector search.
3.  **Conflict Detection**: Logic-based flagging of clinical discrepancies.
4.  **Persistent Registry**: SQL database for case history and longitudinal tracking.
5.  **Professional Export**: PDF reports with evidence citations and safety flags.

---

## ⚠️ Safety & Compliance

**This system is a DRAFT PREPARATION TOOL ONLY.**
- **NOT** for making diagnostic or treatment decisions.
- **REQUIRES** human validation of every finding.
- Designed with **Privacy-First** principles for local deployment.

---

## 📜 License
Licensed under the [MIT License](LICENSE).

---
*Built with clinical realism, safety-first design, and human oversight.*
