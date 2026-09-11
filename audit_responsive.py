import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== MEDIA QUERIES ===")
for mq in re.finditer(r'(@media[^{]+)\{', text):
    print(mq.group(1).strip())

print("\n=== VIEWPORT META ===")
m = re.search(r'<meta name="viewport"[^>]+>', text)
if m:
    print(m.group(0))

print("\n=== CHECKING SIZES & FIXED/ABSOLUTE POSITIONS ===")
for cls in ['.gate', '.hero', '.container', '.timeline', '.gallery-grid', '.envelopes-grid', '.wax-letter-paper', '.quiz-card', '.verse-card', '.secret-panel']:
    pat = rf'({re.escape(cls)}\s*\{{[^}}]+\}})'
    m = re.search(pat, text)
    if m:
        print(f"--- {cls} ---")
        print(m.group(1))

print("\n=== CHECKING TOUCH TARGETS & BUTTONS ===")
for btn in ['.btn-submit', '.btn-yes', '.btn-no-dodger', '.quiz-btn', '.btn-verse', '.secret-trigger', '.envelope-card', '.wax-seal']:
    pat = rf'({re.escape(btn)}\s*\{{[^}}]+\}})'
    m = re.search(pat, text)
    if m:
        print(f"--- {btn} ---")
        print(m.group(1))
