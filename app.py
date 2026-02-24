"""
Streamlit UI for Autonomous Tumor Board System
User-friendly interface for clinicians to submit cases and review reports.
"""

import streamlit as st
import json
import os
from datetime import datetime
import time

from models.case_models import PatientCase
from orchestrator import TumorBoardOrchestrator
from utils.report_generator import TumorBoardReportGenerator


# Page configuration
st.set_page_config(
    page_title="Autonomous Tumor Board",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1a237e;
        text-align: center;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    .agent-output {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'report' not in st.session_state:
        st.session_state.report = None
    if 'case_id' not in st.session_state:
        st.session_state.case_id = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False


def main():
    """Main application"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Autonomous Tumor Board</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">AI-Assisted Multidisciplinary Tumor Board Preparation</p>', unsafe_allow_html=True)
    
    # Critical disclaimer
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ IMPORTANT DISCLAIMER</h3>
        <p><strong>This system is a DRAFT PREPARATION TOOL ONLY</strong></p>
        <ul>
            <li>Does NOT make diagnostic or treatment decisions</li>
            <li>REQUIRES human clinician review</li>
            <li>NOT a substitute for multidisciplinary team discussion</li>
            <li>For educational and research purposes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            ["Submit Case", "View Report", "System Info", "About"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### Time Comparison")
        st.metric("Manual MDT Prep", "5-10 days")
        st.metric("AI-Assisted", "< 5 seconds", delta="-99.9%")
    
    # Main content based on selected page
    if page == "Submit Case":
        show_submit_case_page()
    elif page == "View Report":
        show_view_report_page()
    elif page == "System Info":
        show_system_info_page()
    else:
        show_about_page()


def show_submit_case_page():
    """Show case submission form"""
    
    st.header("📋 Submit New Case")
    
    st.markdown("""
    Enter de-identified patient information below. The system will analyze the case 
    using multiple AI agents and generate a draft tumor board report.
    """)
    
    with st.form("case_submission_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=65, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        with col2:
            primary_site = st.selectbox(
                "Primary Site",
                ["lung", "breast", "colon", "pancreas", "liver", "prostate", "stomach", "other"]
            )
        
        clinical_history = st.text_area(
            "Clinical History",
            height=150,
            placeholder="Enter patient's clinical history, symptoms, and relevant medical background..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit_button = st.form_submit_button("🚀 Process Case", type="primary")
        
        with col2:
            clear_button = st.form_submit_button("Clear")
    
    if submit_button:
        if not clinical_history:
            st.error("Please provide clinical history")
        else:
            process_case(age, gender, primary_site, clinical_history)
    
    if clear_button:
        st.session_state.report = None
        st.session_state.case_id = None
        st.rerun()


def process_case(age: int, gender: str, primary_site: str, clinical_history: str):
    """Process a case through the orchestrator"""
    
    # Generate case ID
    case_id = f"TB-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Create patient case
        patient_case = PatientCase(
            case_id=case_id,
            age=age,
            gender=gender,
            primary_site=primary_site,
            clinical_history=clinical_history
        )
        
        # Initialize orchestrator
        orchestrator = TumorBoardOrchestrator()
        
        # Process each agent with progress updates
        status_text.text("🔬 Running Pathology Agent...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.text("📊 Running Imaging Agent...")
        progress_bar.progress(50)
        time.sleep(0.5)
        
        status_text.text("📚 Running Guideline Agent...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        status_text.text("🔄 Synthesizing MDT Report...")
        progress_bar.progress(90)
        
        # Process case
        report = orchestrator.process_case(patient_case)
        
        # Generate PDF
        status_text.text("📄 Generating PDF Report...")
        os.makedirs("data/outputs", exist_ok=True)
        pdf_path = f"data/outputs/{case_id}_report.pdf"
        report_generator = TumorBoardReportGenerator()
        report_generator.generate_pdf(report, pdf_path)
        
        progress_bar.progress(100)
        status_text.text("✅ Processing Complete!")
        
        # Save to session state
        st.session_state.report = report
        st.session_state.case_id = case_id
        
        # Show success message
        st.success(f"✅ Case {case_id} processed successfully!")
        
        # Get execution summary
        exec_summary = orchestrator.get_execution_summary()
        
        st.markdown(f"""
        <div class="success-box">
            <h4>Processing Complete</h4>
            <p><strong>Case ID:</strong> {case_id}</p>
            <p><strong>Total Time:</strong> {exec_summary['total_time_seconds']} seconds</p>
            <p><strong>Comparison:</strong> Manual MDT prep would take 5-10 days</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-switch to report view
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Error processing case: {str(e)}")


def show_view_report_page():
    """Show generated report"""
    
    st.header("📊 Tumor Board Report")
    
    if st.session_state.report is None:
        st.info("No report available. Please submit a case first.")
        return
    
    report = st.session_state.report
    
    # Report header
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Case ID", report.case_id)
    with col2:
        st.metric("Stage", report.guidelines.stage_estimate.split('(')[0].strip())
    with col3:
        st.metric("Confidence", report.synthesis.confidence.value)
    
    # Tabs for different sections
    tabs = st.tabs([
        "📝 Executive Summary",
        "🔬 Pathology",
        "📊 Imaging",
        "📚 Guidelines",
        "🔄 Synthesis",
        "📄 Full Report"
    ])
    
    # Executive Summary Tab
    with tabs[0]:
        st.markdown("### Executive Summary")
        st.markdown(report.synthesis.executive_summary)
        
        st.markdown("### Key Findings")
        for key, value in report.synthesis.key_findings.items():
            st.markdown(f"**{key.replace('_', ' ')}:** {value}")
    
    # Pathology Tab
    with tabs[1]:
        st.markdown(f"### Pathology Findings")
        
        # Confidence and Evidence Banner
        col1, col2 = st.columns(2)
        with col1:
            confidence_color = {
                "High": "🟢",
                "Moderate": "🟡", 
                "Low": "🔴",
                "Uncertain": "⚪"
            }
            st.metric(
                "Confidence Level",
                f"{confidence_color.get(report.pathology.confidence.value, '⚪')} {report.pathology.confidence.value}"
            )
        with col2:
            st.metric("Evidence Source", report.pathology.evidence_strength)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Tumor Type:** {report.pathology.tumor_type}")
            st.markdown(f"**Grade:** {report.pathology.histologic_grade}")
        with col2:
            st.markdown(f"**Lymph Nodes:** {report.pathology.lymph_node_status}")
            st.markdown(f"**Margins:** {report.pathology.margins}")
        
        st.markdown("#### Biomarkers")
        if report.pathology.biomarkers:
            for marker, value in report.pathology.biomarkers.items():
                st.markdown(f"- **{marker}:** {value}")
        
        st.markdown("#### Clinical Significance")
        st.info(report.pathology.clinical_significance)
        
        if report.pathology.uncertainty_notes:
            st.warning("**Uncertainties:**")
            for note in report.pathology.uncertainty_notes:
                st.markdown(f"- {note}")
    
    # Imaging Tab
    with tabs[2]:
        st.markdown(f"### Imaging Findings")
        
        # Confidence and Evidence Banner
        col1, col2 = st.columns(2)
        with col1:
            confidence_color = {
                "High": "🟢",
                "Moderate": "🟡",
                "Low": "🔴",
                "Uncertain": "⚪"
            }
            st.metric(
                "Confidence Level",
                f"{confidence_color.get(report.imaging.confidence.value, '⚪')} {report.imaging.confidence.value}"
            )
        with col2:
            st.metric("Evidence Source", report.imaging.evidence_strength)
        
        st.markdown("---")
        
        st.markdown(f"**Modality:** {report.imaging.modality}")
        st.markdown(f"**Location:** {report.imaging.tumor_location}")
        st.markdown(f"**Size:** {report.imaging.tumor_size_cm[0]:.1f} x {report.imaging.tumor_size_cm[1]:.1f} x {report.imaging.tumor_size_cm[2]:.1f} cm")
        
        st.markdown("#### Staging Indicators")
        for key, value in report.imaging.staging_indicators.items():
            st.markdown(f"- **{key.replace('_', ' ')}:** {value}")
        
        st.markdown("#### Key Observations")
        for obs in report.imaging.key_observations:
            st.markdown(f"- {obs}")
    
    # Guidelines Tab
    with tabs[3]:
        st.markdown(f"### Guideline Recommendations")
        
        # Confidence and Evidence Banner
        col1, col2 = st.columns(2)
        with col1:
            confidence_color = {
                "High": "🟢",
                "Moderate": "🟡",
                "Low": "🔴",
                "Uncertain": "⚪"
            }
            st.metric(
                "Confidence Level",
                f"{confidence_color.get(report.guidelines.confidence.value, '⚪')} {report.guidelines.confidence.value}"
            )
        with col2:
            st.metric("Evidence Source", report.guidelines.evidence_strength)
        
        st.markdown("---")
        
        st.markdown(f"**Estimated Stage:** {report.guidelines.stage_estimate}")
        
        st.markdown("#### Treatment Options")
        for i, option in enumerate(report.guidelines.treatment_options, 1):
            with st.expander(f"{i}. {option.treatment_type} ({option.evidence_level})"):
                st.markdown(f"**Description:** {option.description}")
                st.markdown(f"**Reference:** {option.guideline_reference}")
                
                st.markdown("**Considerations:**")
                for consideration in option.considerations:
                    st.markdown(f"- {consideration}")
        
        if report.guidelines.clinical_trials:
            st.markdown("#### Relevant Clinical Trials")
            for trial in report.guidelines.clinical_trials:
                st.markdown(f"- {trial}")
    
    # Synthesis Tab
    with tabs[4]:
        st.markdown(f"### MDT Synthesis (Confidence: {report.synthesis.confidence.value})")
        
        # Changes since last review (if applicable)
        if report.synthesis.changes_since_last_review:
            st.markdown("#### 📅 Changes Since Last Review")
            st.info("Longitudinal tracking demonstrates disease evolution over time")
            for change in report.synthesis.changes_since_last_review:
                st.markdown(f"{change}")
            st.markdown("---")
        
        st.markdown("#### Discussion Points")
        for point in report.synthesis.discussion_points:
            # Highlight disagreements in red
            if "DISAGREEMENT" in point:
                st.error(point)
            else:
                st.info(point)
        
        st.markdown("#### 🎯 Clinician Action Checklist")
        st.success("**Meeting-Ready Action Items:**")
        for action in report.synthesis.clinician_action_checklist:
            if "PRIORITY" in action:
                st.markdown(f"**{action}**")
            else:
                st.markdown(action)
        
        st.markdown("---")
        
        st.markdown("#### Open Questions for MDT")
        for question in report.synthesis.open_questions:
            st.markdown(f"❓ {question}")
        
        st.markdown("#### Uncertainty Flags")
        for flag in report.synthesis.uncertainty_flags:
            if "DISAGREEMENT" in flag:
                st.error(flag)
            else:
                st.warning(flag)
    
    # Full Report Tab
    with tabs[5]:
        st.markdown("### Complete Report (JSON)")
        st.json(report.dict())
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # JSON download
            json_str = json.dumps(report.dict(), indent=2, default=str)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"{report.case_id}_report.json",
                mime="application/json"
            )
        
        with col2:
            # PDF download
            pdf_path = f"data/outputs/{report.case_id}_report.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF",
                        data=f,
                        file_name=f"{report.case_id}_report.pdf",
                        mime="application/pdf"
                    )


