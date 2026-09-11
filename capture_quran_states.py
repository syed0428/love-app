import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page.goto(file_url)
    page.wait_for_timeout(500)

    # 1. Unlock gate
    page.click("#giftCardWrapper")
    page.wait_for_timeout(600)
    page.fill("#dateInput", "13-07-2025")
    page.click("#dateSubmitBtn")
    page.wait_for_timeout(1000)
    page.click("#btnYes")
    page.wait_for_timeout(2000)

    # 2. Scroll to Quran section collapsed
    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterVerses').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(600)
    page.screenshot(path="screenshot_quran_collapsed.png")
    print("Saved screenshot_quran_collapsed.png")

    # 3. Click reveal button
    page.click("#btnNextVerse")
    page.wait_for_timeout(800)
    page.evaluate("() => { document.getElementById('chapterVerses').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(400)
    page.screenshot(path="screenshot_quran_revealed.png")
    print("Saved screenshot_quran_revealed.png")

    browser.close()
