import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_3d_rotation():
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
        
        # Now let's inject our improved 3D rules and test
        page.evaluate("""() => {
            const style = document.createElement('style');
            style.id = 'test3DStyle';
            style.innerHTML = `
                #mainExperience {
                    perspective: 1200px !important;
                    -webkit-perspective: 1200px !important;
                    transform-style: preserve-3d !important;
                }
                .book-page {
                    overflow: visible !important;
                    transform-style: preserve-3d !important;
                    background: radial-gradient(circle at 50% 30%, rgba(35, 12, 48, 0.98), rgba(7, 2, 14, 0.99) 75%), #05020a !important;
                    box-shadow: 0 0 50px rgba(0,0,0,0.8);
                }
                .book-page.page-active {
                    opacity: 1 !important;
                }
                .book-page.turning-next-out {
                    animation: testFlipOut 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
                    opacity: 1 !important;
                }
                @keyframes testFlipOut {
                    0% {
                        transform: rotateY(0deg);
                        box-shadow: 0 0 0 rgba(0,0,0,0);
                    }
                    35% {
                        transform: rotateY(-38deg) skewY(-2deg);
                        box-shadow: -25px 0 50px rgba(0,0,0,0.7);
                    }
                    70% {
                        transform: rotateY(-85deg) skewY(-3.5deg);
                        box-shadow: -45px 0 80px rgba(0,0,0,0.9);
                    }
                    100% {
                        transform: rotateY(-135deg) skewY(0deg);
                        box-shadow: -15px 0 30px rgba(0,0,0,0.4);
                    }
                }
                .book-page.turning-next-in {
                    animation: none !important;
                    transform: rotateY(0deg) translateZ(-5px) !important;
                    opacity: 1 !important;
                    display: block !important;
                    z-index: 5 !important;
                }
            `;
            document.head.appendChild(style);
        }""")
        
        print("Injected test 3D styles!")
        
        # Trigger next chapter
        page.click("#btnBookNext")
        
        # Capture frames at 150ms, 300ms, 450ms, 600ms, 800ms
        frame_delays = [150, 150, 150, 150, 250]
        for idx, d in enumerate(frame_delays):
            page.wait_for_timeout(d)
            # Evaluate transform of hero
            tf = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
            print(f"Frame {idx+1} transform:", tf)
            page.screenshot(path=f"screenshot_test_flip_frame_{idx+1}.png")
            
        browser.close()

if __name__ == "__main__":
    test_3d_rotation()
