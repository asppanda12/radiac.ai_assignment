from typing import Dict, List
import json
from pathlib import Path

class CreativeScorer:
    def __init__(self, kb_path: str = None):
        """Initialize the creative scorer with knowledge base data."""
        self.kb = self._load_kb(kb_path) if kb_path else {}
        
    def _load_kb(self, kb_path: str) -> Dict:
        """Load the knowledge base data."""
        with open(kb_path, 'r') as f:
            return json.load(f)
    
    def score_creative(self, creative: Dict, product_name: str) -> float:
        """Score a creative based on various heuristics.
        
        Args:
            creative: The creative to score
            product_name: Name of the product
            
        Returns:
            float: Score between 0 and 1
        """
        scores = []
        
        # 1. Feature effectiveness score
        if product_name in self.kb.get("products", {}):
            features = self.kb["products"][product_name]["features"]
            mentioned_features = [
                f for f in features
                if f.lower() in creative["body"].lower() or f.lower() in creative["headline"].lower()
            ]
            if mentioned_features:
                feature_scores = [features[f]["effectiveness"] for f in mentioned_features]
                scores.append(sum(feature_scores) / len(feature_scores))
        
        # 2. Length appropriateness score
        headline_length = len(creative["headline"])
        body_length = len(creative["body"])
        
        # Ideal lengths based on common platform limits
        if 30 <= headline_length <= 65:  # Good headline length for most platforms
            scores.append(1.0)
        elif headline_length < 30:
            scores.append(0.7)
        else:
            scores.append(0.5)
            
        if 60 <= body_length <= 180:  # Good body length for most platforms
            scores.append(1.0)
        elif body_length < 60:
            scores.append(0.7)
        else:
            scores.append(0.5)
        
        # 3. CTA clarity score
        cta_length = len(creative["cta"])
        if 2 <= len(creative["cta"].split()) <= 4:  # Ideal CTA word count
            scores.append(1.0)
        else:
            scores.append(0.6)
        
        # 4. Justification completeness
        if len(creative["justification"].split()) >= 5:
            scores.append(1.0)
        else:
            scores.append(0.7)
        
        return sum(scores) / len(scores) if scores else 0.5
