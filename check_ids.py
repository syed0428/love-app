import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

ids = re.findall(r'id=["\']([^"\']+)["\']', text)
print("All IDs found in index.html:")
for i in ids:
    print(i)
