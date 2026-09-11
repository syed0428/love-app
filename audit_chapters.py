import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<(header|section)[^>]*id="([^"]+)"[^>]*>', re.IGNORECASE)
for m in pattern.finditer(content):
    start = m.start()
    tag = m.group(1)
    sid = m.group(2)
    # find line number
    line_no = content[:start].count('\n') + 1
    # find heading inside first 500 chars
    chunk = content[start:start+1000]
    headings = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', chunk, re.DOTALL)
    heading_text = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]
    print(f"Line {line_no:4d} | <{tag} id=\"{sid}\"> | Heading: {heading_text}")
