import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def debug_hero():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        html_path = os.path.abspath("index.html")
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_timeout(500)
        
        # Unlock site
        page.click("#giftCardWrapper")
        page.wait_for_timeout(500)
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)
        page.click("#btnYes")
        page.wait_for_timeout(2000)
        
        # Check initial state
        initial = page.evaluate("""() => {
            const h = document.getElementById("heroSection");
            const cs = window.getComputedStyle(h);
            return {
                className: h.className,
                display: cs.display,
                visibility: cs.visibility,
                animationName: cs.animationName,
                transform: cs.transform
            };
        }""")
        print("Initial hero:", initial)
        
        # Trigger next
        page.click("#btnBookNext")
        page.wait_for_timeout(100)
        
        mid = page.evaluate("""() => {
            const h = document.getElementById("heroSection");
            const cs = window.getComputedStyle(h);
            return {
                className: h.className,
                display: cs.display,
                visibility: cs.visibility,
                animationName: cs.animationName,
                transform: cs.transform,
                animationPlayState: cs.animationPlayState,
                animationDuration: cs.animationDuration
            };
        }""")
        print("Mid hero (100ms):", mid)
        
        # Wait 300ms
        page.wait_for_timeout(300)
        mid2 = page.evaluate("""() => {
            const h = document.getElementById("heroSection");
            const cs = window.getComputedStyle(h);
            return {
                className: h.className,
                display: cs.display,
                visibility: cs.visibility,
                animationName: cs.animationName,
                transform: cs.transform
            };
        }""")
        print("Mid hero (400ms):", mid2)
        
        browser.close()

if __name__ == "__main__":
    debug_hero()
