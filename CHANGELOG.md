# Changelog

All notable changes to the Autonomous Tumor Board project will be documented in this file.

## [1.1.0] - 2026-04-10
### Added
- **Real Computational Units**: Replaced simulated mocks with actual `OpenCV` vision analysis and `pydicom` radiological extraction.
- **Semantic RAG Engine**: Implemented `Sentence-Transformers` + `FAISS` for grounded medical guideline matching.
- **Persistence Layer**: Integrated `SQLAlchemy` and `SQLite` for persistent clinical case storage and longitudinal tracking.
- **MDT Conflict Detection**: Added a reasoning engine to the Synthesizer agent to detect discrepancies between radiology and pathology.
- **Improved PDF Reporting**: Automated professional report generation with evidence-strength indicators via `ReportLab`.
- **System Test Suite**: New `test_system.py` using synthetic biological data (DICOM and Histology images) to verify the full pipeline.

### Changed
- **Architecture**: Decoupled agent logic into specialized processors in `utils/`.
- **API**: Upgraded FastAPI endpoints to include DB dependency injection and secure file handling.
- **UI**: Updated Streamlit interface to support v1.1 features and persistent history view.
- **Dependencies**: Loosened version constraints in `requirements.txt` to support Python 3.12-3.14.

### Fixed
- **Security**: Resolved path traversal vulnerabilities in file upload endpoints.
- **Environment**: Fixed `reportlab` and `numpy` build failures on high-version Python.
- **Data Integrity**: Enforced strict Pydantic validation across all agent boundaries.

## [1.0.0] - 2026-04-01
### Added
- Initial project architecture (FastAPI + Streamlit).
- Multi-agent orchestration framework (simulated).
- Basic report generation logic.
- Pydantic case models.
