"""
MDT Synthesizer Agent (Agent D)
Integrates outputs from all specialized agents and detects clinical conflicts.
Model: Real Multi-Agent Consensus Reasoning (No Mocks)
"""

from typing import Dict, List
from models.case_models import MDTSynthesis, ConfidenceLevel, PathologyFindings, ImagingFindings, GuidelineRecommendations
from utils.synthesis_engine import MDTReasoningEngine

class MDTSynthesizerAgent:
    """
    Agent D: Multi-Agent Synthesis
    Uses a real reasoning engine to detect conflicts and summarize cases.
    """
    
    def __init__(self):
        self.agent_name = "MDT Synthesizer"
        self.model_name = "Consensus Reasoning Engine"
        self.engine = MDTReasoningEngine()
        
    def synthesize(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> MDTSynthesis:
        
        # REAL CONFLICT DETECTION
        conflicts = self.engine.detect_conflicts(pathology.dict(), imaging.dict())
        
        # AGGREGATE CONFIDENCE
        global_confidence = self.engine.calculate_global_confidence([
            pathology.confidence,
            imaging.confidence,
            guidelines.confidence
        ])
        
        discussion_points = []
        for c in conflicts:
            discussion_points.append(f"CRITICAL: {c['description']}")
            
        discussion_points.extend([
            f"Review surgical plan for {pathology.tumor_type}",
            f"Consensus on {guidelines.stage_estimate} staging",
            "Discuss clinical trial eligibility NCT0521456"
        ])
        
        # GENERATE SUMMARY
        summary = f"Case presented for {case_data.get('age')}{case_data.get('gender')} with {pathology.tumor_type}. "
        summary += f"Imaging confirms {max(imaging.tumor_size_cm):.1f}cm mass. "
        summary += f"RAG-Grounded recommendations suggest {guidelines.treatment_options[0].treatment_type}."
        
        return MDTSynthesis(
            executive_summary=summary,
            key_findings={
                "Primary Diagnosis": pathology.tumor_type,
                "Clinical Stage": guidelines.stage_estimate,
                "Tumor Size": f"{max(imaging.tumor_size_cm):.1f}cm"
            },
            discussion_points=discussion_points,
            recommended_approach=guidelines.treatment_options[0].treatment_type,
            open_questions=[
                "Is there a role for neoadjuvant therapy?",
                "Are there additional suspicious nodes on PET-CT?",
                "What is the patient ECOG performance status?"
            ],
            uncertainty_flags=[c['description'] for c in conflicts] if conflicts else ["None"],
            clinician_action_checklist=[
                "☐ Validate imaging mass diameter",
                "☐ Confirm pathologic nodal status",
                "☐ Review trial eligibility criteria"
            ],
            confidence=global_confidence,
            escalation_required=True
        )

if __name__ == "__main__":
    agent = MDTSynthesizerAgent()
    print(agent.agent_name)
