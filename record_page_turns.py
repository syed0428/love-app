import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def record_turns():
    video_dir = os.path.abspath("videos")
    os.makedirs(video_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        html_path = os.path.abspath("index.html")
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_timeout(1000)
        
        # 1. Unlock Site
        page.click("#giftCardWrapper")
        page.wait_for_timeout(600)
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)
        page.click("#btnYes")
        page.wait_for_timeout(2200)
        
        print("Site unlocked!")
        
        # Verify initial state on Chapter 1
        page.wait_for_timeout(500)
        page.screenshot(path="screenshot_turn_0_ch1_idle.png")
        
        # 2. Click Next: Turn from Chapter 1 to Chapter 2
        print("Clicking Next (Turn 1: Ch 1 -> Ch 2)...")
        btn_next = page.locator("#btnBookNext")
        btn_next.click()
        
        # Capture frames during the 3D flip (duration 850ms)
        page.wait_for_timeout(180) # ~20% of flip
        page.screenshot(path="screenshot_turn1_mid_20pct.png")
        tf1 = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Mid-turn 1 (20%) transform:", tf1)
        
        page.wait_for_timeout(250) # ~50% of flip
        page.screenshot(path="screenshot_turn1_mid_50pct.png")
        tf2 = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Mid-turn 1 (50%) transform:", tf2)
        
        page.wait_for_timeout(250) # ~80% of flip
        page.screenshot(path="screenshot_turn1_mid_80pct.png")
        tf3 = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Mid-turn 1 (80%) transform:", tf3)
        
        page.wait_for_timeout(350) # Flip settled
        page.screenshot(path="screenshot_turn1_ch2_settled.png")
        print("Chapter 2 settled!")
        
        # Pause at normal viewing speed (1.5 seconds)
        page.wait_for_timeout(1500)
        
        # 3. Click Next: Turn from Chapter 2 to Chapter 3
        print("Clicking Next (Turn 2: Ch 2 -> Ch 3)...")
        btn_next.click()
        
        # Capture frames during second 3D flip
        page.wait_for_timeout(180)
        page.screenshot(path="screenshot_turn2_mid_20pct.png")
        
        page.wait_for_timeout(250)
        page.screenshot(path="screenshot_turn2_mid_50pct.png")
        
        page.wait_for_timeout(250)
        page.screenshot(path="screenshot_turn2_mid_80pct.png")
        
        page.wait_for_timeout(350)
        page.screenshot(path="screenshot_turn2_ch3_settled.png")
        print("Chapter 3 settled!")
        
        # Pause at normal viewing speed
        page.wait_for_timeout(1800)
        
        # Close context to finalize video recording
        context.close()
        browser.close()
        
        video_files = os.listdir(video_dir)
        print("Recorded videos:", video_files)
        if video_files:
            latest_vid = os.path.join(video_dir, video_files[-1])
            print("Video saved at:", latest_vid)

if __name__ == "__main__":
    record_turns()
