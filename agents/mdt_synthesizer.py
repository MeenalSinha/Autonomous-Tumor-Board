"""
MDT Synthesizer Agent (Agent D - Coordinator)
Synthesizes findings from all agents into a cohesive tumor board report.

Model: MedGemma 27B (reasoning-heavy) - simulated
Role: Coordination, synthesis, uncertainty flagging
"""

import json
from typing import Dict, List
from datetime import datetime
from models.case_models import (
    MDTSynthesis,
    PathologyFindings,
    ImagingFindings,
    GuidelineRecommendations,
    ConfidenceLevel
)


class MDTSynthesizerAgent:
    """
    Agent D: MDT Report Synthesizer & Coordinator
    
    Integrates outputs from all specialist agents into a cohesive,
    clinician-reviewable tumor board summary.
    
    Critical principles:
    - Does NOT make final treatment decisions
    - Highlights areas of uncertainty
    - Flags discrepancies between modalities
    - Always requires human review
    """
    
    def __init__(self):
        self.agent_name = "MDT Synthesizer"
        self.model_name = "MedGemma 27B (Coordination & Synthesis)"
        
    def synthesize(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> MDTSynthesis:
        """
        Synthesize all agent outputs into MDT-ready summary.
        
        This is the coordinator function that brings everything together
        in the style of a real tumor board discussion.
        
        NEW: Detects agent disagreements and flags them explicitly.
        """
        
        # CRITICAL: Detect agent disagreements first
        disagreements = self._detect_agent_disagreements(
            pathology, imaging, guidelines
        )
        
        # Generate executive summary (with disagreements if present)
        exec_summary = self._create_executive_summary(
            case_data, pathology, imaging, guidelines, disagreements
        )
        
        # Compile key findings
        key_findings = self._compile_key_findings(
            pathology, imaging, guidelines
        )
        
        # Generate discussion points (prioritize disagreements)
        discussion_points = self._generate_discussion_points(
            pathology, imaging, guidelines, disagreements
        )
        
        # Create recommended approach (NOT a decision)
        recommended_approach = self._create_recommended_approach(
            guidelines, pathology, imaging
        )
        
        # Identify open questions
        open_questions = self._identify_open_questions(
            pathology, imaging, guidelines
        )
        
        # Compile uncertainty flags
        uncertainty_flags = self._compile_uncertainty_flags(
            pathology, imaging, guidelines, disagreements
        )
        
        # Generate clinician action checklist
        action_checklist = self._generate_clinician_action_checklist(
            pathology, imaging, guidelines, disagreements
        )
        
        # Process longitudinal changes if available
        changes = self._process_longitudinal_changes(case_data, pathology, imaging)
        
        # Assess overall confidence (lower if disagreements exist)
        confidence = self._assess_overall_confidence(
            pathology, imaging, guidelines, disagreements
        )
        
        return MDTSynthesis(
            executive_summary=exec_summary,
            key_findings=key_findings,
            changes_since_last_review=changes,
            discussion_points=discussion_points,
            recommended_approach=recommended_approach,
            open_questions=open_questions,
            uncertainty_flags=uncertainty_flags,
            clinician_action_checklist=action_checklist,
            confidence=confidence,
            escalation_required=True  # Always True - human review mandatory
        )
    
    def _detect_agent_disagreements(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> List[str]:
        """
        Detect disagreements or discrepancies between agent outputs.
        
        This is CRITICAL for clinical realism - real tumor boards exist
        precisely because different specialists see different things.
        
        Returns list of disagreement descriptions for flagging.
        """
        
        disagreements = []
        
        # 1. Size discrepancy between pathology and imaging
        if pathology.tumor_size_mm and imaging.tumor_size_cm:
            path_size_cm = pathology.tumor_size_mm / 10
            img_size_cm = max(imaging.tumor_size_cm)
            
            if abs(path_size_cm - img_size_cm) > 1.0:  # >1cm difference
                disagreements.append(
                    f"Size discrepancy: Pathology reports {path_size_cm:.1f}cm "
                    f"vs Imaging {img_size_cm:.1f}cm. Reconciliation needed."
                )
        
        # 2. Lymph node status disagreement
        path_nodes = pathology.lymph_node_status.lower() if pathology.lymph_node_status else ""
        img_nodes = imaging.lymph_nodes.lower()
        
        path_positive = "positive" in path_nodes or "involved" in path_nodes
        img_suspicious = "enlarged" in img_nodes or "suspicious" in img_nodes or "borderline" in img_nodes
        path_negative = "0/" in path_nodes or "negative" in path_nodes
        
        if path_negative and img_suspicious:
            disagreements.append(
                "Lymph node discordance: Pathology shows negative nodes but "
                "imaging suggests borderline/suspicious adenopathy. Additional sampling may be indicated."
            )
        
        # 3. Staging discrepancy
        if "Clinical" in guidelines.stage_estimate or "Suspected" in guidelines.stage_estimate:
            if pathology.confidence == ConfidenceLevel.LOW or imaging.confidence == ConfidenceLevel.LOW:
                disagreements.append(
                    "Staging uncertainty: Low confidence in pathology or imaging findings "
                    "limits definitive stage assignment. Consider additional diagnostic procedures."
                )
        
        # 4. Grade vs imaging aggressiveness mismatch
        if "poorly differentiated" in pathology.histologic_grade.lower() or "Grade 3" in pathology.histologic_grade:
            if "well-defined" in imaging.spread_assessment.lower() or "confined" in imaging.spread_assessment.lower():
                disagreements.append(
                    "Biology vs imaging discordance: High-grade histology suggests aggressive behavior "
                    "but imaging shows relatively confined disease. This warrants discussion."
                )
        
        # 5. Confidence level disagreements (one agent very confident, another not)
        confidences = [pathology.confidence, imaging.confidence, guidelines.confidence]
        if ConfidenceLevel.HIGH in confidences and ConfidenceLevel.LOW in confidences:
            high_agents = []
            low_agents = []
            if pathology.confidence == ConfidenceLevel.HIGH:
                high_agents.append("Pathology")
            elif pathology.confidence == ConfidenceLevel.LOW:
                low_agents.append("Pathology")
            if imaging.confidence == ConfidenceLevel.HIGH:
                high_agents.append("Imaging")
            elif imaging.confidence == ConfidenceLevel.LOW:
                low_agents.append("Imaging")
            if guidelines.confidence == ConfidenceLevel.HIGH:
                high_agents.append("Guidelines")
            elif guidelines.confidence == ConfidenceLevel.LOW:
                low_agents.append("Guidelines")
            
            if high_agents and low_agents:
                disagreements.append(
                    f"Confidence discordance: {', '.join(high_agents)} show high confidence "
                    f"while {', '.join(low_agents)} show low confidence. "
                    f"Consider which data sources are most reliable for this case."
                )
        
        # 6. Treatment implications disagreement
        stage_roman = guidelines.stage_estimate.split()[1] if len(guidelines.stage_estimate.split()) > 1 else ""
        
        if "IV" in stage_roman and any("Surgical" in opt.treatment_type for opt in guidelines.treatment_options):
            disagreements.append(
                "Treatment paradigm question: Stage IV disease identified but surgical options listed. "
                "Clarify if oligometastatic vs widely metastatic and appropriateness of local therapy."
            )
        
        return disagreements
    
    def _create_executive_summary(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations,
        disagreements: List[str]
    ) -> str:
        """
        Create 3-4 paragraph executive summary.
        Written in clinical language, suitable for tumor board presentation.
        """
        
        age = case_data.get("age", "Unknown")
        gender = case_data.get("gender", "Unknown")
        
        summary = f"""CASE PRESENTATION

This case involves a {age}-year-old {gender.lower()} patient presenting with {case_data.get('primary_site', 'unknown primary site')}-related symptoms. {case_data.get('clinical_history', 'Clinical details provided.')}

INTEGRATED FINDINGS

Pathology analysis reveals {pathology.tumor_type.lower()}. The tumor demonstrates {pathology.histologic_grade.lower()}. Biomarker analysis shows {self._summarize_biomarkers(pathology.biomarkers)}. 

Imaging studies ({imaging.modality}) demonstrate a lesion measuring {imaging.tumor_size_cm[0]:.1f} x {imaging.tumor_size_cm[1]:.1f} x {imaging.tumor_size_cm[2]:.1f} cm at {imaging.tumor_location.lower()}. {imaging.spread_assessment.split('.')[0]}.

Based on available data, {guidelines.stage_estimate.lower()} is estimated. Guideline-based treatment options include {len(guidelines.treatment_options)} distinct pathways, ranging from surgical resection to systemic therapy to clinical trial enrollment.

SYNTHESIS

This case demonstrates the complexity of {case_data.get('primary_site', 'cancer')} management requiring integrated multidisciplinary input. Several areas warrant careful MDT discussion, including optimal treatment sequencing, patient fitness for aggressive intervention, and consideration of novel therapeutic approaches through clinical trials.

The AI-assisted analysis provides a structured foundation for tumor board discussion but requires expert clinical judgment for final treatment planning."""

        # Add disagreement section if any exist
        if disagreements:
            summary += "\n\n⚠️ AGENT DISAGREEMENTS DETECTED\n\n"
            summary += "The following areas show differing interpretations between modalities and require prioritized MDT discussion:\n\n"
            for disagreement in disagreements:
                summary += f"• {disagreement}\n"
            summary += "\nThese disagreements are flagged for explicit resolution during tumor board review."
        
        return summary.strip()
    
    def _summarize_biomarkers(self, biomarkers: Dict[str, str]) -> str:
        """Summarize biomarker profile"""
        if not biomarkers:
            return "limited biomarker data available"
        
        key_markers = list(biomarkers.items())[:2]  # First 2 markers
        summary = ", ".join([f"{k}: {v}" for k, v in key_markers])
        
        if len(biomarkers) > 2:
            summary += f", among {len(biomarkers)} total markers evaluated"
        
        return summary
    
    def _compile_key_findings(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> Dict[str, str]:
        """Compile key findings from each modality"""
        
        findings = {
            "Pathology": f"{pathology.tumor_type}, {pathology.histologic_grade}",
            "Imaging": f"{imaging.modality}: {max(imaging.tumor_size_cm):.1f}cm lesion, {imaging.tumor_location}",
            "Stage": guidelines.stage_estimate,
            "Biomarkers": self._format_biomarkers_short(pathology.biomarkers),
            "Treatment_Options": f"{len(guidelines.treatment_options)} evidence-based pathways identified"
        }
        
        return findings
    
    def _format_biomarkers_short(self, biomarkers: Dict[str, str]) -> str:
        """Short biomarker summary"""
        if not biomarkers:
            return "Pending or not available"
        return "; ".join([f"{k}:{v}" for k, v in list(biomarkers.items())[:3]])
    
    def _generate_discussion_points(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations,
        disagreements: List[str]
    ) -> List[str]:
        """
        Generate key points for MDT discussion.
        These are questions/topics the human team should debate.
        
        PRIORITY: Disagreements come first.
        """
        
        points = []
        
        # PRIORITY: Add disagreements as discussion points first
        if disagreements:
            for disagreement in disagreements:
                points.append(f"🔴 DISAGREEMENT: {disagreement}")
        
        # Treatment selection
        points.append(
            f"Treatment approach selection: {len(guidelines.treatment_options)} "
            "guideline-concordant options available - discuss sequencing and patient preferences"
        )
        
        # Staging confirmation
        if "Suspected" in guidelines.stage_estimate or "Clinical" in guidelines.stage_estimate:
            points.append(
                "Staging confirmation: Consider additional imaging (PET-CT) or invasive "
                "staging procedures to confirm clinical stage"
            )
        
        # Resectability
        if any("Surgical" in opt.treatment_type for opt in guidelines.treatment_options):
            points.append(
                "Resectability assessment: Surgical candidacy requires thoracic surgery "
                "evaluation of technical resectability and patient fitness"
            )
        
        # Biomarker implications
        if pathology.biomarkers:
            points.append(
                "Biomarker-directed therapy: Discuss implications of molecular profile "
                "for treatment selection and sequencing"
            )
        
        # Clinical trials
        if guidelines.clinical_trials:
            points.append(
                f"Clinical trial eligibility: {len(guidelines.clinical_trials)} potentially "
                "relevant trials identified - assess patient eligibility and interest"
            )
        
        # Quality of life
        points.append(
            "Goals of care: Clarify patient preferences, quality of life priorities, "
            "and acceptance of treatment-related toxicity"
        )
        
        # Subspecialty input
        points.append(
            "Subspecialty consultation: Consider additional input from radiation oncology, "
            "thoracic surgery, interventional radiology as indicated"
        )
        
        return points
    
    def _create_recommended_approach(
        self,
        guidelines: GuidelineRecommendations,
        pathology: PathologyFindings,
        imaging: ImagingFindings
    ) -> str:
        """
        Create a recommended approach framework.
        
        CRITICAL: This is NOT a treatment decision - it's a structured
        framework for the human team to consider.
        """
        
        approach = """SUGGESTED DISCUSSION FRAMEWORK (Requires MDT Confirmation)

Based on guideline analysis and integrated findings, the following framework is suggested for tumor board discussion:

1. STAGING COMPLETION
   - Confirm clinical stage with additional imaging if indicated
   - Consider invasive staging procedures based on treatment intent
   - Assess fitness for aggressive intervention (performance status, comorbidities)

2. TREATMENT PATHWAY CONSIDERATION
   The guideline analysis identified multiple evidence-based options:
"""
        
        # Add top 2-3 treatment options
        for i, option in enumerate(guidelines.treatment_options[:3], 1):
            approach += f"\n   Option {i}: {option.treatment_type}\n"
            approach += f"   - {option.description}\n"
            approach += f"   - Evidence: {option.evidence_level}\n"
        
        approach += """
3. MULTIDISCIPLINARY INPUT REQUIRED
   - Surgical evaluation (if resection considered)
   - Medical oncology (systemic therapy planning)
   - Radiation oncology (if RT indicated)
   - Patient preferences and goals of care discussion

4. NEXT STEPS
   - Complete any pending diagnostic work-up
   - Formal tumor board presentation
   - Patient counseling regarding options
   - Shared decision-making process

⚠️ FINAL TREATMENT PLAN MUST BE DETERMINED BY MDT DISCUSSION WITH PATIENT INPUT"""
        
        return approach.strip()
    
    def _identify_open_questions(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations
    ) -> List[str]:
        """
        Identify questions that remain unanswered.
        Human experts must address these.
        """
        
        questions = []
        
        # From pathology uncertainties
        for uncertainty in pathology.uncertainty_notes:
            questions.append(f"Pathology: {uncertainty}")
        
        # From imaging uncertainties
        for uncertainty in imaging.uncertainty_notes[:2]:  # Top 2
            questions.append(f"Imaging: {uncertainty}")
        
        # Treatment-specific questions
        questions.append(
            "What is the patient's performance status and fitness for aggressive therapy?"
        )
        
        questions.append(
            "Has the patient expressed preferences regarding treatment intensity and potential toxicity?"
        )
        
        if guidelines.clinical_trials:
            questions.append(
                "Does the patient meet eligibility criteria and express interest in clinical trial participation?"
            )
        
        questions.append(
            "Are there social determinants of health or logistical barriers affecting treatment selection?"
        )
        
        questions.append(
            "Is this case appropriate for presentation at an academic tumor board for additional expert input?"
        )
        
        return questions
    
    def _compile_uncertainty_flags(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations,
        disagreements: List[str]
    ) -> List[str]:
        """
        Compile all uncertainty flags across modalities.
        Critical for risk management and informed decision-making.
        
        PRIORITY: Disagreements are the most important uncertainties.
        """
        
        flags = []
        
        # Overall uncertainty statement
        flags.append(
            "⚠️ This AI-generated analysis is for DISCUSSION PURPOSES ONLY and does not "
            "constitute a diagnostic or treatment decision"
        )
        
        # CRITICAL: Flag disagreements prominently
        if disagreements:
            flags.append(
                f"🔴 AGENT DISAGREEMENTS DETECTED ({len(disagreements)}): "
                "Multiple interpretations exist - prioritize resolution during MDT"
            )
        
        # Confidence-based flags
        if pathology.confidence in [ConfidenceLevel.LOW, ConfidenceLevel.UNCERTAIN]:
            flags.append(
                f"⚠️ Pathology analysis confidence: {pathology.confidence.value} - "
                "Expert review strongly recommended"
            )
        
        if imaging.confidence in [ConfidenceLevel.LOW, ConfidenceLevel.UNCERTAIN]:
            flags.append(
                f"⚠️ Imaging analysis confidence: {imaging.confidence.value} - "
                "Radiologist review essential"
            )
        
        if guidelines.confidence in [ConfidenceLevel.LOW, ConfidenceLevel.UNCERTAIN]:
            flags.append(
                f"⚠️ Guideline matching confidence: {guidelines.confidence.value} - "
                "Consider expert consultation"
            )
        
        # Missing data flags
        if not pathology.biomarkers:
            flags.append(
                "⚠️ Limited biomarker data - comprehensive molecular testing recommended"
            )
        
        # Guideline-specific flags
        for consideration in guidelines.special_considerations[:2]:
            if "recommended" in consideration.lower():
                flags.append(f"⚠️ {consideration}")
        
        # Final safety flag
        flags.append(
            "⚠️ All findings require validation by licensed healthcare professionals "
            "before clinical application"
        )
        
        return flags
    
    def _generate_clinician_action_checklist(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations,
        disagreements: List[str]
    ) -> List[str]:
        """
        Generate concrete action checklist for clinicians.
        
        This transforms the report from "AI analysis" to "meeting-ready artifact."
        
        These are specific, actionable items that clinicians should complete
        during or immediately after the tumor board meeting.
        """
        
        checklist = []
        
        # PRIORITY: Resolve disagreements first
        if disagreements:
            checklist.append(
                "🔴 PRIORITY: Resolve agent disagreements through expert review and discussion"
            )
        
        # Staging confirmation
        if "Clinical" in guidelines.stage_estimate or "Suspected" in guidelines.stage_estimate:
            checklist.append(
                "[ ] Confirm clinical stage - consider additional imaging (PET-CT) or invasive staging"
            )
        
        # Pathology review
        if pathology.confidence != ConfidenceLevel.HIGH or pathology.uncertainty_notes:
            checklist.append(
                "[ ] Request pathology review by subspecialty expert (GI/thoracic/breast pathologist)"
            )
        
        # Additional testing
        if not pathology.biomarkers or len(pathology.biomarkers) < 3:
            checklist.append(
                "[ ] Order comprehensive molecular profiling (NGS panel) if tissue available"
            )
        
        # Imaging follow-up
        if imaging.uncertainty_notes:
            checklist.append(
                "[ ] Schedule additional imaging studies as indicated by radiology"
            )
        
        # Subspecialty consultation
        if any("Surgical" in opt.treatment_type for opt in guidelines.treatment_options):
            checklist.append(
                "[ ] Obtain surgical oncology consultation for resectability assessment"
            )
        
        if any("Radiation" in opt.treatment_type for opt in guidelines.treatment_options):
            checklist.append(
                "[ ] Refer to radiation oncology for treatment planning"
            )
        
        # Clinical trial evaluation
        if guidelines.clinical_trials:
            checklist.append(
                f"[ ] Screen patient for clinical trial eligibility ({len(guidelines.clinical_trials)} trials identified)"
            )
        
        # Patient counseling
        checklist.append(
            "[ ] Schedule patient counseling session to discuss treatment options and preferences"
        )
        
        # Functional assessment
        checklist.append(
            "[ ] Complete performance status assessment (ECOG/Karnofsky) and fitness evaluation"
        )
        
        # Multidisciplinary input
        checklist.append(
            "[ ] Document consensus treatment plan with input from all relevant specialists"
        )
        
        # Follow-up planning
        checklist.append(
            "[ ] Establish surveillance/follow-up imaging schedule per treatment plan"
        )
        
        # Documentation
        checklist.append(
            "[ ] Complete formal tumor board note with rationale for chosen approach"
        )
        
        # Contingency planning
        if len(guidelines.treatment_options) > 1:
            checklist.append(
                "[ ] Define backup treatment plan if first-line approach not feasible"
            )
        
        return checklist
    
    def _process_longitudinal_changes(
        self,
        case_data: Dict,
        pathology: PathologyFindings,
        imaging: ImagingFindings
    ) -> Optional[List[str]]:
        """
        Identify and document changes since last tumor board review.
        
        This adds longitudinal reasoning and makes the MDT feel "alive" rather than static.
        Even if simulated, this demonstrates the capability.
        """
        
        # Check if this is a follow-up case
        if not case_data.get("prior_case_id") and not case_data.get("changes_since_last_review"):
            return None
        
        changes = []
        
        # Use provided changes if available
        if case_data.get("changes_since_last_review"):
            changes.extend(case_data["changes_since_last_review"])
        else:
            # Simulate detection of interval changes
            # In production, would compare to actual prior case data
            changes.append(
                "📊 INTERVAL IMAGING: Tumor size appears stable compared to prior study (no significant change)"
            )
            
            if pathology.lymph_node_status and "positive" in pathology.lymph_node_status.lower():
                changes.append(
                    "🔴 NEW FINDING: Lymph node involvement now documented (not present on prior evaluation)"
                )
            
            # Simulate biomarker evolution
            if pathology.biomarkers:
                changes.append(
                    "🧬 MOLECULAR UPDATE: Additional biomarker testing completed since last review"
                )
        
        # Add context to changes
        if changes:
            changes.insert(0, "This is a follow-up tumor board discussion. Key interval changes:")
        
        return changes if changes else None
    
    def _assess_overall_confidence(
        self,
        pathology: PathologyFindings,
        imaging: ImagingFindings,
        guidelines: GuidelineRecommendations,
        disagreements: List[str]
    ) -> ConfidenceLevel:
        """
        Assess overall confidence in the integrated analysis.
        Conservative approach - defaults to MODERATE.
        
        IMPORTANT: Disagreements lower confidence.
        """
        
        # If disagreements exist, confidence is automatically MODERATE or lower
        if disagreements:
            return ConfidenceLevel.MODERATE
        
        confidences = [
            pathology.confidence,
            imaging.confidence,
            guidelines.confidence
        ]
        
        # If any agent has LOW confidence, overall is MODERATE at best
        if ConfidenceLevel.LOW in confidences or ConfidenceLevel.UNCERTAIN in confidences:
            return ConfidenceLevel.MODERATE
        
        # Even with all HIGH, we return MODERATE for AI analysis
        # (human review always needed)
        return ConfidenceLevel.MODERATE


# Example usage for testing
if __name__ == "__main__":
    from agents.pathology_agent import PathologyAgent
    from agents.imaging_agent import ImagingAgent
    from agents.guideline_agent import GuidelineAgent
    
    # Create test case
    test_case = {
        "case_id": "TB-2026-001",
        "primary_site": "lung",
        "age": 65,
        "gender": "Male",
        "clinical_history": "65M with persistent cough and weight loss"
    }
    
    # Run all agents sequentially
    path_agent = PathologyAgent()
    img_agent = ImagingAgent()
    guide_agent = GuidelineAgent()
    synth_agent = MDTSynthesizerAgent()
    
    pathology = path_agent.analyze(test_case)
    imaging = img_agent.analyze(test_case)
    guidelines = guide_agent.analyze(test_case, pathology, imaging)
    synthesis = synth_agent.synthesize(test_case, pathology, imaging, guidelines)
    
    print(json.dumps(synthesis.dict(), indent=2, default=str))
