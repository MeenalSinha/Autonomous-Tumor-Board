"""
Orchestrator Controller
Manages the sequential execution of all agents and coordinates the workflow.

This is the main control logic that runs the entire tumor board pipeline.
"""

import json
import time
from typing import Dict, Optional
from datetime import datetime

from models.case_models import (
    PatientCase,
    TumorBoardReport,
    PathologyFindings,
    ImagingFindings,
    GuidelineRecommendations,
    MDTSynthesis
)
from agents import (
    PathologyAgent,
    ImagingAgent,
    GuidelineAgent,
    MDTSynthesizerAgent
)


class TumorBoardOrchestrator:
    """
    Main orchestrator for the Autonomous Tumor Board system.
    
    Execution flow:
    1. Validate input case
    2. Run Pathology Agent (Agent A)
    3. Run Imaging Agent (Agent B)  
    4. Run Guideline Agent (Agent C) with A+B outputs
    5. Run MDT Synthesizer (Agent D) with A+B+C outputs
    6. Generate final report
    
    All intermediate outputs are preserved for transparency.
    """
    
    def __init__(self):
        """Initialize all agents"""
        self.pathology_agent = PathologyAgent()
        self.imaging_agent = ImagingAgent()
        self.guideline_agent = GuidelineAgent()
        self.synthesizer_agent = MDTSynthesizerAgent()
        
        # Track execution metrics
        self.execution_times = {}
        
    def process_case(self, patient_case: PatientCase) -> TumorBoardReport:
        """
        Process a complete case through all agents.
        
        Args:
            patient_case: Validated PatientCase object
            
        Returns:
            TumorBoardReport: Complete tumor board draft report
        """
        
        print(f"\n{'='*60}")
        print(f"AUTONOMOUS TUMOR BOARD - CASE {patient_case.case_id}")
        print(f"{'='*60}\n")
        
        # Convert to dict for agent processing
        case_data = patient_case.dict()
        
        # Step 1: Pathology Analysis
        print("🔬 Running Pathology Agent (Agent A)...")
        start_time = time.time()
        pathology_findings = self._run_pathology_agent(case_data)
        self.execution_times['pathology'] = time.time() - start_time
        print(f"   ✓ Completed in {self.execution_times['pathology']:.2f}s")
        print(f"   → Diagnosis: {pathology_findings.tumor_type}")
        
        # Step 2: Imaging Analysis
        print("\n📊 Running Imaging Agent (Agent B)...")
        start_time = time.time()
        imaging_findings = self._run_imaging_agent(case_data)
        self.execution_times['imaging'] = time.time() - start_time
        print(f"   ✓ Completed in {self.execution_times['imaging']:.2f}s")
        print(f"   → Tumor size: {max(imaging_findings.tumor_size_cm):.1f}cm")
        
        # Step 3: Guideline Analysis
        print("\n📚 Running Guideline Agent (Agent C)...")
        start_time = time.time()
        guideline_recommendations = self._run_guideline_agent(
            case_data, pathology_findings, imaging_findings
        )
        self.execution_times['guidelines'] = time.time() - start_time
        print(f"   ✓ Completed in {self.execution_times['guidelines']:.2f}s")
        print(f"   → Stage: {guideline_recommendations.stage_estimate}")
        print(f"   → Treatment options: {len(guideline_recommendations.treatment_options)}")
        
        # Step 4: MDT Synthesis
        print("\n🔄 Running MDT Synthesizer (Agent D)...")
        start_time = time.time()
        mdt_synthesis = self._run_synthesizer(
            case_data, pathology_findings, imaging_findings, guideline_recommendations
        )
        self.execution_times['synthesis'] = time.time() - start_time
        print(f"   ✓ Completed in {self.execution_times['synthesis']:.2f}s")
        print(f"   → Confidence: {mdt_synthesis.confidence.value}")
        
        # Step 5: Generate Final Report
        print("\n📄 Generating Tumor Board Report...")
        report = TumorBoardReport(
            case_id=patient_case.case_id,
            patient_info=patient_case,
            pathology=pathology_findings,
            imaging=imaging_findings,
            guidelines=guideline_recommendations,
            synthesis=mdt_synthesis
        )
        
        total_time = sum(self.execution_times.values())
        print(f"\n{'='*60}")
        print(f"✅ ANALYSIS COMPLETE - Total time: {total_time:.2f}s")
        print(f"{'='*60}\n")
        
        return report
    
    def _run_pathology_agent(self, case_data: Dict) -> PathologyFindings:
        """Execute Pathology Agent"""
        try:
            return self.pathology_agent.analyze(case_data)
        except Exception as e:
            print(f"   ❌ Error in Pathology Agent: {str(e)}")
            raise
    
    def _run_imaging_agent(self, case_data: Dict) -> ImagingFindings:
        """Execute Imaging Agent"""
        try:
            return self.imaging_agent.analyze(case_data)
        except Exception as e:
            print(f"   ❌ Error in Imaging Agent: {str(e)}")
            raise
    
    def _run_guideline_agent(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings
    ) -> GuidelineRecommendations:
        """Execute Guideline Agent"""
        try:
            return self.guideline_agent.analyze(case_data, pathology, imaging)
        except Exception as e:
            print(f"   ❌ Error in Guideline Agent: {str(e)}")
            raise
    
    def _run_synthesizer(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> MDTSynthesis:
        """Execute MDT Synthesizer"""
        try:
            return self.synthesizer_agent.synthesize(
                case_data, pathology, imaging, guidelines
            )
        except Exception as e:
            print(f"   ❌ Error in MDT Synthesizer: {str(e)}")
            raise
    
    def get_execution_summary(self) -> Dict:
        """Get summary of execution times"""
        total = sum(self.execution_times.values())
        return {
            "total_time_seconds": round(total, 2),
            "breakdown": {
                k: round(v, 2) for k, v in self.execution_times.items()
            },
            "comparison": {
                "ai_assisted": f"{total:.1f} seconds",
                "manual_mdt_prep": "5-10 days (estimated)"
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Create test case
    test_case = PatientCase(
        case_id="TB-2026-001",
        age=65,
        gender="Male",
        primary_site="lung",
        clinical_history="65-year-old male with 40 pack-year smoking history presenting with persistent cough, weight loss, and hemoptysis over 3 months."
    )
    
    # Run orchestrator
    orchestrator = TumorBoardOrchestrator()
    report = orchestrator.process_case(test_case)
    
    # Print results
    print("\n" + "="*60)
    print("TUMOR BOARD DRAFT REPORT")
    print("="*60)
    print(f"\nCase ID: {report.case_id}")
    print(f"Generated: {report.generated_at}")
    print(f"\n{report.disclaimer}")
    print("\n" + "="*60)
    
    # Show execution summary
    print("\nExecution Summary:")
    summary = orchestrator.get_execution_summary()
    print(json.dumps(summary, indent=2))
    
    # Save report to JSON
    output_file = f"/home/claude/autonomous_tumor_board/data/sample_cases/{test_case.case_id}_report.json"
    with open(output_file, 'w') as f:
        json.dump(report.dict(), f, indent=2, default=str)
    print(f"\n✓ Report saved to: {output_file}")
