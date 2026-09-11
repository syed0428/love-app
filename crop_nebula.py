import os
from PIL import Image

uploaded_dir = r'C:\Users\alaud\.gemini\antigravity-ide\brain\67963840-92c3-4f01-be83-1057aa0e3db4\.user_uploaded'
f = os.path.join(uploaded_dir, 'media_1789038164448.png')
if not os.path.exists(f):
    f = os.path.join(uploaded_dir, 'media_1789037293510.png')

img = Image.open(f).convert('RGB')
w, h = img.size
print(f"Original size: {w}x{h}")

# The image is 1024x1024
# The nebula part is roughly top y=25 to y=560 (below the white top border and above the swatches)
# Let's crop the nebula part precisely:
nebula = img.crop((20, 25, w - 20, 560))
nebula.save('nebula_backdrop.jpg', quality=95)
print("Saved nebula_backdrop.jpg:", nebula.size)

# Also let's extract the exact 5 swatch hex colors directly from the pixels!
# Swatches are in the bottom region (y ~ 650 to 900)
swatch_xs = [int(w * 0.1), int(w * 0.3), int(w * 0.5), int(w * 0.7), int(w * 0.9)]
swatch_y = 750
colors = []
for x in swatch_xs:
    r, g, b = img.getpixel((x, swatch_y))[:3]
    hex_col = f"#{r:02x}{g:02x}{b:02x}"
    colors.append(hex_col)

print("Exact Extracted Palette:", colors)
