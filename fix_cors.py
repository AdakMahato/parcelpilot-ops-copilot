import re
with open("backend/app/main.py", "r") as f:
    content = f.read()

# Replace CORS hardcoded origins
old_cors = """    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.2.2:3000"
    ],"""
new_cors = """    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),"""
content = content.replace(old_cors, new_cors)

with open("backend/app/main.py", "w") as f:
    f.write(content)
