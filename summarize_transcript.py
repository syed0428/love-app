import sys

with open('full_conversation_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

msgs = text.split('==================== MESSAGE ')
out = []
for i in range(1, len(msgs)):
    lines = msgs[i].strip().split('\n')
    header = lines[0]
    parts = header.split('|')
    sender = parts[1].strip() if len(parts) > 1 else 'UNKNOWN'
    
    body_lines = []
    for l in lines[1:]:
        if not l.startswith('[TOOL CALL') and not l.startswith('[TOOL RESULT') and not l.startswith('  Path:') and not l.startswith('  Command:') and not l.startswith('  Files:'):
            body_lines.append(l)
    body = '\n'.join(body_lines).strip()
    if body:
        out.append(f"### Message {i} - {sender}\n{body}\n")

with open('clean_conversation.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"Wrote {len(out)} messages to clean_conversation.md")
