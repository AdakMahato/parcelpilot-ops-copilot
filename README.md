# ParcelPilot Ops Copilot

An AI-powered internal operations dashboard for ParcelPilot support agents. It connects a powerful large language model (Gemini 3.7 Flash) to live relational data (SQLite) and vectorized organizational knowledge (ChromaDB) to automate complex support investigations.

## Features
- **Issue Intelligence**: A dynamic dashboard calculating real-time SLA breaches and surfacing recurring platform issues.
- **Agentic Chat**: A multi-step conversational agent capable of querying structured data, finding documents, and drafting escalations.
- **Two-Step Confirmations**: Safe execution of state-changing operations via strict UI/Backend confirmation loops.
- **Authoritative Source Resolution**: Deterministic source ranking that inherently respects custom enterprise agreements over deprecated general policies.

## Setup & Local Execution

### Prerequisites
- Node.js 18+
- Python 3.12+

### 1. Environment Configuration
Create a `.env` file in the `backend/` directory:
```bash
GEMINI_API_KEY="your-gemini-api-key"
GEMINI_MODEL="gemini-3.7-flash"
```

### 2. Run the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
*Note: The initial run leverages the provided `parcelpilot.db` and `chroma_db/`. If they are missing, refer to the data loading scripts.*

### 3. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:3000`.

## Testing
We utilize `pytest` to validate tool contracts, authorization scopes, and source resolution.

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest tests/test_tools.py
```

## Known Limitations
- The system currently mocks user authentication via HTTP headers (`x-user-role`).
- Due to the nature of LLM generation, upstream API availability issues (e.g. Gemini 503 Overloaded) may occasionally interrupt chat availability. We employ jittered exponential backoff to mitigate transient failures.
