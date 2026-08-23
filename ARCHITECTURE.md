# ParcelPilot Ops Copilot Architecture

## 1. System Architecture
The application follows a standard React + FastAPI architecture:
- **Frontend**: Next.js (React) application, styling with Tailwind CSS, utilizing `react-markdown` for rendering LLM outputs.
- **Backend**: FastAPI providing REST endpoints (`/api/chat`, `/api/dashboard`, `/api/tickets`, etc.).
- **Persistence**: SQLite (via SQLAlchemy) for relational operational data (Orders, Tickets, Accounts) and ChromaDB for vector-based document retrieval.

## 2. Agent Design
The core agent is powered by **Gemini 3.7 Flash**. We use a rigid tool-calling structure. The agent executes within a loop in the `generate_with_tools` method:
1. User provides a prompt.
2. The agent determines required tools based on system instructions.
3. The backend dynamically runs local tools (`document_search`, `operational_data_lookup`, `sla_calculator`, `prepare_escalation`) and maps results back to Gemini.
4. The cycle repeats until the agent outputs a final Markdown-formatted answer to the user.

## 3. Tool Design
Tools are explicitly typed and strictly enforced server-side.
- `document_search`: Performs vector search over `chroma_db` for policies, SOPs, and agreements.
- `operational_data_lookup`: Performs exact-match SQL queries on `sqlite`.
- `sla_calculator`: Deterministically calculates SLA limits from the provided dataset.
- `prepare_escalation`: A mock state-changing action that prepares an escalation proposal.

## 4. Document Retrieval
We use ChromaDB `sentence-transformers` for embedding generation. 
We retrieve a maximum of 10 chunks per query, then filter out deprecated documents (e.g. `status == 'DEPRECATED'`) and mismatched agreements, ensuring only relevant contexts are appended. Final results are truncated to the top 5 by authority level.

## 5. Structured-Data Handling
To prevent LLM hallucinations, structured data is not dumped raw. `operational_data_lookup` retrieves single relevant records (Orders/Tickets/Accounts) by ID from SQLite, scrubbing internal SQLAlchemy state before injection into the LLM context.

## 6. Access Control
Access control is implemented via a mock authentication context headers (`x-user-role`, `x-allowed-accounts`). The tools validate the context against the requested `account_id` before yielding database or document results.

## 7. Source Reliability & Conflict Resolution
The `document_search` tool attaches explicit metadata (`authority_level`, `status`, `source_type`) to chunks. The Gemini system prompt explicitly dictates conflict resolution hierarchy: `1 (Agreements) > 2 (Current Policies/SOP) > 3 (Product Docs) > 4 (History)`.

## 8. Confirmation Workflow
Safety is paramount. `prepare_escalation` does NOT mutate state. It returns `"status": "ACTION_REQUIRES_CONFIRMATION"`. The frontend detects this state and renders a discrete two-button confirmation card. Only clicking `Confirm` hits the secondary POST endpoint `/api/action/confirm` to mutate state.

## 9. Error Handling
The Gemini client is wrapped in a jittered exponential backoff mechanism (`1s`, `2s`, `4s`) that strictly intercepts transient `429` (rate limit) and `503` (overloaded) errors, whilst catching hard Quota limits (`RESOURCE_EXHAUSTED`) with an immediate user-facing termination payload.
