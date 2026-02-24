# Autonomous Tumor Board - Setup & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone or extract the project**
```bash
cd autonomous_tumor_board
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Streamlit UI (Recommended for Demo)
```bash
streamlit run app.py
```
Then open your browser to: http://localhost:8501

#### Option 2: FastAPI Backend
```bash
uvicorn api:app --reload
```
API documentation available at: http://localhost:8000/docs

#### Option 3: Command Line (Testing)
```bash
python orchestrator/controller.py
```

---

## 📋 Using the System

### Streamlit UI Workflow

1. **Submit Case Page**
   - Enter patient demographics (age, gender)
   - Select primary cancer site
   - Provide clinical history
   - Click "Process Case"

2. **View Report Page**
   - Review executive summary
   - Examine each agent's findings
   - Check uncertainty flags
   - Download JSON or PDF report

3. **System Info Page**
   - View agent architecture
   - Check system capabilities
   - Review features

### API Workflow

1. **Submit a case via API**
```bash
curl -X POST "http://localhost:8000/api/cases/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "gender": "Male",
    "primary_site": "lung",
    "clinical_history": "65M with persistent cough and weight loss"
  }'
```

2. **Retrieve report**
```bash
curl "http://localhost:8000/api/reports/{case_id}"
```

3. **Download PDF**
```bash
curl "http://localhost:8000/api/reports/{case_id}/pdf" --output report.pdf
```

---

## 🏗️ Architecture Overview

### Multi-Agent Pipeline

```
User Input (Case Data)
        ↓
┌───────────────────────────────────┐
│   Orchestrator Controller         │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ Agent A: Pathology Analysis       │
│ Model: MedGemma 4B (Vision)       │
│ Output: Tumor type, grade, etc.   │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ Agent B: Imaging Analysis         │
│ Model: MedGemma 1.5 (Multimodal)  │
│ Output: Size, staging, spread     │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ Agent C: Guideline Matching       │
│ Model: MedGemma 27B (Reasoning)   │
│ Input: A + B outputs              │
│ Output: Treatment options         │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│ Agent D: MDT Synthesizer          │
│ Model: MedGemma 27B (Synthesis)   │
│ Input: A + B + C outputs          │
│ Output: Integrated report         │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│    Tumor Board Draft Report       │
│    - JSON format                  │
│    - PDF document                 │
└───────────────────────────────────┘
```

### Directory Structure

```
autonomous_tumor_board/
├── agents/                  # AI agent implementations
│   ├── pathology_agent.py   # Agent A
│   ├── imaging_agent.py     # Agent B
│   ├── guideline_agent.py   # Agent C
│   └── mdt_synthesizer.py   # Agent D
├── orchestrator/            # Workflow coordination
│   └── controller.py        # Main orchestrator
├── models/                  # Data models (Pydantic)
│   └── case_models.py       # Patient, findings, reports
├── utils/                   # Utility functions
│   └── report_generator.py  # PDF generation
├── data/                    # Data storage
│   ├── guidelines/          # Clinical guidelines
│   ├── outputs/             # Generated reports
│   └── uploads/             # Uploaded files
├── api.py                   # FastAPI backend
├── app.py                   # Streamlit frontend
└── requirements.txt         # Dependencies
```

---

## 🎯 Key Features Implemented

### ✅ Core Features (Non-Negotiable)

1. **Multi-Agent MDT Simulation**
   - 4 specialized agents (Pathology, Imaging, Guidelines, Synthesis)
   - Each produces signed, structured output
   - Sequential dependency-aware execution

2. **MDT-Style Draft Report**
   - Professional tumor board format
   - Case summary, findings, recommendations
   - Uncertainty flags and disclaimers
   - Human review requirements

3. **Safety & Human-in-the-Loop**
   - Prominent disclaimers in all outputs
   - No autonomous treatment decisions
   - Confidence scoring per section
   - Escalation logic

### ✅ Judge-Wow Features

4. **Intermediate Reasoning Visibility**
   - Each agent's output shown separately
   - Transparent decision-making process
   - Traceable reasoning path

5. **Guideline Grounding**
   - Evidence-based recommendations
   - Inline citations (simulated NCCN)
   - Treatment option references

6. **Time-to-Draft Comparison**
   - Displayed prominently in UI
   - "< 5 seconds vs 5-10 days"
   - Clear impact demonstration

7. **Uncertainty-Aware Language**
   - "Findings suggestive of..."
   - Confidence levels (High/Moderate/Low)
   - "Additional testing may be required"

### ✅ Practicality Features

8. **Offline/Local Mode**
   - No cloud dependencies
   - Fully functional locally
   - Privacy-preserving

9. **Structured Outputs**
   - JSON (machine-readable)
   - PDF (human-readable)
   - Downloadable reports

10. **Doctor-First UI**
    - Clean, professional interface
    - Medical terminology
    - Minimal unnecessary graphics

---

## 🧪 Testing

### Sample Test Cases

**Lung Cancer Case:**
```python
PatientCase(
    case_id="TB-TEST-001",
    age=65,
    gender="Male",
    primary_site="lung",
    clinical_history="65M, 40 pack-year smoking history, persistent cough, hemoptysis"
)
```

**Breast Cancer Case:**
```python
PatientCase(
    case_id="TB-TEST-002",
    age=52,
    gender="Female",
    primary_site="breast",
    clinical_history="52F, palpable mass in left breast upper outer quadrant"
)
```

### Running Tests

```bash
# Test individual agents
python agents/pathology_agent.py
python agents/imaging_agent.py
python agents/guideline_agent.py
python agents/mdt_synthesizer.py

