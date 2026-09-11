with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove style="display:none" from btn-change-photo in HTML
c = c.replace('class="btn-change-photo clickable" style="display:none"', 'class="btn-change-photo clickable"')

# 2. Add !important to display: inline-flex in CSS
c = c.replace('display: inline-flex;\n        opacity: 0.95;', 'display: inline-flex !important;\n        opacity: 0.95;')
c = c.replace('display: inline-flex;\n        opacity: 0.8;', 'display: inline-flex !important;\n        opacity: 0.8;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated btn-change-photo display rules!")
