import re
with open("backend/app/agent.py", "r") as f:
    content = f.read()

content = content.replace(
    'log_activity("Agent query", f"User query: {user_message}", actor="System")',
    'log_activity("Agent query", f"User query: {user_message}", actor=auth_context.get("role", "System"))'
)

with open("backend/app/agent.py", "w") as f:
    f.write(content)
