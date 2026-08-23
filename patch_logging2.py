import re
with open("backend/app/llm/gemini_provider.py", "r") as f:
    content = f.read()

content = content.replace("/tmp/gemini_error.txt", "gemini_error.txt")

with open("backend/app/llm/gemini_provider.py", "w") as f:
    f.write(content)
