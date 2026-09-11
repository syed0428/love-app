with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find all occurrences of dateInput
for m in re.finditer(r'dateInput', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print("--- MATCH ---")
    print(text[start:end])