def show_system_info_page():
    """Show system information"""
    
    st.header("🤖 System Information")
    
    st.markdown("### Multi-Agent Architecture")
    
    agents = [
        {
            "name": "Agent A: Pathology Agent",
            "model": "MedGemma 4B (Vision-Heavy)",
            "role": "Analyzes histopathology findings, tumor grading, biomarkers"
        },
        {
            "name": "Agent B: Imaging Agent",
            "model": "MedGemma 1.5 (Multimodal Reasoning)",
            "role": "Analyzes medical imaging (CT/MRI), staging, spread assessment"
        },
        {
            "name": "Agent C: Guideline Agent",
            "model": "MedGemma 27B (Reasoning-Heavy)",
            "role": "Matches cases to clinical guidelines, identifies treatment options"
        },
        {
            "name": "Agent D: MDT Synthesizer",
            "model": "MedGemma 27B (Coordination)",
            "role": "Synthesizes all findings into cohesive tumor board report"
        }
    ]
    
    for agent in agents:
        with st.expander(agent["name"]):
            st.markdown(f"**Model:** {agent['model']}")
            st.markdown(f"**Role:** {agent['role']}")
    
    st.markdown("### Key Features")
    
    features = {
        "Multi-Agent Simulation": "✅ Separate specialized agents for each modality",
        "MDT-Style Reports": "✅ Professional tumor board documentation",
        "Safety Features": "✅ Disclaimers, confidence scoring, human-in-the-loop",
        "Intermediate Reasoning": "✅ Visible agent outputs and decision rationale",
        "Guideline Grounding": "✅ Evidence-based recommendations with citations",
        "Uncertainty Awareness": "✅ Explicit confidence levels and open questions",
        "Offline Capable": "✅ No cloud dependency required",
        "Structured Outputs": "✅ JSON and PDF reports",
        "Time Savings": "✅ Minutes vs. days for MDT preparation"
    }
    
    col1, col2 = st.columns(2)
    items = list(features.items())
    mid = len(items) // 2
    
    with col1:
        for feature, status in items[:mid]:
            st.markdown(f"**{feature}**")
            st.markdown(status)
            st.markdown("")
    
    with col2:
        for feature, status in items[mid:]:
            st.markdown(f"**{feature}**")
            st.markdown(status)
            st.markdown("")


