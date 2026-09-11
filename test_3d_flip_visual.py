import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Let's inspect the current computed styles and capture mid-flip frames
def capture_flip_frames():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        html_path = os.path.abspath("index.html")
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_timeout(1000)
        
        # Unlock site
        page.click("#giftCardWrapper")
        page.wait_for_timeout(600)
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)
        page.click("#btnYes")
        page.wait_for_timeout(2200)
        
        print("Unlocked site!")
        
        # Check computed styles of #mainExperience and #heroSection
        styles = page.evaluate("""() => {
            const main = document.getElementById("mainExperience");
            const hero = document.getElementById("heroSection");
            const csMain = window.getComputedStyle(main);
            const csHero = window.getComputedStyle(hero);
            return {
                mainPerspective: csMain.perspective,
                mainTransformStyle: csMain.transformStyle,
                mainOverflow: csMain.overflow,
                heroOverflowY: csHero.overflowY,
                heroTransformStyle: csHero.transformStyle,
                heroTransformOrigin: csHero.transformOrigin
            };
        }""")
        print("Computed styles before fix:", styles)
        
        browser.close()

if __name__ == "__main__":
    capture_flip_frames()
