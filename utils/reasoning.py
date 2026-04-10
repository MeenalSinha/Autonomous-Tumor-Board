import json
import os
from typing import Dict, List, Any

class MedicalReasoningEngine:
    """
    Core reasoning engine for agents to use.
    Provides RAG-like capabilities over local medical knowledge.
    """
    
    def __init__(self, knowledge_dir: str = "knowledge_base"):
        self.knowledge_dir = knowledge_dir
        self.guidelines = self._load_knowledge("guidelines.json")
        
    def _load_knowledge(self, filename: str) -> Dict:
        path = os.path.join(self.knowledge_dir, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}
        
    def match_guidelines(self, site: str, tumor_type: str, stage: str) -> List[Dict]:
        """Matches clinical findings against guidelines"""
        # Search logic over self.guidelines
        matched_options = []
        site_key = f"{site.lower()}_nccn"
        
        if site_key in self.guidelines:
            site_data = self.guidelines[site_key]
            # Simple fuzzy matching for tumor type
            for t_type, stages in site_data.items():
                if t_type in tumor_type.lower():
                    # Match stage
                    stage_key = "stage_i" if "Stage I" in stage else "stage_iii" if "Stage III" in stage else None
                    if stage_key and stage_key in stages:
                        matched_options.append(stages[stage_key])
                        
        return matched_options

    def analyze_biomarkers(self, site: str, findings: Dict) -> Dict[str, str]:
        """Validates biomarker relevance for specific sites"""
        # In production this would use a reference ontology
        return findings
