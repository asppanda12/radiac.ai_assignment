from src.models.brief import CampaignBrief
from src.models.campaign import Campaign

def validate_campaign(campaign: Campaign, brief: CampaignBrief) -> None:
    """Validate campaign output against the input brief.
    
    Args:
        campaign (Campaign): The generated campaign
        brief (CampaignBrief): The input brief
        
    Raises:
        ValueError: If validation fails
    """
    # Validate campaign ID matches
    if campaign.campaign_id != brief.campaign_id:
        raise ValueError("Campaign ID mismatch")
    
    # Validate total budget matches
    if campaign.total_budget != brief.budget:
        raise ValueError("Total budget mismatch")
    
    # Validate budget breakdown sum
    budget_sum = sum(campaign.budget_breakdown.values())
    if abs(budget_sum - campaign.total_budget) > 0.01:  # Allow for small float differences
        raise ValueError("Budget breakdown sum doesn't match total budget")
    
    # Validate all channels from brief are in budget breakdown
    for channel in brief.channels:
        if channel not in campaign.budget_breakdown:
            raise ValueError(f"Channel {channel} from brief missing in budget breakdown")
    
    # Validate ad groups have unique IDs
    ad_group_ids = [ag.id for ag in campaign.ad_groups]
    if len(ad_group_ids) != len(set(ad_group_ids)):
        raise ValueError("Duplicate ad group IDs found")
    
    # Validate creatives have unique IDs within each ad group
    for ad_group in campaign.ad_groups:
        creative_ids = [c.id for c in ad_group.creatives]
        if len(creative_ids) != len(set(creative_ids)):
            raise ValueError(f"Duplicate creative IDs found in ad group {ad_group.id}")
    
    # Update checks in campaign
    campaign.checks.budget_sum_ok = True
    campaign.checks.required_fields_present = True
