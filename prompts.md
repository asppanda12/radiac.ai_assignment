# Prompt Design Documentation

## System Prompt Design

The system prompt is designed to:
1. Set clear expectations for output format and schema compliance
2. Emphasize validation requirements
3. Define guidelines for creative content and targeting
4. Establish professional tone and brand alignment

### Key Components

1. Role definition: Positions the model as an expert marketing campaign planner
2. Output requirements: Lists specific requirements for schema compliance and content quality
3. Guidelines: Provides detailed rules for budget, targeting, and creative content
4. Validation checklist: Ensures output meets all technical requirements

## User Prompt Design

The user prompt template is intentionally simple to:
1. Focus on the campaign brief data
2. Maintain consistency in output format
3. Allow flexibility in brief content

### Design Decisions

1. JSON format: Briefs are passed as structured JSON to ensure consistency
2. Multiple variants: Explicitly requests multiple ad variants to encourage diversity
3. Context preservation: Includes complete brief to maintain all context

## Known Failure Cases

1. Hallucination of Product Details
   - Symptom: Model may generate features not in the brief
   - Mitigation: Add explicit warning against inventing features
   - Future: Implement product KB for grounding

2. Budget Allocation Errors
   - Symptom: Rounding errors in budget breakdown
   - Mitigation: Added explicit validation
   - Future: Add specific rules for minimum allocations

3. Inconsistent Targeting
   - Symptom: Targeting may not align with audience hints
   - Mitigation: Added targeting validation step
   - Future: Develop targeting taxonomy

4. Creative Length Issues
   - Symptom: Ad copy may exceed platform limits
   - Mitigation: Add platform-specific length checks
   - Future: Implement platform-specific validators

## Future Improvements

1. Add example outputs in system prompt
2. Implement structured creative guidelines per channel
3. Add competitor awareness through KB integration
4. Develop channel-specific budget allocation rules
