#!/usr/bin/env python3
"""
Test script to verify Autonomous Tumor Board system functionality.
Runs a complete test case through all agents and generates reports.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.case_models import PatientCase
from orchestrator import TumorBoardOrchestrator
from utils.report_generator import TumorBoardReportGenerator


def test_individual_agents():
    """Test each agent individually"""
    
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL AGENTS")
    print("="*60)
    
    from agents import PathologyAgent, ImagingAgent, GuidelineAgent, MDTSynthesizerAgent
    
    # Test case data
    test_case = {
        "case_id": "TEST-001",
        "primary_site": "lung",
        "age": 65,
        "gender": "Male",
        "clinical_history": "65M with persistent cough and weight loss"
    }
    
    # Test Pathology Agent
    print("\n1. Testing Pathology Agent...")
    try:
        path_agent = PathologyAgent()
        path_findings = path_agent.analyze(test_case)
        print(f"   ✓ Pathology Agent OK")
        print(f"   → Diagnosis: {path_findings.tumor_type}")
        print(f"   → Confidence: {path_findings.confidence.value}")
    except Exception as e:
        print(f"   ✗ Pathology Agent FAILED: {e}")
        return False
    
    # Test Imaging Agent
    print("\n2. Testing Imaging Agent...")
    try:
        img_agent = ImagingAgent()
        img_findings = img_agent.analyze(test_case)
        print(f"   ✓ Imaging Agent OK")
        print(f"   → Modality: {img_findings.modality}")
        print(f"   → Size: {max(img_findings.tumor_size_cm):.1f}cm")
    except Exception as e:
        print(f"   ✗ Imaging Agent FAILED: {e}")
        return False
    
    # Test Guideline Agent
    print("\n3. Testing Guideline Agent...")
    try:
        guide_agent = GuidelineAgent()
        guidelines = guide_agent.analyze(test_case, path_findings, img_findings)
        print(f"   ✓ Guideline Agent OK")
        print(f"   → Stage: {guidelines.stage_estimate}")
        print(f"   → Options: {len(guidelines.treatment_options)}")
    except Exception as e:
        print(f"   ✗ Guideline Agent FAILED: {e}")
        return False
    
    # Test Synthesizer Agent
    print("\n4. Testing MDT Synthesizer...")
    try:
        synth_agent = MDTSynthesizerAgent()
        synthesis = synth_agent.synthesize(test_case, path_findings, img_findings, guidelines)
        print(f"   ✓ Synthesizer Agent OK")
        print(f"   → Discussion points: {len(synthesis.discussion_points)}")
        print(f"   → Open questions: {len(synthesis.open_questions)}")
    except Exception as e:
        print(f"   ✗ Synthesizer Agent FAILED: {e}")
        return False
    
    print("\n✓ All individual agents passed!")
    return True


def test_orchestrator():
    """Test full orchestrator workflow"""
    
    print("\n" + "="*60)
    print("TESTING ORCHESTRATOR WORKFLOW")
    print("="*60)
    
    try:
        # Create test case
        patient_case = PatientCase(
            case_id="TEST-FULL-001",
            age=65,
            gender="Male",
            primary_site="lung",
            clinical_history="65-year-old male with 40 pack-year smoking history. Presents with persistent cough, 15lb weight loss over 3 months, and occasional hemoptysis. CT chest shows 3.2cm mass in right upper lobe."
        )
        
        print(f"\nProcessing case: {patient_case.case_id}")
        
        # Initialize orchestrator
        orchestrator = TumorBoardOrchestrator()
        
        # Process case
        report = orchestrator.process_case(patient_case)
        
        # Verify report structure
        assert report.case_id == patient_case.case_id
        assert report.pathology is not None
        assert report.imaging is not None
        assert report.guidelines is not None
        assert report.synthesis is not None
        
        print(f"\n✓ Orchestrator workflow completed successfully!")
        print(f"  → Report generated for case {report.case_id}")
        
        # Get execution summary
        exec_summary = orchestrator.get_execution_summary()
        print(f"  → Total time: {exec_summary['total_time_seconds']}s")
        
        return True, report
        
    except Exception as e:
        print(f"\n✗ Orchestrator test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_report_generation(report):
    """Test PDF report generation"""
    
    print("\n" + "="*60)
    print("TESTING REPORT GENERATION")
    print("="*60)
    
    try:
        # Ensure output directory exists
        os.makedirs("data/outputs", exist_ok=True)
        
        # Generate PDF
        pdf_path = f"data/outputs/{report.case_id}_test_report.pdf"
        
        generator = TumorBoardReportGenerator()
        generated_path = generator.generate_pdf(report, pdf_path)
        
        # Verify file was created
        assert os.path.exists(generated_path)
        file_size = os.path.getsize(generated_path)
        
        print(f"\n✓ PDF generation successful!")
        print(f"  → File: {generated_path}")
        print(f"  → Size: {file_size:,} bytes")
        
        # Also save JSON
        json_path = f"data/outputs/{report.case_id}_test_report.json"
        with open(json_path, 'w') as f:
            json.dump(report.dict(), f, indent=2, default=str)
        
        print(f"  → JSON: {json_path}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Report generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_models():
    """Test Pydantic data models"""
    
    print("\n" + "="*60)
    print("TESTING DATA MODELS")
    print("="*60)
    
    try:
        from models.case_models import (
            PatientCase,
            PathologyFindings,
            ImagingFindings,
            GuidelineRecommendations,
            MDTSynthesis,
            TumorBoardReport,
            ConfidenceLevel,
            TreatmentOption
        )
        
        # Test PatientCase validation
        print("\n1. Testing PatientCase validation...")
        case = PatientCase(
            case_id="TEST-001",
            age=65,
            gender="Male",
            primary_site="lung",
            clinical_history="Test history"
        )
        assert case.age == 65
        print("   ✓ PatientCase validation OK")
        
        # Test invalid age
        try:
            invalid_case = PatientCase(
                case_id="TEST-002",
                age=150,  # Invalid
                gender="Male",
                primary_site="lung",
                clinical_history="Test"
            )
            print("   ✗ Age validation failed to catch invalid value")
            return False
        except:
            print("   ✓ Age validation working correctly")
        
        # Test ConfidenceLevel enum
        print("\n2. Testing ConfidenceLevel enum...")
        assert ConfidenceLevel.HIGH.value == "High"
        assert ConfidenceLevel.MODERATE.value == "Moderate"
        print("   ✓ ConfidenceLevel enum OK")
        
        print("\n✓ All data models passed validation!")
        return True
        
    except Exception as e:
        print(f"\n✗ Data model test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    
    print("\n" + "="*80)
    print(" "*20 + "AUTONOMOUS TUMOR BOARD - SYSTEM TEST")
    print("="*80)
    
    results = {}
    
    # Test 1: Data Models
    results['data_models'] = test_data_models()
    
    # Test 2: Individual Agents
    results['individual_agents'] = test_individual_agents()
    
    # Test 3: Orchestrator
    orchestrator_passed, report = test_orchestrator()
    results['orchestrator'] = orchestrator_passed
    
    # Test 4: Report Generation (only if orchestrator passed)
    if orchestrator_passed and report:
        results['report_generation'] = test_report_generation(report)
    else:
        results['report_generation'] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name.replace('_', ' ').title():.<50} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*80)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nThe system is ready to use. You can now:")
        print("  1. Run the Streamlit UI: streamlit run app.py")
        print("  2. Run the FastAPI backend: uvicorn api:app --reload")
        print("  3. Check generated test reports in: data/outputs/")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease review the errors above and fix any issues.")
    print("="*80 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
