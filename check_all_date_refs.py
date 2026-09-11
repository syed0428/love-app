with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['13/07', '13072025', 'ANNIVERSARY', 'dateFeedback', 'changed our lives', 'July', '2025', 'failedDateAttempts']):
        print(f"{i+1}: {l.strip()}")
