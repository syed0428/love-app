with open('index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'id="dateInput"' in line:
            print(f"Line {i}: {line}")
