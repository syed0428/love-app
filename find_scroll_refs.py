with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'scrollProgressBar' in l or 'initTypingEffect' in l or 'reveal-on-scroll' in l or 'IntersectionObserver' in l or 'window.addEventListener("scroll"' in l or "window.addEventListener('scroll'" in l:
        print(f"{i+1}: {l.strip()[:120]}")
