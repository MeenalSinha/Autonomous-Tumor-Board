# Autonomous Tumor Board (Agentic MDT Assistant)

> AI-assisted, multi-agent system that prepares draft multidisciplinary tumor board reports for complex cancer cases.

## 🎯 What It Does

Simulates a multidisciplinary cancer team meeting using multiple AI "agents" to prepare a draft cancer treatment discussion in minutes instead of weeks.

## ⚡ Impact: Manual vs AI-Assisted MDT

```
MANUAL MDT PREPARATION              AI-ASSISTED MDT PREPARATION
━━━━━━━━━━━━━━━━━━━━━━━━━━          ━━━━━━━━━━━━━━━━━━━━━━━━━━

Day 1-2:  Pathology review          Instant:  ┌──────────────┐
Day 2-3:  Imaging review                      │  All Agents  │
Day 3-5:  Guideline research                  │   Process    │
Day 5-7:  Schedule coordination               │ Concurrently │
Day 7-10: Draft preparation                   └──────────────┘
          Multiple review cycles                      ↓
          ↓                                    Instant: Draft Ready
Day 10+:  Finally ready for MDT                      ↓
                                              Then: Human MDT Review

⏱️  5-10 DAYS                                ⏱️  < 5 SECONDS + REVIEW

                                             99.9% TIME REDUCTION
```

**The Result:** Doctors get comprehensive, structured reports immediately — focusing their expertise on decision-making, not data gathering.

## 🏗️ Architecture

### Multi-Agent System
- **Agent A (Pathology)**: Analyzes histopathology findings
- **Agent B (Imaging)**: Analyzes CT/MRI scans
- **Agent C (Guidelines)**: Checks treatment guidelines and trials
- **Agent D (MDT Synthesizer)**: Coordinates and synthesizes all findings

### Tech Stack
- **Models**: MedGemma (4B, 1.5, 27B) - simulated for demo
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Imaging**: PyDICOM, OpenCV
- **Knowledge**: FAISS + Sentence Transformers
- **Language**: Python 3.10+

## 🚀 Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Start the Streamlit UI
streamlit run app.py

# Or run the FastAPI backend separately
uvicorn api:app --reload
```

## 📁 Project Structure

```
autonomous_tumor_board/
├── agents/
│   ├── __init__.py
│   ├── pathology_agent.py
│   ├── imaging_agent.py
│   ├── guideline_agent.py
│   └── mdt_synthesizer.py
├── orchestrator/
│   ├── __init__.py
│   └── controller.py
├── models/
│   ├── __init__.py
│   ├── case_models.py
│   └── agent_outputs.py
├── utils/
│   ├── __init__.py
│   ├── medical_imaging.py
│   ├── guideline_db.py
│   └── report_generator.py
├── data/
│   ├── guidelines/
│   ├── sample_cases/
│   └── templates/
├── api.py
├── app.py
├── requirements.txt
└── README.md
```

## ✨ Key Features

### Core Features
- ✅ Multi-agent MDT simulation
- ✅ MDT-style draft report generation
- ✅ Safety disclaimers and human-in-the-loop
- ✅ Intermediate reasoning visibility
- ✅ Guideline grounding with citations
- ✅ Uncertainty-aware language
- ✅ Offline/local execution
- ✅ Structured JSON + PDF outputs
- ✅ Editable by clinicians
- ✅ Time-to-draft comparison

### 🆕 V1.1 High-Impact Improvements
- ✅ **Agent Disagreement Detection** - Explicitly flags when agents disagree (clinical realism)
- ✅ **Clinician Action Checklist** - Meeting-ready action items for tumor board
- ✅ **Longitudinal Tracking** - "Changes Since Last Review" for follow-up cases
- ✅ **Enhanced Confidence Display** - Visual indicators + evidence source labels

> See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed information on these enhancements.

### Safety Features
- 🔒 No automatic treatment decisions
- 🔒 Explicit confidence scoring
- 🔒 "Human review required" disclaimers
- 🔒 Privacy-first (offline capable)
- 🔒 Structured escalation logic

## 📊 Example Output

```
Tumor Board Draft Report
├── Case Summary (de-identified)
├── Pathology Findings (Agent A)
├── Imaging Findings (Agent B)
├── Guideline-Aligned Options (Agent C)
├── MDT Synthesis (Agent D)
└── Human Review Required Section
```

## ⚠️ Important Disclaimer

**This system is a DRAFT PREPARATION TOOL ONLY**
- Does NOT make diagnostic decisions
- Does NOT provide treatment recommendations
- REQUIRES human clinician review
- NOT a substitute for multidisciplinary team discussion

## 🎓 Use Cases

- Preparing tumor board materials in under-resourced hospitals
- Accelerating case preparation for experienced MDT teams
- Educational tool for medical training
- Research into AI-assisted clinical workflows

## 🔬 Future Clinical Validation

This system demonstrates feasibility and technical architecture. Clinical deployment would require prospective validation studies comparing AI-assisted vs traditional MDT preparation in real-world settings, measuring outcomes such as time-to-treatment, decision quality, and clinician satisfaction.

## 📝 License

This is a demonstration/competition project. Not for clinical use.

## 🤝 Contributing

This project was built for educational and competition purposes.

---

**Built with clinical realism, safety-first design, and human oversight.**
