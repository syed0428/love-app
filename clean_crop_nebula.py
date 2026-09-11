import os
from PIL import Image

uploaded_dir = r'C:\Users\alaud\.gemini\antigravity-ide\brain\67963840-92c3-4f01-be83-1057aa0e3db4\.user_uploaded'
f = os.path.join(uploaded_dir, 'media_1789038164448.png')
if not os.path.exists(f):
    f = os.path.join(uploaded_dir, 'media_1789037293510.png')

img = Image.open(f).convert('RGB')
w, h = img.size

# The watermark PAPERHEARTDESIGN.COM is at the top left from y=0 to ~y=65.
# Let's crop from y=68 to y=560, and from x=20 to w-20:
clean_nebula = img.crop((20, 68, w - 20, 560))
clean_nebula.save('nebula_backdrop.jpg', quality=95)
print("Saved clean watermark-free nebula_backdrop.jpg with size:", clean_nebula.size)
