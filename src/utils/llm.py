import os
from typing import Dict, Optional

from openai import OpenAI

def get_llm_response(
    system_prompt: str,
    user_prompt: str,
    mock: bool = False
) -> Dict:
    """Get response from the LLM.
    
    Args:
        system_prompt (str): The system prompt
        user_prompt (str): The user prompt
        mock (bool): Whether to return mock responses
        
    Returns:
        Dict: The LLM response parsed as JSON
    """
    if mock:
        return _get_mock_response()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-4"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content

def _get_mock_response() -> Dict:
    """Return a mock campaign response for testing."""
    return {
        "campaign_id": "cmp_2025_09_01",
        "campaign_name": "FocusFlow Trial Push Sep2025",
        "objective": "trial_signups",
        "total_budget": 5000,
        "budget_breakdown": {
            "search": 3000,
            "social": 2000
        },
        "ad_groups": [
            {
                "id": "ag_1",
                "target": {
                    "age": "25-40",
                    "behaviors": ["remote work", "productivity apps"]
                },
                "creatives": [
                    {
                        "id": "c_1a",
                        "headline": "Get More Done — Free 14-Day Trial",
                        "body": "AI task prioritization that fits your calendar. Try FocusFlow free for 14 days.",
                        "cta": "Start Free Trial",
                        "justification": "Highlights trial + AI feature; concise for search."
                    }
                ]
            }
        ],
        "checks": {
            "budget_sum_ok": True,
            "required_fields_present": True
        }
    }
