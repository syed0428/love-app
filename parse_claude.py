import urllib.request
import json
import os

url = 'https://claude.ai/api/chat_snapshots/c30009f0-da0c-48a3-9c0a-88c694b32e2c?rendering_mode=messages&render_all_tools=true'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(resp)

output_lines = []
output_lines.append(f"Snapshot Title: {data.get('snapshot_name')}")
output_lines.append(f"Author: {data.get('created_by')}")
output_lines.append(f"Created At: {data.get('created_at')}")
output_lines.append("=" * 60)

messages = data.get('chat_messages', [])
output_lines.append(f"Total messages: {len(messages)}\n")

for i, msg in enumerate(messages):
    sender = msg.get('sender', '').upper()
    output_lines.append(f"\n--- [MESSAGE {i+1}] {sender} ---")
    for block in msg.get('content', []):
        btype = block.get('type')
        if btype == 'text':
            output_lines.append(block.get('text', ''))
        elif btype == 'tool_use':
            name = block.get('name')
            inp = block.get('input')
            output_lines.append(f"[TOOL USE: {name}]")
            if name == 'create_file' and isinstance(inp, dict):
                path = inp.get('path', '')
                content = inp.get('content', '')
                output_lines.append(f"[Created file: {path}, size: {len(content)} chars]")
                with open('extracted_hayathi_site.html', 'w', encoding='utf-8') as f_site:
                    f_site.write(content)
        elif btype == 'tool_result':
            output_lines.append(f"[TOOL RESULT: {block.get('name')}]")

with open('claude_conversation_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("Done. Wrote to claude_conversation_summary.txt")
