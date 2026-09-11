with open('index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'filter' in line and 'blur' in line:
            print(f"Line {i}: {line.strip()}")
