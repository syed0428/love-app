import json

with open('snapshot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, m in enumerate(data.get('chat_messages', [])):
    for b in m.get('content', []):
        if b.get('name') in ['str_replace', 'bash_tool']:
            inp = b.get('input')
            if inp:
                print(f"Msg {i} {b.get('name')}: {list(inp.keys()) if isinstance(inp, dict) else inp}")
