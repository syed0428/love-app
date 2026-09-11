from PIL import Image, ImageEnhance
import base64

# Enhance contrast and saturation directly in the image file
img = Image.open('nebula_backdrop.jpg').convert('RGB')
enhancer_con = ImageEnhance.Contrast(img)
img = enhancer_con.enhance(1.18)
enhancer_col = ImageEnhance.Color(img)
img = enhancer_col.enhance(1.25)

img.save('nebula_backdrop.jpg', quality=92, optimize=True)
print("Saved optimized nebula_backdrop.jpg with baked-in vibrancy!")

# Generate base64
with open('nebula_backdrop.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
data_uri = f"data:image/jpeg;base64,{b64}"

print("New Base64 length:", len(data_uri))
with open('nebula_b64.txt', 'w') as f:
    f.write(data_uri)
