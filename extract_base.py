import json

with open('snapshot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for idx in [7, 59]:
    msg = data['chat_messages'][idx]
    for b in msg.get('content', []):
        if b.get('name') == 'create_file':
            inp = b.get('input', {})
            text = inp.get('file_text', '')
            path = inp.get('path', '')
            print(f"Msg {idx}: path={path}, len={len(text)}")
            fname = f"msg_{idx}_{path.split('/')[-1]}"
            with open(fname, 'w', encoding='utf-8') as out:
                out.write(text)
            print(f"Saved {fname}")
