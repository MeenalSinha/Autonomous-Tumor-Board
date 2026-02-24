"""
Imaging Agent (Agent B)
Analyzes medical imaging (CT/MRI) and generates structured radiology reports.

Model: MedGemma 1.5 (multimodal reasoning) - simulated
Focus: Tumor staging, size assessment, spread indicators
"""

import json
from typing import Dict, List
from datetime import datetime
from models.case_models import ImagingFindings, ConfidenceLevel


class ImagingAgent:
    """
    Agent B: Medical Imaging Analysis
    
    Simulates MedGemma 1.5 with multimodal reasoning.
    In production, would process DICOM files and 3D reconstructions.
    """
    
    def __init__(self):
        self.agent_name = "Imaging Agent"
        self.model_name = "MedGemma 1.5 (Multimodal Reasoning)"
        
    def analyze(self, case_data: Dict) -> ImagingFindings:
        """
        Analyze imaging data and generate structured findings.
        
        In production:
        - Would process actual DICOM files
        - Perform automated segmentation
        - Generate volumetric measurements
        - Detect lymph nodes and metastases
        
        For demo:
        - Simulates realistic radiological analysis
        - Uses anatomical knowledge and staging criteria
        """
        
        primary_site = case_data.get("primary_site", "Unknown").lower()
        clinical_history = case_data.get("clinical_history", "")
        
        # Determine imaging modality
        modality = self._select_modality(primary_site)
        
        # Simulate tumor localization
        location = self._localize_tumor(primary_site)
        
        # Simulate size measurements
        size = self._measure_tumor(primary_site)
        
        # Assess staging indicators
        staging = self._assess_staging(primary_site, size)
        
        # Evaluate spread
        spread = self._evaluate_spread(primary_site, staging)
        
        # Assess lymph nodes
        lymph_nodes = self._assess_lymph_nodes(primary_site)
        
        # Check for distant metastases
        metastases = self._check_metastases(primary_site)
        
        # Generate key observations
        observations = self._generate_observations(
            modality, location, size, staging, spread
        )
        
        # Assess confidence
        confidence = self._assess_confidence(modality, size)
        
        # Identify uncertainties
        uncertainties = self._identify_uncertainties(
            modality, staging, metastases
        )
        
        return ImagingFindings(
            modality=modality,
            tumor_location=location,
            tumor_size_cm=size,
            staging_indicators=staging,
            spread_assessment=spread,
            lymph_nodes=lymph_nodes,
            distant_metastases=metastases,
            confidence=confidence,
            key_observations=observations,
            uncertainty_notes=uncertainties
        )
    
    def _select_modality(self, site: str) -> str:
        """Select appropriate imaging modality"""
        modality_map = {
            "lung": "Contrast-enhanced CT Chest",
            "breast": "MRI Breast with contrast",
            "brain": "MRI Brain with and without contrast",
            "liver": "Triphasic CT Abdomen or MRI Liver",
            "colon": "CT Abdomen/Pelvis with contrast",
            "pancreas": "Pancreatic Protocol CT",
            "prostate": "Multiparametric MRI Prostate"
        }
        
        for key, value in modality_map.items():
            if key in site:
                return value
        
        return "CT with contrast"
    
    def _localize_tumor(self, site: str) -> str:
        """Localize tumor within anatomical site"""
        locations = {
            "lung": "Right upper lobe, posterior segment",
            "breast": "Left breast, upper outer quadrant at 10 o'clock position",
            "colon": "Sigmoid colon, approximately 20cm from anal verge",
            "liver": "Right hepatic lobe, segments 6-7",
            "pancreas": "Pancreatic head",
            "prostate": "Left peripheral zone, mid-gland"
        }
        
        for key, value in locations.items():
            if key in site:
                return value
        
        return f"{site.title()}, primary mass"
    
    def _measure_tumor(self, site: str) -> List[float]:
        """
        Simulate tumor measurements [length, width, height] in cm
        Follows RECIST 1.1 criteria where applicable
        """
        # Simulated measurements - would be automated segmentation in production
        return [3.2, 2.8, 2.5]  # cm
    
    def _assess_staging(self, site: str, size: List[float]) -> Dict[str, str]:
        """Assess TNM staging indicators from imaging"""
        max_dimension = max(size)
        
        staging = {}
        
        # T stage (Tumor)
        if max_dimension < 2:
            staging["T_stage_indicator"] = "Suggests T1 (≤2cm)"
        elif max_dimension < 3:
            staging["T_stage_indicator"] = "Suggests T1-T2 (2-3cm)"
        elif max_dimension < 5:
            staging["T_stage_indicator"] = "Suggests T2 (3-5cm)"
        else:
            staging["T_stage_indicator"] = "Suggests T3 (>5cm)"
        
        # Additional staging features
        staging["Local_invasion"] = "No evidence of chest wall or mediastinal invasion"
        staging["Vascular_involvement"] = "No vascular encasement identified"
        
        return staging
    
    def _evaluate_spread(self, site: str, staging: Dict[str, str]) -> str:
        """Evaluate tumor spread patterns"""
        assessment = """The primary tumor appears confined to the organ of origin.

No definite extracapsular extension or invasion into adjacent structures identified on current imaging.

Tumor margins appear relatively well-defined, though biological behavior cannot be fully determined by imaging alone."""
        
        return assessment.strip()
    
    def _assess_lymph_nodes(self, site: str) -> str:
        """Assess regional lymph nodes"""
        # Simulated lymph node assessment
        return """Regional lymph nodes:
- Right hilar nodes: Normal size (<1cm)
- Subcarinal nodes: Borderline enlarged (1.2cm short axis)
- Mediastinal nodes: Multiple nodes up to 1.5cm

Recommendation: Borderline nodes warrant close attention. Consider PET-CT for metabolic characterization or biopsy if clinically indicated."""
    
    def _check_metastases(self, site: str) -> str:
        """Check for distant metastases"""
        return "No definite distant metastases identified on current study. Liver, adrenals, and imaged skeleton appear unremarkable."
    
    def _generate_observations(
        self,
        modality: str,
        location: str,
        size: List[float],
        staging: Dict[str, str],
        spread: str
    ) -> List[str]:
        """Generate key radiological observations"""
        observations = [
            f"Primary lesion identified at {location}",
            f"Measured {size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} cm",
            f"Imaging performed: {modality}",
            "Tumor demonstrates heterogeneous enhancement pattern",
            "No calcifications identified within the lesion",
            "Surrounding parenchyma shows mild inflammatory changes"
        ]
        
        return observations
    
    def _assess_confidence(self, modality: str, size: List[float]) -> ConfidenceLevel:
        """Assess confidence in imaging interpretation"""
        # In production, would consider image quality, artifacts, etc.
        if max(size) > 1.0:  # Larger lesions easier to characterize
            return ConfidenceLevel.MODERATE
        else:
            return ConfidenceLevel.LOW
    
    def _identify_uncertainties(
        self, modality: str, staging: Dict[str, str], metastases: str
    ) -> List[str]:
        """Identify areas requiring additional imaging or review"""
        uncertainties = []
        
        if "CT" in modality:
            uncertainties.append(
                "MRI may provide superior soft tissue characterization"
            )
        
        uncertainties.append(
            "PET-CT recommended for comprehensive staging and detection of occult metastases"
        )
        
        uncertainties.append(
            "Follow-up imaging in 6-8 weeks recommended to assess response after treatment initiation"
        )
        
        uncertainties.append(
            "Radiologist subspecialty review recommended for final staging determination"
        )
        
        return uncertainties


# Example usage for testing
if __name__ == "__main__":
    agent = ImagingAgent()
    
    test_case = {
        "case_id": "TB-2026-001",
        "primary_site": "lung",
        "clinical_history": "65M with persistent cough and weight loss"
    }
    
    findings = agent.analyze(test_case)
    print(json.dumps(findings.dict(), indent=2, default=str))
