import base64
import re

with open('nebula_backdrop.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
data_uri = f'data:image/jpeg;base64,{b64}'

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'--nebula-bg-data:\s*url\([^)]+\);', f'--nebula-bg-data: url("{data_uri}");', text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated --nebula-bg-data with clean crop! Length:", len(data_uri))
