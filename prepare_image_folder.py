import os
import shutil

img_dir = "image"
if not os.path.exists(img_dir):
    os.makedirs(img_dir, exist_ok=True)

for i in range(1, 7):
    src_double_ext = os.path.join(img_dir, f"photo{i}.jpg.jpeg")
    dst_single_ext = os.path.join(img_dir, f"photo{i}.jpg")
    
    if os.path.exists(src_double_ext) and not os.path.exists(dst_single_ext):
        shutil.copy2(src_double_ext, dst_single_ext)
        print(f"Created alias: {dst_single_ext} from {src_double_ext}")
    elif os.path.exists(dst_single_ext):
        print(f"{dst_single_ext} already exists.")
    else:
        print(f"Warning: {src_double_ext} not found.")

print("\nFiles in image/:", os.listdir(img_dir))
