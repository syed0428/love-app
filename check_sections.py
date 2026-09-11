import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find main and all sections
print("main tag:", re.findall(r'<main[^>]*>', content))
print("sections:", re.findall(r'<(?:header|section)[^>]*id="([^"]+)"', content))
