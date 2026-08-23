# Product Strategy

## Problem Addressed
Support agents at ParcelPilot need rapid, accurate answers blending structured data (orders, SLAs) and unstructured data (agreements, SOPs) without hallucinating business rules.

## Proactive Issue Detection
The Issue Intelligence Dashboard (available at `/api/dashboard`) queries the structured SQLite database to proactively flag SLA breaches and group related tickets (e.g., the CSV upload failures).

## Trust & Reliability Strategy
- **Deterministic Rules**: SLA calculations and fee validations are hard-coded in Python, not LLM-guessed.
- **Source Filtering**: Deprecated documents are forcefully excluded by the retrieval tool before the LLM sees them.

## Future Roadmap
- Integration with live Zendesk/Salesforce APIs.
- Real-time event streaming for SLA updates.
