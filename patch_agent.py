import re
with open("backend/app/agent.py", "r") as f:
    content = f.read()

import_stmt = "\nfrom app.db_logger import log_activity\n"
if "log_activity" not in content:
    content = content.replace("from app.llm.gemini_provider import GeminiProvider", "from app.llm.gemini_provider import GeminiProvider" + import_stmt)

run_start = "    def run(self, user_message: str, auth_context: dict):"
log_stmt = """    def run(self, user_message: str, auth_context: dict):
        log_activity("Agent query", f"User query: {user_message}", actor="System")
"""
content = content.replace(run_start, log_stmt)

with open("backend/app/agent.py", "w") as f:
    f.write(content)
