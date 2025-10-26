import json
from pathlib import Path

import pytest

from src.agent import CampaignAgent
from src.models.brief import CampaignBrief
from src.models.campaign import Campaign

@pytest.fixture
def example_brief():
    brief_path = Path(__file__).parent.parent / "examples" / "brief1.json"
    with open(brief_path, "r") as f:
        return json.load(f)

def test_campaign_creation(example_brief):
    # Initialize agent with mock LLM
    agent = CampaignAgent(mock=True)
    
    # Process brief
    campaign = agent.process_brief(example_brief)
    
    # Validate campaign matches brief
    assert campaign["campaign_id"] == example_brief["campaign_id"]
    assert campaign["total_budget"] == example_brief["budget"]
    
    # Validate budget breakdown
    budget_sum = sum(campaign["budget_breakdown"].values())
    assert abs(budget_sum - campaign["total_budget"]) < 0.01
    
    # Validate all channels are present
    for channel in example_brief["channels"]:
        assert channel in campaign["budget_breakdown"]
    
    # Validate ad groups and creatives
    assert len(campaign["ad_groups"]) > 0
    for ad_group in campaign["ad_groups"]:
        assert len(ad_group["creatives"]) > 0
        
    # Validate checks passed
    assert campaign["checks"]["budget_sum_ok"]
    assert campaign["checks"]["required_fields_present"]
