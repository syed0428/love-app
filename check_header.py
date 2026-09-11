with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print(re.findall(r'<header[^>]*id="heroSection"[^>]*>', text))
