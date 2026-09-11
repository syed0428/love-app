import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def capture_demonstration():
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
        page.wait_for_timeout(800)
        
        # Unlock site
        page.click("#giftCardWrapper")
        page.wait_for_timeout(500)
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)
        page.click("#btnYes")
        page.wait_for_timeout(2200)
        
        print("Site unlocked!")
        
        # Screenshot 1: Chapter 1 resting flat
        page.wait_for_timeout(400)
        page.screenshot(path="screenshot_demo_ch1_idle.png")
        
        # ==========================================
        # TURN 1: Chapter 1 -> Chapter 2
        # ==========================================
        print("Starting Turn 1 (Ch 1 -> Ch 2)...")
        btn_next = page.locator("#btnBookNext")
        btn_next.click()
        
        # Frame A: 180ms (~22 deg rotation)
        page.wait_for_timeout(180)
        page.screenshot(path="screenshot_demo_turn1_frameA.png")
        tfA = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Turn 1 - Frame A transform:", tfA)
        
        # Frame B: +170ms = 350ms (~55 deg rotation, peak 3D foreshortening & fold shadow!)
        page.wait_for_timeout(170)
        page.screenshot(path="screenshot_demo_turn1_frameB_peak3D.png")
        tfB = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Turn 1 - Frame B (PEAK 3D) transform:", tfB)
        
        # Frame C: +220ms = 570ms (~85 deg rotation)
        page.wait_for_timeout(220)
        page.screenshot(path="screenshot_demo_turn1_frameC.png")
        tfC = page.evaluate("() => window.getComputedStyle(document.getElementById('heroSection')).transform")
        print("Turn 1 - Frame C transform:", tfC)
        
        # Settle: +350ms (Turn 1 complete)
        page.wait_for_timeout(350)
        page.screenshot(path="screenshot_demo_ch2_settled.png")
        print("Turn 1 complete! Settled on Chapter 2.")
        
        # Pause at normal viewing speed (2 seconds)
        page.wait_for_timeout(2000)
        
        # ==========================================
        # TURN 2: Chapter 2 -> Chapter 3
        # ==========================================
        print("Starting Turn 2 (Ch 2 -> Ch 3)...")
        btn_next.click()
        
        # Frame A: 180ms
        page.wait_for_timeout(180)
        page.screenshot(path="screenshot_demo_turn2_frameA.png")
        tf2A = page.evaluate("() => window.getComputedStyle(document.getElementById('chapterTimeline')).transform")
        print("Turn 2 - Frame A transform:", tf2A)
        
        # Frame B: +170ms = 350ms (Peak 3D foreshortening & fold shadow!)
        page.wait_for_timeout(170)
        page.screenshot(path="screenshot_demo_turn2_frameB_peak3D.png")
        tf2B = page.evaluate("() => window.getComputedStyle(document.getElementById('chapterTimeline')).transform")
        print("Turn 2 - Frame B (PEAK 3D) transform:", tf2B)
        
        # Frame C: +220ms = 570ms
        page.wait_for_timeout(220)
        page.screenshot(path="screenshot_demo_turn2_frameC.png")
        
        # Settle: +350ms (Turn 2 complete)
        page.wait_for_timeout(350)
        page.screenshot(path="screenshot_demo_ch3_settled.png")
        print("Turn 2 complete! Settled on Chapter 3.")
        
        # Pause at normal viewing speed (2 seconds)
        page.wait_for_timeout(2000)
        
        # Close context to write out video
        context.close()
        browser.close()
        
        video_path = page.video.path() if page.video else None
        print("Video recording saved to:", video_path)

if __name__ == "__main__":
    capture_demonstration()
