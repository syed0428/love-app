import json

with open('snapshot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

output = []
output.append(f"Snapshot Title: {data.get('snapshot_name')}")
output.append(f"Author: {data.get('created_by')} ({data.get('creator', {}).get('full_name')})")
output.append(f"Created At: {data.get('created_at')}")
output.append(f"Updated At: {data.get('updated_at')}")
output.append("=" * 60)

messages = data.get('chat_messages', [])
output.append(f"Total Messages: {len(messages)}\n")

for i, msg in enumerate(messages):
    sender = msg.get('sender', '').upper()
    created = msg.get('created_at', '')
    output.append(f"\n==================== MESSAGE {i+1} | {sender} | {created} ====================")
    
    # Check text field first
    if msg.get('text'):
        output.append(msg.get('text'))
        
    for block in msg.get('content', []):
        btype = block.get('type')
        if btype == 'text':
            t = block.get('text', '').strip()
            if t:
                output.append(t)
        elif btype == 'tool_use':
            tname = block.get('name')
            inp = block.get('input') or {}
            output.append(f"\n[TOOL CALL: {tname}]")
            if tname == 'create_file':
                path = inp.get('path', '')
                content = inp.get('content', '')
                output.append(f"  Path: {path} (length: {len(content)} chars)")
                # save artifact file if it exists
                with open(f"extracted_site_msg_{i+1}.html", "w", encoding="utf-8") as f_out:
                    f_out.write(content)
            elif tname == 'bash_tool':
                output.append(f"  Command: {inp.get('command', '')}")
            elif tname == 'present_files':
                output.append(f"  Files: {inp.get('filepaths', [])}")
            else:
                output.append(f"  Input keys: {list(inp.keys()) if isinstance(inp, dict) else type(inp)}")
        elif btype == 'tool_result':
            output.append(f"[TOOL RESULT: {block.get('name')}]")

with open('full_conversation_transcript.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"Parsed {len(messages)} messages successfully.")
