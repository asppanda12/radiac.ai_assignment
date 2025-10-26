import json
from pathlib import Path
from typing import Dict, Optional

from src.models.brief import CampaignBrief
from src.models.campaign import Campaign
from src.utils.llm import get_llm_response
from src.utils.metrics import MetricsLogger
from src.utils.scorer import CreativeScorer
from src.validators.checks import validate_campaign

class CampaignAgent:
    def __init__(self, mock: bool = False, kb_path: Optional[str] = None):
        """Initialize the Campaign Agent.
        
        Args:
            mock (bool): Whether to use mock responses for testing
            kb_path (str, optional): Path to the knowledge base file
        """
        self.mock = mock
        self.kb_path = kb_path or str(Path(__file__).parent.parent / "kb" / "product_data.json")
        self.metrics = MetricsLogger()
        self.scorer = CreativeScorer(self.kb_path)
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load system and user prompts from files."""
        prompts_dir = Path(__file__).parent / "prompts"
        
        with open(prompts_dir / "system.py", "r") as f:
            self.system_prompt = f.read()
            
        with open(prompts_dir / "user.py", "r") as f:
            self.user_prompt_template = f.read()

    def process_brief(self, brief: Dict) -> Dict:
        """Process a campaign brief and generate a campaign plan.
        
        Args:
            brief (Dict): The campaign brief in JSON format
            
        Returns:
            Dict: The generated campaign plan
        """
        self.metrics.reset_metrics()
        self.metrics.start_processing()
        
        try:
            # Validate input brief
            validated_brief = CampaignBrief(**brief)
            
            # Format user prompt with brief details
            user_prompt = self.user_prompt_template.format(
                brief=json.dumps(validated_brief.model_dump(), indent=2)
            )
            
            # Get response from LLM
            response = get_llm_response(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                mock=self.mock
            )
            
            # Parse and validate response
            campaign = Campaign(**response)
            
            # Run consistency checks
            validate_campaign(campaign, validated_brief)
            
            # Score creatives and add scores to response
            for ad_group in campaign.ad_groups:
                for creative in ad_group.creatives:
                    score = self.scorer.score_creative(
                        creative.model_dump(),
                        validated_brief.product.name
                    )
                    creative_dict = creative.model_dump()
                    creative_dict["score"] = score
                    
                    # Check for potential hallucinations
                    if any(
                        feature.lower() not in creative.body.lower() and 
                        feature.lower() not in creative.headline.lower()
                        for feature in validated_brief.product.key_features
                    ):
                        self.metrics.log_hallucination(
                            f"Creative {creative.id} may contain hallucinated features",
                            confidence=0.8
                        )
            
            self.metrics.end_processing(success=True)
            campaign_dict = campaign.model_dump()
            campaign_dict["metrics"] = self.metrics.get_metrics()
            
            return campaign_dict
            
        except Exception as e:
            self.metrics.log_validation_error(str(e))
            self.metrics.end_processing(success=False)
            raise

    def process_brief_from_file(self, brief_path: str) -> Dict:
        """Process a campaign brief from a JSON file.
        
        Args:
            brief_path (str): Path to the JSON brief file
            
        Returns:
            Dict: The generated campaign plan
        """
        with open(brief_path, "r") as f:
            brief = json.load(f)
        return self.process_brief(brief)
