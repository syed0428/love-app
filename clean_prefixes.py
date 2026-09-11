with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "-webkit-backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);",
    "-webkit-backdrop-filter: blur(6px);"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned duplicate webkit prefix.")
