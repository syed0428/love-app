import shutil
import os

artifact_dir = r"C:\Users\alaud\.gemini\antigravity-ide\brain\67963840-92c3-4f01-be83-1057aa0e3db4"

files_to_copy = [
    "screenshot_book_ch1_desktop.png",
    "screenshot_book_ch2_timeline.png",
    "screenshot_book_ch3_gallery.png",
    "screenshot_book_ch8_closing.png",
    "screenshot_book_mobile_ch1.png",
    "screenshot_book_mobile_ch2.png"
]

for f in files_to_copy:
    if os.path.exists(f):
        dst = os.path.join(artifact_dir, f)
        shutil.copy2(f, dst)
        print(f"Copied {f} -> {dst}")
    else:
        print(f"Warning: {f} does not exist.")
