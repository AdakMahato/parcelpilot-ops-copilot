import json

log_path = "/Users/aadarshamahato/.gemini/antigravity/brain/4ae7b9a9-366c-4169-9e12-facf1497acd1/.system_generated/logs/transcript_full.jsonl"
with open(log_path, 'r') as f:
    lines = f.readlines()

for line in lines:
    try:
        data = json.loads(line)
        if 'tool_calls' in data:
            # We are looking for the tool response from 'cat frontend/src/app/page.tsx'
            pass
        if data.get('source') == 'SYSTEM' and 'tool_calls' not in data:
            # Maybe tool response
            content = data.get('content', '')
            if 'import React, { useState, useEffect } from \'react\';' in content and 'export default function Home()' in content:
                # Extract the code block
                start = content.find('"use client";')
                end = content.rfind('}') + 1
                if start != -1 and end != -1:
                    code = content[start:end]
                    # We might have multiple, let's keep going to find the one right before the rewrite
                    with open("recovered_page.tsx", "w") as out:
                        out.write(code)
    except Exception as e:
        pass
