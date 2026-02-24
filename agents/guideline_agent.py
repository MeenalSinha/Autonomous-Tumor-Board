"""
Guideline Agent (Agent C)
Analyzes treatment guidelines and clinical trials based on pathology and imaging findings.

Model: MedGemma 27B (reasoning-heavy) - simulated
Sources: NCCN Guidelines, Clinical Trials Database
"""

import json
from typing import Dict, List
from datetime import datetime
from models.case_models import (
    GuidelineRecommendations, 
    TreatmentOption, 
    ConfidenceLevel,
    PathologyFindings,
    ImagingFindings
)


class GuidelineAgent:
    """
    Agent C: Clinical Guideline & Trial Matching
    
    Simulates MedGemma 27B for complex reasoning.
    In production, would use RAG over actual NCCN guidelines and trial databases.
    """
    
    def __init__(self):
        self.agent_name = "Guideline & Trial Agent"
        self.model_name = "MedGemma 27B (Reasoning-Heavy)"
        self.guideline_version = "NCCN Guidelines v2.2026 (simulated)"
        
    def analyze(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings
    ) -> GuidelineRecommendations:
        """
        Generate guideline-aligned treatment recommendations.
        
        In production:
        - Would perform RAG over actual NCCN guidelines
        - Search ClinicalTrials.gov API
        - Match eligibility criteria
        
        For demo:
        - Simulates evidence-based recommendations
        - Uses realistic guideline language
        """
        
        # Extract key information
        primary_site = case_data.get("primary_site", "Unknown").lower()
        tumor_type = pathology.tumor_type
        stage_estimate = self._estimate_stage(pathology, imaging)
        
        # Generate treatment options
        treatment_options = self._generate_treatment_options(
            primary_site, tumor_type, stage_estimate, pathology, imaging
        )
        
        # Find relevant clinical trials
        trials = self._find_clinical_trials(primary_site, tumor_type, pathology)
        
        # Identify guideline sources
        sources = self._list_guideline_sources(primary_site)
        
        # Special considerations
        considerations = self._identify_special_considerations(
            pathology, imaging, case_data
        )
        
        # Assess confidence
        confidence = self._assess_confidence(stage_estimate, pathology)
        
        return GuidelineRecommendations(
            primary_diagnosis=tumor_type,
            stage_estimate=stage_estimate,
            treatment_options=treatment_options,
            clinical_trials=trials,
            guideline_sources=sources,
            confidence=confidence,
            special_considerations=considerations
        )
    
    def _estimate_stage(
        self, pathology: PathologyFindings, imaging: ImagingFindings
    ) -> str:
        """Estimate clinical stage based on available data"""
        
        # Extract tumor size
        tumor_size_cm = max(imaging.tumor_size_cm)
        
        # Extract lymph node status
        lymph_positive = "positive" in imaging.lymph_nodes.lower()
        
        # Check for metastases
        has_metastases = imaging.distant_metastases and \
                        "no definite" not in imaging.distant_metastases.lower()
        
        # Simplified staging logic (actual would be much more complex)
        if has_metastases:
            return "Clinical Stage IV (Suspected metastatic disease)"
        elif lymph_positive:
            return "Clinical Stage III (Suspected regional lymph node involvement)"
        elif tumor_size_cm > 5:
            return "Clinical Stage IIB-III (T3 lesion)"
        elif tumor_size_cm > 2:
            return "Clinical Stage IIA (T2 lesion)"
        else:
            return "Clinical Stage I (Early stage)"
        
    def _generate_treatment_options(
        self,
        site: str,
        tumor_type: str,
        stage: str,
        pathology: PathologyFindings,
        imaging: ImagingFindings
    ) -> List[TreatmentOption]:
        """Generate evidence-based treatment options"""
        
        options = []
        
        # Option 1: Surgical approach (if appropriate stage)
        if "Stage I" in stage or "Stage II" in stage:
            options.append(TreatmentOption(
                treatment_type="Surgical Resection",
                description="Anatomic resection (lobectomy or pneumonectomy) with systematic lymph node dissection",
                guideline_reference="NCCN Guidelines v2.2026 - Preferred for resectable early-stage disease",
                evidence_level="Category 1 (High-level evidence)",
                considerations=[
                    "Patient must be medically fit for surgery",
                    "Adequate pulmonary reserve required",
                    "Multidisciplinary evaluation recommended",
                    "Consider neoadjuvant therapy if borderline resectable"
                ],
                contraindications=[
                    "Poor performance status (ECOG ≥3)",
                    "Inadequate cardiopulmonary reserve",
                    "Unresectable disease on imaging"
                ]
            ))
        
        # Option 2: Systemic therapy
        if pathology.biomarkers.get("PD-L1"):
            pd_l1_value = pathology.biomarkers["PD-L1"]
            
            options.append(TreatmentOption(
                treatment_type="Immunotherapy-Based Regimen",
                description=f"PD-1/PD-L1 inhibitor (pembrolizumab or nivolumab) ± chemotherapy. PD-L1 expression: {pd_l1_value}",
                guideline_reference="NCCN Guidelines v2.2026 - Category 1 for PD-L1 ≥50%",
                evidence_level="Category 1" if "50%" in pd_l1_value else "Category 2A",
                considerations=[
                    "Higher PD-L1 expression associated with better response",
                    "Monitor for immune-related adverse events",
                    "Consider combination vs monotherapy based on PD-L1 level",
                    "Baseline imaging and PFTs required"
                ],
                contraindications=[
                    "Active autoimmune disease",
                    "History of severe immune-related toxicity",
                    "Symptomatic interstitial lung disease"
                ]
            ))
        
        # Option 3: Radiation therapy
        options.append(TreatmentOption(
            treatment_type="Radiation Therapy",
            description="Definitive radiotherapy (SBRT for early stage or conventional RT for locally advanced)",
            guideline_reference="NCCN Guidelines v2.2026 - Alternative for medically inoperable patients",
            evidence_level="Category 1 for SBRT in early stage",
            considerations=[
                "SBRT (stereotactic body radiation therapy) preferred for peripheral T1-T2 tumors",
                "Conventional fractionation for central tumors or larger lesions",
                "Careful planning to minimize lung toxicity",
                "May be combined with systemic therapy"
            ],
            contraindications=[
                "Prior thoracic radiation exceeding tolerance",
                "Severe baseline pulmonary fibrosis"
            ]
        ))
        
        # Option 4: Clinical trial (always consider)
        options.append(TreatmentOption(
            treatment_type="Clinical Trial Enrollment",
            description="Investigational therapy through an appropriate clinical trial",
            guideline_reference="NCCN Guidelines v2.2026 - Encouraged for all patients when available",
            evidence_level="Category 2A",
            considerations=[
                "May provide access to novel targeted therapies",
                "Eligibility criteria must be met",
                "Patient willingness and informed consent required",
                "Trial availability varies by institution"
            ],
            contraindications=[]
        ))
        
        return options
    
    def _find_clinical_trials(
        self, site: str, tumor_type: str, pathology: PathologyFindings
    ) -> List[str]:
        """
        Simulate clinical trial matching.
        In production, would query ClinicalTrials.gov API.
        """
        
        trials = []
        
        # Simulate realistic trial names
        if "lung" in site:
            trials = [
                "NCT05123456: Phase III trial of novel TKI in EGFR-mutant NSCLC",
                "NCT05234567: Immunotherapy combination in PD-L1 high expressors",
                "NCT05345678: Neoadjuvant chemoimmunotherapy for resectable Stage III",
            ]
        elif "breast" in site:
            trials = [
                "NCT05456789: CDK4/6 inhibitor in hormone receptor-positive disease",
                "NCT05567890: HER2-targeted ADC in HER2-low breast cancer",
            ]
        else:
            trials = [
                "NCT05678901: Pan-tumor basket trial for rare molecular alterations",
                "NCT05789012: Novel immunotherapy in solid tumors",
            ]
        
        return trials
    
    def _list_guideline_sources(self, site: str) -> List[str]:
        """List guideline sources used"""
        
        sources = [
            "NCCN Clinical Practice Guidelines in Oncology v2.2026",
            "ASCO Clinical Practice Guidelines",
            "ESMO Clinical Practice Guidelines"
        ]
        
        if "lung" in site:
            sources.append("International Association for the Study of Lung Cancer (IASLC) Staging Manual 9th Edition")
        
        return sources
    
    def _identify_special_considerations(
        self, pathology: PathologyFindings, imaging: ImagingFindings, case_data: Dict
    ) -> List[str]:
        """Identify special patient-specific considerations"""
        
        considerations = []
        
        # Age-based considerations
        age = case_data.get("age", 0)
        if age > 75:
            considerations.append(
                "Elderly patient: Consider comprehensive geriatric assessment before aggressive therapy"
            )
        elif age < 50:
            considerations.append(
                "Younger patient: May be candidate for more aggressive multimodal therapy"
            )
        
        # Biomarker-based
        if pathology.biomarkers:
            considerations.append(
                "Molecular profiling complete - targeted therapy options available"
            )
        else:
            considerations.append(
                "Consider comprehensive genomic profiling (NGS) if not yet performed"
            )
        
        # Uncertainty flags
        if pathology.uncertainty_notes:
            considerations.append(
                "Pathology review by subspecialist recommended before final treatment planning"
            )
        
        if imaging.uncertainty_notes:
            considerations.append(
                "Additional imaging (PET-CT) recommended for complete staging"
            )
        
        # Multidisciplinary care
        considerations.append(
            "Formal multidisciplinary tumor board discussion strongly recommended"
        )
        
        considerations.append(
            "Patient preferences and goals of care should guide final treatment selection"
        )
        
        return considerations
    
    def _assess_confidence(
        self, stage: str, pathology: PathologyFindings
    ) -> ConfidenceLevel:
        """Assess confidence in guideline recommendations"""
        
        # Lower confidence if staging uncertain
        if "Suspected" in stage:
            return ConfidenceLevel.MODERATE
        
        # Lower confidence if pathology uncertain
        if pathology.confidence == ConfidenceLevel.LOW:
            return ConfidenceLevel.MODERATE
        
        return ConfidenceLevel.MODERATE


# Example usage for testing
if __name__ == "__main__":
    from agents.pathology_agent import PathologyAgent
    from agents.imaging_agent import ImagingAgent
    
    # Create test case
    test_case = {
        "case_id": "TB-2026-001",
        "primary_site": "lung",
        "age": 65,
        "clinical_history": "65M with persistent cough and weight loss"
    }
    
    # Run previous agents
    path_agent = PathologyAgent()
    img_agent = ImagingAgent()
    
    pathology = path_agent.analyze(test_case)
    imaging = img_agent.analyze(test_case)
    
    # Run guideline agent
    guide_agent = GuidelineAgent()
    recommendations = guide_agent.analyze(test_case, pathology, imaging)
    
    print(json.dumps(recommendations.dict(), indent=2, default=str))
