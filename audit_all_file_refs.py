import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check all src attributes
src_matches = re.findall(r'src=["\']([^"\']+)["\']', content)
print("=== All src references ===")
for s in set(src_matches):
    if s.startswith('data:'):
        print(f"data URI (length {len(s)})")
    else:
        exists = os.path.exists(s)
        print(f"src: '{s}' -> exists on disk: {exists}")

# 2. Check all href attributes
href_matches = re.findall(r'href=["\']([^"\']+)["\']', content)
print("\n=== All href references ===")
for h in set(href_matches):
    if h.startswith('#') or h.startswith('data:'):
        continue
    exists = os.path.exists(h)
    print(f"href: '{h}' -> exists on disk: {exists}")

# 3. Check all url(...) in CSS
url_matches = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content)
print("\n=== All CSS url(...) references ===")
for u in set(url_matches):
    if u.startswith('data:'):
        print(f"CSS data URI (length {len(u)})")
    else:
        exists = os.path.exists(u)
        print(f"CSS url: '{u}' -> exists on disk: {exists}")
