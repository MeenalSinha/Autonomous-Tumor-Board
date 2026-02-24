"""
Report Generator Utility
Creates professional PDF reports from tumor board analysis.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict
import os

from models.case_models import TumorBoardReport


class TumorBoardReportGenerator:
    """Generate professional PDF reports for tumor board cases"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#0d47a1'),
            spaceAfter=12,
            spaceBefore=12,
            borderPadding=5,
            borderColor=colors.HexColor('#0d47a1'),
            borderWidth=0,
            leftIndent=0
        ))
        
        # Warning style
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            alignment=TA_CENTER,
            spaceAfter=20,
            borderPadding=10,
            borderColor=colors.red,
            borderWidth=1
        ))
        
        # Agent output style
        self.styles.add(ParagraphStyle(
            name='AgentOutput',
            parent=self.styles['Normal'],
            fontSize=9,
            leftIndent=20,
            spaceAfter=6
        ))
    
    def generate_pdf(self, report: TumorBoardReport, output_path: str) -> str:
        """
        Generate PDF report from TumorBoardReport object.
        
        Args:
            report: TumorBoardReport object
            output_path: Path where PDF should be saved
            
        Returns:
            str: Path to generated PDF
        """
        
        # Create document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        story = []
        
        # Header
        story.extend(self._create_header(report))
        
        # Disclaimer (prominent)
        story.extend(self._create_disclaimer(report))
        
        # Executive Summary
        story.extend(self._create_executive_summary(report))
        
        # Case Information
        story.extend(self._create_case_info(report))
        
        # Agent Outputs (each on separate section)
        story.extend(self._create_pathology_section(report))
        story.extend(self._create_imaging_section(report))
        story.extend(self._create_guideline_section(report))
        story.extend(self._create_synthesis_section(report))
        
        # Footer
        story.extend(self._create_footer(report))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_header(self, report: TumorBoardReport) -> list:
        """Create document header"""
        elements = []
        
        title = Paragraph(
            "AUTONOMOUS TUMOR BOARD<br/>Draft Report for MDT Review",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Metadata table
        metadata = [
            ['Case ID:', report.case_id],
            ['Generated:', report.generated_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Status:', 'DRAFT - Requires Human Review']
        ]
        
        meta_table = Table(metadata, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_disclaimer(self, report: TumorBoardReport) -> list:
        """Create prominent disclaimer"""
        elements = []
        
        disclaimer_text = f"""⚠️ {report.disclaimer}
        
This AI-generated analysis is provided as a DISCUSSION TOOL for tumor board preparation.
It does NOT constitute medical advice, diagnosis, or treatment recommendations.
ALL findings require validation by licensed healthcare professionals."""
        
        disclaimer = Paragraph(disclaimer_text, self.styles['Warning'])
        elements.append(disclaimer)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_executive_summary(self, report: TumorBoardReport) -> list:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeader']))
        
        summary_text = report.synthesis.executive_summary.replace('\n\n', '<br/><br/>')
        summary = Paragraph(summary_text, self.styles['Normal'])
        elements.append(summary)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_case_info(self, report: TumorBoardReport) -> list:
        """Create case information section"""
        elements = []
        
        elements.append(Paragraph("CASE INFORMATION", self.styles['SectionHeader']))
        
        case_data = [
            ['Age:', f"{report.patient_info.age} years"],
            ['Gender:', report.patient_info.gender],
            ['Primary Site:', report.patient_info.primary_site],
            ['Clinical History:', report.patient_info.clinical_history]
        ]
        
        case_table = Table(case_data, colWidths=[1.5*inch, 5*inch])
        case_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ]))
        
        elements.append(case_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_pathology_section(self, report: TumorBoardReport) -> list:
        """Create pathology findings section"""
        elements = []
        
        elements.append(Paragraph(
            f"PATHOLOGY FINDINGS (Agent A - Confidence: {report.pathology.confidence.value})",
            self.styles['SectionHeader']
        ))
        
        # Key findings
        path_data = [
            ['Tumor Type:', report.pathology.tumor_type],
            ['Grade:', report.pathology.histologic_grade],
            ['Lymph Nodes:', report.pathology.lymph_node_status or 'N/A'],
            ['Margins:', report.pathology.margins or 'N/A']
        ]
        
        path_table = Table(path_data, colWidths=[1.5*inch, 5*inch])
        path_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(path_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Biomarkers
        if report.pathology.biomarkers:
            elements.append(Paragraph("Biomarker Profile:", self.styles['Heading4']))
            biomarker_text = "<br/>".join([
                f"• {k}: {v}" for k, v in report.pathology.biomarkers.items()
            ])
            elements.append(Paragraph(biomarker_text, self.styles['AgentOutput']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_imaging_section(self, report: TumorBoardReport) -> list:
        """Create imaging findings section"""
        elements = []
        
        elements.append(Paragraph(
            f"IMAGING FINDINGS (Agent B - Confidence: {report.imaging.confidence.value})",
            self.styles['SectionHeader']
        ))
        
        size_str = f"{report.imaging.tumor_size_cm[0]:.1f} x {report.imaging.tumor_size_cm[1]:.1f} x {report.imaging.tumor_size_cm[2]:.1f} cm"
        
        img_data = [
            ['Modality:', report.imaging.modality],
            ['Location:', report.imaging.tumor_location],
            ['Size:', size_str],
            ['Lymph Nodes:', report.imaging.lymph_nodes]
        ]
        
        img_table = Table(img_data, colWidths=[1.5*inch, 5*inch])
        img_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(img_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_guideline_section(self, report: TumorBoardReport) -> list:
        """Create guideline recommendations section"""
        elements = []
        
        elements.append(Paragraph(
            f"GUIDELINE-BASED RECOMMENDATIONS (Agent C - Confidence: {report.guidelines.confidence.value})",
            self.styles['SectionHeader']
        ))
        
        elements.append(Paragraph(f"<b>Estimated Stage:</b> {report.guidelines.stage_estimate}", 
                                self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Treatment options
        elements.append(Paragraph("<b>Treatment Options:</b>", self.styles['Heading4']))
        
        for i, option in enumerate(report.guidelines.treatment_options, 1):
            option_text = f"""<b>{i}. {option.treatment_type}</b><br/>
            {option.description}<br/>
            <i>Evidence Level: {option.evidence_level}</i>"""
            
            elements.append(Paragraph(option_text, self.styles['AgentOutput']))
            elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_synthesis_section(self, report: TumorBoardReport) -> list:
        """Create MDT synthesis section"""
        elements = []
        
        elements.append(Paragraph(
            f"MDT SYNTHESIS (Agent D - Confidence: {report.synthesis.confidence.value})",
            self.styles['SectionHeader']
        ))
        
        # Changes since last review (if applicable)
        if report.synthesis.changes_since_last_review:
            elements.append(Paragraph("<b>Changes Since Last Review:</b>", self.styles['Heading4']))
            
            for change in report.synthesis.changes_since_last_review:
                change_clean = change.replace("📊", "").replace("🔴", "").replace("🧬", "").strip()
                elements.append(Paragraph(f"• {change_clean}", self.styles['AgentOutput']))
            
            elements.append(Spacer(1, 0.1*inch))
        
        # Discussion points
        elements.append(Paragraph("<b>Key Discussion Points:</b>", self.styles['Heading4']))
        
        for point in report.synthesis.discussion_points:
            # Remove emoji for PDF
            point_clean = point.replace("🔴", "").strip()
            if "DISAGREEMENT" in point:
                point_styled = f"<b>[DISAGREEMENT]</b> {point_clean.replace('DISAGREEMENT:', '')}"
                elements.append(Paragraph(f"• {point_styled}", self.styles['AgentOutput']))
            else:
                elements.append(Paragraph(f"• {point_clean}", self.styles['AgentOutput']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Clinician Action Checklist
        elements.append(Paragraph("<b>Clinician Action Checklist:</b>", self.styles['Heading4']))
        elements.append(Paragraph(
            "The following action items should be completed during or after tumor board:",
            self.styles['Normal']
        ))
        
        for action in report.synthesis.clinician_action_checklist:
            # Remove emoji
            action_clean = action.replace("🔴", "").replace("[ ]", "☐").strip()
            if "PRIORITY" in action:
                elements.append(Paragraph(f"<b>{action_clean}</b>", self.styles['AgentOutput']))
            else:
                elements.append(Paragraph(f"{action_clean}", self.styles['AgentOutput']))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Open questions
        elements.append(Paragraph("<b>Open Questions for MDT:</b>", self.styles['Heading4']))
        
        for question in report.synthesis.open_questions[:5]:  # Top 5
            elements.append(Paragraph(f"• {question}", self.styles['AgentOutput']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_footer(self, report: TumorBoardReport) -> list:
        """Create document footer"""
        elements = []
        
        elements.append(PageBreak())
        
        footer_text = """<b>IMPORTANT DISCLAIMERS AND LIMITATIONS</b><br/><br/>
        
This document was generated by an AI-assisted tumor board preparation system and is intended
SOLELY as a discussion tool for multidisciplinary team meetings.<br/><br/>

<b>This system does NOT:</b><br/>
• Make diagnostic determinations<br/>
• Provide treatment recommendations<br/>
• Replace clinical judgment<br/>
• Substitute for tumor board discussion<br/><br/>

<b>All findings in this report require:</b><br/>
• Validation by licensed healthcare professionals<br/>
• Review by subspecialty experts<br/>
• Discussion at formal tumor board<br/>
• Patient counseling and shared decision-making<br/><br/>

<b>Human Review Status: REQUIRED</b><br/><br/>

Generated by Autonomous Tumor Board System v1.0<br/>
For research and educational purposes only.
        """
        
        footer = Paragraph(footer_text, self.styles['Normal'])
        elements.append(footer)
        
        return elements


# Testing
if __name__ == "__main__":
    print("Report generator utility loaded.")
    print("Use TumorBoardReportGenerator.generate_pdf() to create reports.")