def show_about_page():
    """Show about page"""
    
    st.header("ℹ️ About")
    
    st.markdown("""
    ### Autonomous Tumor Board System
    
    **What it does:**  
    Simulates a multidisciplinary cancer team meeting using multiple AI "agents" to prepare 
    draft tumor board reports in minutes instead of weeks.
    
    **How it works:**
    - One AI analyzes pathology findings
    - Another analyzes medical imaging  
    - Another checks treatment guidelines
    - Together, they create a review-ready report for doctors
    
    **Why it matters:**  
    Tumor board meetings are slow, expensive, and unavailable in many hospitals. 
    This system doesn't replace doctors — it prepares the groundwork for them.
    
    ### Use Cases
    - Preparing tumor board materials in under-resourced hospitals
    - Accelerating case preparation for experienced MDT teams
    - Educational tool for medical training
    - Research into AI-assisted clinical workflows
    
    ### Tech Stack
    - **Models:** MedGemma (4B, 1.5, 27B) - simulated
    - **Backend:** FastAPI
    - **Frontend:** Streamlit
    - **Architecture:** Multi-agent orchestration
    - **Output:** JSON + PDF reports
    
    ### Safety & Ethics
    This system is designed with patient safety as the top priority:
    - No autonomous medical decisions
    - Mandatory human review
    - Transparent reasoning
    - Uncertainty flagging
    - Evidence-based recommendations
    
    ### Disclaimer
    This is a demonstration/educational system. It is NOT approved for clinical use 
    and does NOT provide medical advice, diagnosis, or treatment recommendations.
    
    ---
    
    **Version:** 1.0.0  
    **Purpose:** Educational & Research  
    **License:** Demo/Competition Project
    """)


if __name__ == "__main__":
    main()
