import numpy as np
from typing import Dict, List, Any
from models.case_models import ConfidenceLevel

class MDTReasoningEngine:
    """
    Real reasoning engine for synthesizing multi-agent outputs.
    Uses weighted conflict detection and confidence aggregation.
    """
    
    def calculate_global_confidence(self, confidences: List[ConfidenceLevel]) -> ConfidenceLevel:
        """Aggregates confidence levels from multiple agents"""
        score_map = {
            ConfidenceLevel.HIGH: 1.0,
            ConfidenceLevel.MODERATE: 0.6,
            ConfidenceLevel.LOW: 0.2
        }
        scores = [score_map.get(c, 0.5) for c in confidences]
        avg_score = np.mean(scores)
        
        if avg_score > 0.8: return ConfidenceLevel.HIGH
        if avg_score > 0.4: return ConfidenceLevel.MODERATE
        return ConfidenceLevel.LOW
        
    def detect_conflicts(self, path_data: Dict, img_data: Dict) -> List[Dict]:
        """Detects objective clinical conflicts between imaging and pathology"""
        conflicts = []
        
        # Conflict 1: Size mismatch (Pathology vs Imaging)
        path_size = path_data.get("tumor_size_mm", 0) / 10 # cm
        img_size = max(img_data.get("tumor_size_cm", [0]))
        
        if abs(path_size - img_size) > 1.5:
            conflicts.append({
                "type": "SIZE_MISMATCH",
                "severity": "HIGH",
                "description": f"Imaging suggests {img_size}cm while pathology shows {path_size}cm. Possible sampling error or multi-focal disease."
            })
            
        # Conflict 2: Staging discrepancy
        if img_size > 5.0 and "0/" in path_data.get("lymph_node_status", ""):
            conflicts.append({
                "type": "STAGING_DISCREPANCY",
                "severity": "MEDIUM",
                "description": "Large tumor (>5cm) with negative pathologic lymph nodes. Confirm radiology nodal assessment."
            })
            
        return conflicts
