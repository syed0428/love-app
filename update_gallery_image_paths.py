import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the 6 gallery img src attributes from photoX.jpg to image/photoX.jpg
for i in range(1, 7):
    old_str = f'id="galleryImg{i}" src="photo{i}.jpg"'
    new_str = f'id="galleryImg{i}" src="image/photo{i}.jpg"'
    if old_str in content:
        content = content.replace(old_str, new_str, 1)
        print(f"Replaced galleryImg{i} src with image/photo{i}.jpg")
    else:
        print(f"Warning: {old_str} not found")

# 2. Update initGalleryPhotos in JS
old_js_block = """          // Check if local file exists on disk
          const testImg = new Image();
          testImg.onload = () => {
            displayPhotoInFrame(i, `photo${i}.jpg`);
          };
          testImg.onerror = () => {
            // Keep empty placeholder visible
          };
          testImg.src = `photo${i}.jpg`;"""

new_js_block = """          // Check if local file exists on disk in image/ folder
          const testImg = new Image();
          testImg.onload = () => {
            displayPhotoInFrame(i, `image/photo${i}.jpg`);
          };
          testImg.onerror = () => {
            // Check fallback for double extension (.jpg.jpeg)
            const testImg2 = new Image();
            testImg2.onload = () => {
              displayPhotoInFrame(i, `image/photo${i}.jpg.jpeg`);
            };
            testImg2.onerror = () => {
              // Keep empty placeholder visible; caption remains intact
            };
            testImg2.src = `image/photo${i}.jpg.jpeg`;
          };
          testImg.src = `image/photo${i}.jpg`;"""

if old_js_block in content:
    content = content.replace(old_js_block, new_js_block, 1)
    print("Updated initGalleryPhotos() successfully!")
else:
    print("Warning: old_js_block not found exactly, searching by regex...")
    pattern = r"// Check if local file exists on disk\s+const testImg = new Image\(\);[\s\S]*?testImg\.src = `photo\$\{i\}\.jpg`;"
    if re.search(pattern, content):
        content = re.sub(pattern, new_js_block.strip(), content)
        print("Replaced initGalleryPhotos via regex!")
    else:
        print("Error: Could not locate initGalleryPhotos block.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("index.html updated successfully.")
