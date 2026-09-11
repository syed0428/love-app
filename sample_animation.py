import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def sample():
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
        
        # Click Next
        page.click("#btnBookNext")
        
        # Sample every 50ms for 1000ms
        start = time.time()
        while time.time() - start < 1.1:
            t_elapsed = int((time.time() - start) * 1000)
            res = page.evaluate("""() => {
                const el = document.getElementById("heroSection");
                const cs = window.getComputedStyle(el);
                return {
                    display: cs.display,
                    transform: cs.transform,
                    opacity: cs.opacity,
                    animName: cs.animationName
                };
            }""")
            if 'matrix' in res['transform']:
                # print summary
                print(f"{t_elapsed}ms: {res['display']} | anim={res['animName']} | tf={res['transform'][:35]}...")
            else:
                print(f"{t_elapsed}ms: {res['display']} | anim={res['animName']} | tf={res['transform']}")
            page.wait_for_timeout(50)
            
        browser.close()

if __name__ == "__main__":
    sample()