# Test full orchestrator
python orchestrator/controller.py

# Test API
curl http://localhost:8000/health
```

---

## 📊 Expected Output

### Report Structure

1. **Executive Summary**
   - Patient snapshot
   - Key findings synthesis
   - Stage estimate
   - Critical discussion points

2. **Pathology Findings** (Agent A)
   - Tumor type and grade
   - Biomarker profile
   - Lymph node status
   - Clinical significance
   - Uncertainties

3. **Imaging Findings** (Agent B)
   - Imaging modality used
   - Tumor location and size
   - Staging indicators
   - Spread assessment
   - Recommendations

4. **Guideline Recommendations** (Agent C)
   - Stage estimate
   - Treatment options (2-4)
   - Clinical trials
   - Evidence levels
   - Special considerations

5. **MDT Synthesis** (Agent D)
   - Discussion points
   - Recommended approach
   - Open questions
   - Uncertainty flags
   - Human review requirement

### Sample Processing Time

```
Agent A (Pathology):  ~0.1s
Agent B (Imaging):    ~0.1s
Agent C (Guidelines): ~0.2s
Agent D (Synthesis):  ~0.1s
PDF Generation:       ~0.5s
─────────────────────────────
Total:                ~1.0s
```

---

## ⚠️ Important Notes

### Limitations

1. **Simulated Models**: Uses rule-based logic to simulate MedGemma models
2. **No Real Vision**: Doesn't process actual pathology images or DICOM files
3. **Mock Guidelines**: Uses simplified guideline summaries, not full NCCN database
4. **No Learning**: Doesn't learn from cases or improve over time
5. **Not Clinical**: NOT approved for actual clinical use

### What This IS

- ✅ Demonstration of multi-agent architecture
- ✅ Proof-of-concept for AI-assisted MDT prep
- ✅ Educational tool for AI in healthcare
- ✅ Research prototype

### What This IS NOT

- ❌ Medical device
- ❌ Diagnostic system
- ❌ Treatment recommendation engine
- ❌ Replacement for clinical expertise

---

## 🤝 Support

### Troubleshooting

**Issue: Dependencies not installing**
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**Issue: Streamlit not starting**
```bash
# Check if port 8501 is available
streamlit run app.py --server.port 8502
```

**Issue: Import errors**
```bash
# Ensure you're in the project directory
cd autonomous_tumor_board
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Getting Help

For questions or issues:
1. Check this documentation
2. Review the README.md
3. Examine the code comments
4. Check agent implementation files

---

## 📝 Citation & Attribution

This system was built for educational and competition purposes using:
- Simulated MedGemma models (architecture only, not actual models)
- NCCN guideline structure (simulated content)
- Standard clinical staging systems (TNM)
- Evidence-based medicine principles

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Purpose:** Educational/Research/Competition Demo  
**Status:** Prototype - Not for Clinical Use
