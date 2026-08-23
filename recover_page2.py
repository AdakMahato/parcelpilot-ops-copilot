import json

log_path = "/Users/aadarshamahato/.gemini/antigravity/brain/4ae7b9a9-366c-4169-9e12-facf1497acd1/.system_generated/logs/transcript_full.jsonl"
with open(log_path, 'r') as f:
    for line in f:
        if 'import ReactMarkdown from \\'react-markdown\\';' in line:
            data = json.loads(line)
            content = data.get('content', '')
            if 'export default function Home()' in content:
                # print snippet to see if it matches
                print("Found match!")
                lines = content.split('\\n')
                out_lines = []
                capture = False
                for c_line in lines:
                    if '"use client";' in c_line:
                        capture = True
                        # clean up any leading output markers if they got split weirdly
                        c_line = '"use client";'
                    if capture:
                        out_lines.append(c_line)
                if out_lines:
                    with open("recovered_page.tsx", "w") as out:
                        out.write('\\n'.join(out_lines))
