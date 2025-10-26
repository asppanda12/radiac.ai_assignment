import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Add parent directory to path to import agent
sys.path.append(str(Path(__file__).parent.parent))
from src.agent import CampaignAgent

st.set_page_config(
    page_title="Campaign Agent UI",
    page_icon="🎯",
    layout="wide"
)

def load_example_brief():
    """Load an example brief for the demo."""
    example_path = Path(__file__).parent.parent / "examples" / "brief1.json"
    with open(example_path, "r") as f:
        return json.load(f)

def main():
    st.title("Ad Campaign Generator 🎯")
    st.write("Convert campaign briefs into structured ad campaign plans using AI.")

    # Initialize session state
    if "brief" not in st.session_state:
        st.session_state.brief = load_example_brief()

    # Sidebar for configuration
    with st.sidebar:
        st.subheader("Configuration")
        mock_llm = st.checkbox("Use Mock LLM (for testing)", value=False)
        
        st.subheader("Load Example")
        if st.button("Load Example Brief"):
            st.session_state.brief = load_example_brief()

    # Main content area - split into two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Campaign Brief")
        
        # Campaign ID
        campaign_id = st.text_input(
            "Campaign ID",
            value=st.session_state.brief["campaign_id"],
            help="Format: cmp_YYYY_MM_DD"
        )

        # Goal
        goal = st.text_area(
            "Campaign Goal",
            value=st.session_state.brief["goal"]
        )

        # Product Details
        st.write("Product Details")
        product_name = st.text_input(
            "Product Name",
            value=st.session_state.brief["product"]["name"]
        )
        product_category = st.text_input(
            "Product Category",
            value=st.session_state.brief["product"]["category"]
        )
        key_features = st.text_area(
            "Key Features (one per line)",
            value="\n".join(st.session_state.brief["product"]["key_features"])
        )
        price = st.text_input(
            "Price",
            value=st.session_state.brief["product"]["price"]
        )

        # Budget and Channels
        budget = st.number_input(
            "Budget",
            value=float(st.session_state.brief["budget"]),
            min_value=0.0
        )
        channels = st.multiselect(
            "Channels",
            options=["search", "social", "display", "video"],
            default=st.session_state.brief["channels"]
        )

        # Audience and Tone
        audience = st.text_area(
            "Audience Hints (one per line)",
            value="\n".join(st.session_state.brief["audience_hints"])
        )
        tone = st.text_input(
            "Tone",
            value=st.session_state.brief["tone"]
        )

        # Create brief dictionary
        brief = {
            "campaign_id": campaign_id,
            "goal": goal,
            "product": {
                "name": product_name,
                "category": product_category,
                "key_features": [f.strip() for f in key_features.split("\n") if f.strip()],
                "price": price
            },
            "budget": budget,
            "channels": channels,
            "audience_hints": [a.strip() for a in audience.split("\n") if a.strip()],
            "tone": tone
        }

        if st.button("Generate Campaign Plan"):
            try:
                agent = CampaignAgent(mock=mock_llm)
                with st.spinner("Generating campaign plan..."):
                    campaign = agent.process_brief(brief)
                st.session_state.campaign = campaign
                st.success("Campaign plan generated successfully!")
            except Exception as e:
                st.error(f"Error generating campaign plan: {str(e)}")

    with col2:
        st.subheader("Generated Campaign Plan")
        if "campaign" in st.session_state:
            # Display campaign overview
            st.write("### Campaign Overview")
            st.write(f"**Name:** {st.session_state.campaign['campaign_name']}")
            st.write(f"**Objective:** {st.session_state.campaign['objective']}")
            
            # Display budget breakdown
            st.write("### Budget Breakdown")
            budget_df = pd.DataFrame([
                {"Channel": k, "Budget": f"${v:,.2f}"}
                for k, v in st.session_state.campaign["budget_breakdown"].items()
            ])
            st.dataframe(budget_df, hide_index=True)

            # Display ad groups
            st.write("### Ad Groups")
            for i, ag in enumerate(st.session_state.campaign["ad_groups"], 1):
                with st.expander(f"Ad Group {i}: {ag['target']['age']} - {', '.join(ag['target']['behaviors'])}"):
                    for j, creative in enumerate(ag["creatives"], 1):
                        st.write(f"**Creative {j}**")
                        st.write(f"Headline: {creative['headline']}")
                        st.write(f"Body: {creative['body']}")
                        st.write(f"CTA: {creative['cta']}")
                        st.write(f"*Justification: {creative['justification']}*")
                        st.divider()

            # Display validation checks
            st.write("### Validation Checks")
            checks = st.session_state.campaign["checks"]
            st.write("✅" if checks["budget_sum_ok"] else "❌", "Budget sum valid")
            st.write("✅" if checks["required_fields_present"] else "❌", "Required fields present")

            # Add export button
            if st.download_button(
                "Download Campaign Plan",
                data=json.dumps(st.session_state.campaign, indent=2),
                file_name="campaign_plan.json",
                mime="application/json"
            ):
                st.success("Campaign plan downloaded!")

if __name__ == "__main__":
    main()
