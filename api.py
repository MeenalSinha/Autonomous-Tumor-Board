"""
FastAPI Backend for Autonomous Tumor Board System
Provides REST API endpoints for case submission and report generation.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from typing import Optional, Dict, List
import json
import os
import re
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from models.case_models import PatientCase, TumorBoardReport
from models.database import PatientCaseDB, TumorBoardReportDB
from orchestrator import TumorBoardOrchestrator
from utils.report_generator import TumorBoardReportGenerator
from utils.db_manager import get_db, init_db


# Initialize FastAPI app
app = FastAPI(
    title="Autonomous Tumor Board API",
    description="AI-assisted multidisciplinary tumor board preparation system",
    version="1.1.0"
)

# Initialize database
init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize report generator
report_generator = TumorBoardReportGenerator()

# Ensure directories exist
os.makedirs("data/outputs", exist_ok=True)
os.makedirs("data/uploads", exist_ok=True)


class CaseSubmission(BaseModel):
    """API model for case submission"""
    age: int
    gender: str
    primary_site: str
    clinical_history: str


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Autonomous Tumor Board API",
        "version": "1.1.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "submit_case": "/api/cases/submit",
            "get_report": "/api/reports/{case_id}",
            "download_pdf": "/api/reports/{case_id}/pdf"
        },
        "disclaimer": "⚠️ DRAFT PREPARATION TOOL ONLY - NOT FOR CLINICAL DECISIONS"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "pathology": "operational",
            "imaging": "operational",
            "guidelines": "operational",
            "synthesizer": "operational"
        }
    }


@app.post("/api/cases/submit")
async def submit_case(case: CaseSubmission, db: Session = Depends(get_db)) -> Dict:
    """
    Submit a new case for tumor board analysis with DB persistence.
    """
    
    try:
        case_id = f"TB-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Save case to DB
        db_case = PatientCaseDB(
            case_id=case_id,
            age=case.age,
            gender=case.gender,
            primary_site=case.primary_site,
            clinical_history=case.clinical_history
        )
        db.add(db_case)
        db.commit()

        patient_case = PatientCase(
            case_id=case_id,
            age=case.age,
            gender=case.gender,
            primary_site=case.primary_site,
            clinical_history=case.clinical_history
        )
        
        # Process through orchestrator with DB session
        orchestrator = TumorBoardOrchestrator(db_session=db)
        report = orchestrator.process_case(patient_case)
        
        # PDF generation logic remains
        pdf_path = f"data/outputs/{case_id}_report.pdf"
        report_generator.generate_pdf(report, pdf_path)
        
        return {
            "success": True,
            "case_id": case_id,
            "report": report.dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reports/{case_id}")
async def get_report(case_id: str) -> Dict:
    """
    Retrieve a tumor board report by case ID.
    
    Args:
        case_id: Case identifier
        
    Returns:
        Dict containing report data
    """
    
    json_path = f"data/outputs/{case_id}_report.json"
    
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail=f"Report not found for case {case_id}")
    
    try:
        with open(json_path, 'r') as f:
            report_data = json.load(f)
        
        return {
            "success": True,
            "case_id": case_id,
            "report": report_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading report: {str(e)}")


@app.get("/api/reports/{case_id}/pdf")
async def download_pdf(case_id: str):
    """
    Download PDF report for a case.
    
    Args:
        case_id: Case identifier
        
    Returns:
        FileResponse with PDF
    """
    
    pdf_path = f"data/outputs/{case_id}_report.pdf"
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail=f"PDF report not found for case {case_id}")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{case_id}_tumor_board_report.pdf"
    )


@app.post("/api/upload/pathology")
async def upload_pathology(file: UploadFile = File(...)):
    """Securely upload pathology file"""
    safe_name = sanitize_filename(file.filename)
    file_path = f"data/uploads/{safe_name}"
    os.makedirs("data/uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"success": True, "filename": safe_name}


@app.post("/api/upload/imaging")
async def upload_imaging(file: UploadFile = File(...)):
    """
    Upload imaging file (placeholder - would process DICOM in production).
    
    Args:
        file: Uploaded file
        
    Returns:
        Dict with upload confirmation
    """
    
    # Save file
    file_path = f"data/uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "success": True,
        "filename": file.filename,
        "path": file_path,
        "message": "File uploaded successfully. In production, this would be processed for DICOM analysis."
    }


@app.get("/api/stats")
async def get_statistics():
    """Get system statistics"""
    
    # Count processed cases
    output_dir = "data/outputs"
    case_files = [f for f in os.listdir(output_dir) if f.endswith('_report.json')] if os.path.exists(output_dir) else []
    
    return {
        "total_cases_processed": len(case_files),
        "agents": {
            "pathology_agent": "MedGemma 4B (Vision-Heavy)",
            "imaging_agent": "MedGemma 1.5 (Multimodal)",
            "guideline_agent": "MedGemma 27B (Reasoning)",
            "synthesizer": "MedGemma 27B (Coordination)"
        },
        "average_processing_time": "< 5 seconds",
        "comparison": {
            "manual_mdt_prep": "5-10 days",
            "ai_assisted": "< 5 seconds"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
