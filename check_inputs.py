import json

with open('snapshot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

found = 0
for i, m in enumerate(data.get('chat_messages', [])):
    for b in m.get('content', []):
        if b.get('type') == 'tool_use':
            inp = b.get('input')
            if inp:
                found += 1
                keys = list(inp.keys()) if isinstance(inp, dict) else type(inp)
                print(f"Msg {i} tool {b.get('name')} has input: {keys}")

print(f"Total tools with input: {found}")
