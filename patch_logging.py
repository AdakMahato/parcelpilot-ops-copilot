import re

with open("backend/app/llm/gemini_provider.py", "r") as f:
    content = f.read()

replacement = """
                # Log to a local file so the sandbox can read it
                with open("/tmp/gemini_error.txt", "w") as f_err:
                    f_err.write(f"HTTP Status: {status_code}\\nError: {e}\\n")
                    
                # If daily quota is exhausted
"""
content = content.replace("# If daily quota is exhausted", replacement)

with open("backend/app/llm/gemini_provider.py", "w") as f:
    f.write(content)
