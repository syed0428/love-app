with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_str = 'class="btn-change-photo clickable"'
new_str = 'class="btn-change-photo clickable" style="display:none"'

count = c.count(old_str)
c = c.replace(old_str, new_str)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"Updated {count} btn-change-photo elements!")
