with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Let's inspect .nebula-glow and .grain in CSS
print("=== NEBULA GLOW & GRAIN ===")
m = re.search(r'/\* Fixed Nebula Backdrops \*/.*?(?=/\* Floating Parallax Hearts)', text, re.DOTALL)
if m:
    print(m.group(0)[:800])

print("=== CANVAS DRAW FUNCTION ===")
m2 = re.search(r'function draw\(\) \{.*?(?=window\.addEventListener\("resize")', text, re.DOTALL)
if m2:
    print(m2.group(0)[:800])
