import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

viewports = [
    {"name": "Mobile Small (iPhone SE)", "width": 375, "height": 667},
    {"name": "Mobile Medium (iPhone 12/13/14)", "width": 390, "height": 844},
    {"name": "Mobile Large (iPhone Pro Max)", "width": 414, "height": 896},
    {"name": "Tablet (iPad Portrait)", "width": 768, "height": 1024},
    {"name": "Laptop (MacBook/PC)", "width": 1024, "height": 768},
    {"name": "Desktop 1080p", "width": 1440, "height": 900},
]

file_path = "file:///" + os.path.abspath("index.html").replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for vp in viewports:
        page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
        page.goto(file_path)
        page.wait_for_timeout(500)
        
        # Check initial horizontal overflow on gate
        scroll_w = page.evaluate("document.documentElement.scrollWidth")
        inner_w = page.evaluate("window.innerWidth")
        gate_overflow = scroll_w > inner_w
        
        # Click gift
        page.click("#giftCardWrapper")
        page.wait_for_timeout(2600)
        
        # Check date input fit
        date_box = page.locator("#dateInput").bounding_box()
        dialog_box = page.locator("#dateGateDialog").bounding_box()
        
        # Fill date & submit
        page.type("#dateInput", "13072025", delay=30)
        page.wait_for_timeout(600)
        page.click("#btnYes")
        page.wait_for_timeout(1800)
        
        # Check main site horizontal overflow across entire scroll
        max_scroll_w = page.evaluate("""() => {
            let maxW = document.documentElement.scrollWidth;
            for (let y = 0; y <= document.body.scrollHeight; y += 300) {
                window.scrollTo(0, y);
                maxW = Math.max(maxW, document.documentElement.scrollWidth);
            }
            return maxW;
        }""")
        has_overflow = max_scroll_w > inner_w
        
        # Check Quran verse section initial state
        verse_card_text = page.locator(".verse-card").inner_text()
        verse_has_arabic_initially = "وَمِنْ آيَاتِهِ" in verse_card_text
        
        print(f"[{vp['name']}]")
        print(f"  Viewport width: {inner_w}px | Max scrollWidth: {max_scroll_w}px | Overflow: {has_overflow}")
        print(f"  Gate dialog width: {dialog_box['width'] if dialog_box else 'N/A'}px (fits in {inner_w}px)")
        print(f"  Quran verse visible on load: {verse_has_arabic_initially}")
        
        page.close()
    browser.close()
