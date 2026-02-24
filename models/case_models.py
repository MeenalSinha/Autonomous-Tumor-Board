"""
Data models for tumor board cases and agent outputs.
Uses Pydantic for validation and structured outputs.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence levels for AI predictions"""
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"
    UNCERTAIN = "Uncertain"


class PatientCase(BaseModel):
    """De-identified patient case information"""
    case_id: str = Field(..., description="Unique case identifier")
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    primary_site: str
    clinical_history: str
    pathology_file: Optional[str] = None
    imaging_file: Optional[str] = None
    prior_case_id: Optional[str] = Field(
        default=None,
        description="Reference to previous tumor board case for longitudinal tracking"
    )
    changes_since_last_review: Optional[List[str]] = Field(
        default=None,
        description="Notable changes since prior evaluation (if applicable)"
    )
    uploaded_at: datetime = Field(default_factory=datetime.now)


class PathologyFindings(BaseModel):
    """Output from Pathology Agent"""
    agent_name: str = "Pathology Agent"
    tumor_type: str
    histologic_grade: str
    tumor_size_mm: Optional[float] = None
    biomarkers: Dict[str, str] = Field(default_factory=dict)
    lymph_node_status: Optional[str] = None
    margins: Optional[str] = None
    confidence: ConfidenceLevel
    evidence_strength: str = Field(
        default="Histology",
        description="Primary evidence source: Histology, Immunohistochemistry, Molecular, etc."
    )
    raw_observations: str
    clinical_significance: str
    uncertainty_notes: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class ImagingFindings(BaseModel):
    """Output from Imaging Agent"""
    agent_name: str = "Imaging Agent"
    modality: str  # CT, MRI, PET, etc.
    tumor_location: str
    tumor_size_cm: List[float] = Field(description="[length, width, height] in cm")
    staging_indicators: Dict[str, str]
    spread_assessment: str
    lymph_nodes: str
    distant_metastases: Optional[str] = None
    confidence: ConfidenceLevel
    evidence_strength: str = Field(
        default="Imaging",
        description="Primary evidence source: CT, MRI, PET-CT, Ultrasound, etc."
    )
    key_observations: List[str]
    uncertainty_notes: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class TreatmentOption(BaseModel):
    """Single treatment pathway option"""
    treatment_type: str
    description: str
    guideline_reference: str
    evidence_level: str
    considerations: List[str]
    contraindications: List[str] = Field(default_factory=list)


class GuidelineRecommendations(BaseModel):
    """Output from Guideline Agent"""
    agent_name: str = "Guideline & Trial Agent"
    primary_diagnosis: str
    stage_estimate: str
    treatment_options: List[TreatmentOption]
    clinical_trials: List[str] = Field(default_factory=list)
    guideline_sources: List[str]
    confidence: ConfidenceLevel
    evidence_strength: str = Field(
        default="Clinical Guidelines",
        description="Primary evidence source: NCCN, ASCO, ESMO, Clinical Trials, etc."
    )
    special_considerations: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


class MDTSynthesis(BaseModel):
    """Output from MDT Synthesizer Agent"""
    agent_name: str = "MDT Synthesizer"
    executive_summary: str
    key_findings: Dict[str, str]
    changes_since_last_review: Optional[List[str]] = Field(
        default=None,
        description="Interval changes detected since prior tumor board (if applicable)"
    )
    discussion_points: List[str]
    recommended_approach: str
    open_questions: List[str]
    uncertainty_flags: List[str]
    clinician_action_checklist: List[str] = Field(
        default_factory=list,
        description="Concrete action items for clinicians to complete during/after MDT"
    )
    confidence: ConfidenceLevel
    escalation_required: bool = Field(
        default=True,
        description="Always True - human review required"
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class TumorBoardReport(BaseModel):
    """Complete MDT draft report"""
    case_id: str
    patient_info: PatientCase
    pathology: PathologyFindings
    imaging: ImagingFindings
    guidelines: GuidelineRecommendations
    synthesis: MDTSynthesis
    generated_at: datetime = Field(default_factory=datetime.now)
    disclaimer: str = Field(
        default="⚠️ DRAFT FOR CLINICIAN REVIEW ONLY - NOT A DIAGNOSTIC OR TREATMENT DECISION"
    )
    human_review_required: bool = Field(default=True)
    
    class Config:
        json_schema_extra = {
            "example": {
                "case_id": "TB-2026-001",
                "disclaimer": "⚠️ DRAFT FOR CLINICIAN REVIEW ONLY"
            }
        }
