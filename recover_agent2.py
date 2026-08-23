import json

log_path = "/Users/aadarshamahato/.gemini/antigravity/brain/4ae7b9a9-366c-4169-9e12-facf1497acd1/.system_generated/logs/transcript_full.jsonl"
with open(log_path, 'r') as f:
    for line in f:
        if 'class OpsAgent:' in line and 'def run' in line:
            data = json.loads(line)
            content = data.get('content', '')
            if 'import os' in content and 'The user wants the response strictly in this exact Markdown structure' not in content:
                print("Found older agent.py!")
                start = content.find('import os')
                if start != -1:
                    code = content[start:]
                    with open("recovered_agent.py", "w") as out:
                        out.write(code)
                    break # Stop at first match which is oldest
