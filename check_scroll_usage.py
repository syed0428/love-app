import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scroll_matches = [m.start() for m in re.finditer(r'scroll', content, re.IGNORECASE)]
print(f"Total 'scroll' matches: {len(scroll_matches)}")
for m in scroll_matches:
    print(repr(content[m-30:m+70]))
