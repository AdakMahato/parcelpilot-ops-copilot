# Architecture

## Agent Architecture
We use a single orchestrator agent powered by function-calling. This reduces the complexity and latency of multi-agent handoffs while preserving robustness.

## Tools
The agent has access to primary deterministic tools:
- `document_search`: Retrieves unstructured docs with explicit source filtering (excluding DEPRECATED).
- `operational_data_lookup`: Retrieves structured data (orders, tickets, accounts) from SQLite. Enforces account-level authorization.
- `sla_calculator`: Deterministic business logic calculating SLA targets.
- `prepare_escalation`: Mocks preparing a state-changing action.

## Retrieval & Source Precedence
We use ChromaDB for local vector embeddings. Post-retrieval filtering removes deprecated documents. Resulting chunks are sorted by `authority_level` (1=Agreements, 2=Current Policies, etc.).

## Authorization
Role-based restrictions (Support Agent vs Read-Only Analyst) and account-scoping (allowed_accounts array) are enforced at the backend tool layer, not the LLM prompt.

## Confirmation Workflow
`prepare_escalation` returns a structured JSON payload asking for confirmation, which the frontend intercepts to render a confirmation button. Only after explicit confirmation is `execute_escalation` triggered.
