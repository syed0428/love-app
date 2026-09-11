with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['id="mainExperience"', 'id="scrollProgressBar"', '</main>', 'scroll-progress', 'initTypingEffect', 'typingLine']):
        print(f"{i+1}: {l.strip()[:110]}")
