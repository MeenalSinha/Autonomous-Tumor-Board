# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-13

### Added
- 🎯 **Agent Disagreement Detection**: System now explicitly flags when agents disagree
  - Detects 6 types of disagreements (size, lymph nodes, staging, etc.)
  - Prominently displayed in UI and reports
  - Prioritized in discussion points
  
- 🎯 **Clinician Action Checklist**: Meeting-ready action items
  - Concrete tasks for tumor board follow-up
  - Priority flagging for urgent items
  - Covers staging, consultations, testing, trials
  
- 🎯 **Longitudinal Tracking**: "Changes Since Last Review" feature
  - Tracks disease evolution over time
  - Documents interval changes
  - Supports follow-up case discussions
  
- 🎯 **Enhanced Confidence Display**: Visual indicators and evidence labels
  - Color-coded confidence levels (🟢🟡🔴⚪)
  - Evidence source labels per agent
  - Prominent metric cards in UI

- 📊 Visual timeline in README showing manual vs AI-assisted workflow
- 🎤 Demo narration script (<120 seconds)
- 🔬 Clinical validation note in documentation

### Changed
- Improved UI layout with confidence metrics
- Enhanced PDF report formatting
- Better disagreement highlighting throughout system

### Documentation
- Added IMPROVEMENTS.md detailing V1.1 enhancements
- Added DEMO_SCRIPT.md for presentations
- Updated README with visual timeline
- Enhanced FEATURES.md with new capabilities

## [1.0.0] - 2026-02-12

### Added
- 🤖 Multi-agent architecture with 4 specialized agents:
  - Agent A: Pathology analysis
  - Agent B: Imaging analysis
  - Agent C: Guideline matching
  - Agent D: MDT synthesis
  
- 📄 Professional tumor board report generation:
  - MDT-style format
  - JSON and PDF outputs
  - Structured with Pydantic models
  
- 🛡️ Comprehensive safety features:
  - No autonomous decisions
  - Confidence scoring
  - Uncertainty tracking
  - Human review requirements
  - Multiple disclaimers
  
- 🎨 User interfaces:
  - Streamlit demo UI
  - FastAPI backend with REST API
  - Interactive report viewer
  
- 📚 Complete documentation:
  - README.md - Project overview
  - SETUP_GUIDE.md - Installation instructions
  - FEATURES.md - Complete feature list
  - QUICKSTART.md - Quick reference
  
- ✅ Quality assurance:
  - Comprehensive test suite
  - Data validation with Pydantic
  - Type hints throughout
  - Extensive docstrings

### Core Features
- Intermediate reasoning visibility
- Guideline grounding with citations
- Offline/local execution capability
- Time-to-draft comparison (5-10 days → <5 seconds)
- Uncertainty-aware language throughout
- Editable outputs (JSON/PDF)

---

## Future Roadmap

### Planned for v1.2
- [ ] Real vision model integration for pathology
- [ ] DICOM file processing for imaging
- [ ] RAG over actual NCCN guidelines
- [ ] ClinicalTrials.gov API integration
- [ ] Multi-cancer type support

### Planned for v2.0
- [ ] Real-time collaboration features
- [ ] EMR/EHR integration capabilities
- [ ] Advanced molecular profiling support
- [ ] Outcome prediction models
- [ ] Clinical validation study framework

---

## Notes

- This is a demonstration/educational project
- Not approved for clinical use
- Requires regulatory approval for healthcare deployment
- All models are simulated for proof-of-concept

For detailed information about specific features, see:
- [FEATURES.md](FEATURES.md) - Complete feature documentation
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - V1.1 enhancement details
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Comprehensive overview
