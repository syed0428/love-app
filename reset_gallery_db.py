import os
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto(file_url)
    page.evaluate("""() => {
        indexedDB.deleteDatabase("HayathiLoveGalleryDB");
        for (let i = 1; i <= 6; i++) {
            localStorage.removeItem("hayathi_gallery_" + i);
        }
    }""")
    b.close()
    print("Database reset successfully for clean user experience!")
