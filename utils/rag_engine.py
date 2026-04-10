import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict

class MedicalRAGEngine:
    """
    Real RAG engine using Sentence-Transformers and FAISS.
    Replaces simulated knowledge lookups with semantic search.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        
    def build_index(self, knowledge_file: str):
        """Builds a vector index from a JSON knowledge file"""
        if not os.path.exists(knowledge_file):
            return
            
        with open(knowledge_file, 'r') as f:
            data = json.load(f)
            
        # Flatten knowledge into chunks
        chunks = []
        for site, types in data.items():
            for t_type, stages in types.items():
                for stage, details in stages.items():
                    text = f"Site: {site}. Type: {t_type}. Stage: {stage}. Treatment: {details['treatment']}. Options: {', '.join(details['options'])}"
                    chunks.append({
                        "text": text,
                        "metadata": details
                    })
        
        self.documents = chunks
        if not chunks:
            return
            
        embeddings = self.model.encode([c['text'] for c in chunks])
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(np.array(embeddings).astype('float32'))
        
    def query(self, query_text: str, k: int = 3) -> List[Dict]:
        """Performs semantic search for guidelines"""
        if self.index is None or not self.documents:
            return []
            
        query_vec = self.model.encode([query_text])
        distances, indices = self.index.search(np.array(query_vec).astype('float32'), k)
        
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.documents):
                results.append(self.documents[i]['metadata'])
        return results
