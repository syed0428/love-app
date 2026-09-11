import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_tests():
    with sync_playwright() as p:
        print("Launching Chromium browser...")
        browser = p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1280x800)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        html_path = os.path.abspath("index.html")
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_timeout(1000)
        
        print("--- STEP 1: Testing Gate Unlock Flow ---")
        page.click("#giftCardWrapper")
        page.wait_for_timeout(800)
        
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)
        
        page.click("#btnYes")
        page.wait_for_timeout(2200)
        
        main = page.locator("#mainExperience")
        assert "revealed" in main.get_attribute("class"), "Main experience should have class 'revealed'"
        print("✓ Main experience successfully unlocked!")
        
        nav_bar = page.locator("#bookNavBar")
        assert "visible" in nav_bar.get_attribute("class"), "Book nav bar should be visible"
        print("✓ Book bottom navigation bar is visible!")
        
        hero = page.locator("#heroSection")
        assert "page-active" in hero.get_attribute("class"), "Hero section should be page-active"
        print("✓ Chapter 1 (Hero) is page-active!")
        
        btn_prev = page.locator("#btnBookPrev")
        assert "hidden-btn" in btn_prev.get_attribute("class"), "Back button should be hidden on chapter 1"
        print("✓ Back button is hidden on Chapter 1!")
        
        dots = page.locator(".book-dot")
        count = dots.count()
        assert count == 8, f"Expected 8 chapter dots, got {count}"
        assert "active" in dots.nth(0).get_attribute("class"), "First dot should be active"
        print(f"✓ Found {count} chapter dots; Dot 0 is active!")
        
        page.screenshot(path="screenshot_book_ch1_desktop.png")
        
        # Step 4: Click Next -> Turn to Chapter 2 (Our Story)
        print("--- STEP 2: Testing Forward Page-Turn to Chapter 2 ---")
        btn_next = page.locator("#btnBookNext")
        btn_next.click()
        page.wait_for_timeout(950)
        
        timeline = page.locator("#chapterTimeline")
        assert "page-active" in timeline.get_attribute("class"), "Timeline should be page-active"
        assert "hidden-btn" not in btn_prev.get_attribute("class"), "Back button should now be visible"
        assert "active" in dots.nth(1).get_attribute("class"), "Dot 1 should be active"
        label_text = page.locator("#bookNavLabel").text_content()
        print(f"✓ Successfully turned to Chapter 2! Label: '{label_text}'")
        
        page.screenshot(path="screenshot_book_ch2_timeline.png")
        
        # Step 5: Test Sequential Forward Page Turns through all 8 chapters
        print("--- STEP 3: Sequential Page Turns to Chapter 8 ---")
        expected_chapters = [
            ("chapterGallery", "Chapter 3: Photo Memories"),
            ("chapterEnvelopes", "Chapter 4: Love Notes"),
            ("chapterLetter", "Chapter 5: Sealed Letter"),
            ("chapterQuiz", "Chapter 6: Our Quiz"),
            ("chapterVerses", "Chapter 7: Sacred Dua"),
            ("chapterClosing", "Chapter 8: Closing & Secret")
        ]
        
        for ch_id, ch_desc in expected_chapters:
            btn_next.click()
            page.wait_for_timeout(950)
            ch_el = page.locator(f"#{ch_id}")
            assert "page-active" in ch_el.get_attribute("class"), f"{ch_id} should be page-active"
            lbl = page.locator("#bookNavLabel").text_content()
            print(f"✓ Turned to {ch_desc} | Nav Label: '{lbl}'")
            
        page.screenshot(path="screenshot_book_ch8_closing.png")
        
        # Verify Typing text triggered in Chapter 8
        page.wait_for_timeout(2000)
        typing_el = page.locator("#typingText")
        typing_text = typing_el.text_content()
        assert len(typing_text) > 5, f"Typing text should have animated, got: '{typing_text}'"
        print(f"✓ Typing effect in Chapter 8 triggered smoothly! Text: '{typing_text[:40]}...'")
        
        # Step 6: Test Back Button (Backward 3D Flip)
        print("--- STEP 4: Testing Backward Page-Turn from Ch 8 to Ch 7 ---")
        btn_prev.click()
        page.wait_for_timeout(950)
        verses = page.locator("#chapterVerses")
        assert "page-active" in verses.get_attribute("class"), "Chapter 7 (Verses) should be page-active after Back"
        print("✓ Backward page flip returned to Chapter 7!")
        
        # Step 7: Test Direct Dot Jump (e.g. click Dot 2 for Gallery)
        print("--- STEP 5: Testing Direct Dot Jump to Chapter 3 (Gallery) ---")
        dots.nth(2).click()
        page.wait_for_timeout(950)
        gallery = page.locator("#chapterGallery")
        assert "page-active" in gallery.get_attribute("class"), "Chapter 3 (Gallery) should be page-active after dot click"
        print("✓ Direct dot navigation to Chapter 3 worked perfectly!")
        page.screenshot(path="screenshot_book_ch3_gallery.png")
        
        # Step 8: Desktop Keyboard Navigation
        print("--- STEP 6: Testing Desktop Keyboard Navigation (ArrowRight / ArrowLeft) ---")
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(950)
        envelopes = page.locator("#chapterEnvelopes")
        assert "page-active" in envelopes.get_attribute("class"), "ArrowRight should flip to Chapter 4 (Envelopes)"
        print("✓ ArrowRight navigation successfully flipped to Chapter 4!")
        
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(950)
        assert "page-active" in gallery.get_attribute("class"), "ArrowLeft should flip back to Chapter 3 (Gallery)"
        print("✓ ArrowLeft navigation successfully flipped back to Chapter 3!")
        
        context.close()
        
        # ==========================================
        # 2. Mobile Viewport & Swipe Gesture Test
        # ==========================================
        print("\n--- STEP 7: Testing Mobile Viewport (375x812) & Touch Swiping ---")
        mobile_context = browser.new_context(
            viewport={"width": 375, "height": 812},
            has_touch=True,
            is_mobile=True
        )
        mobile_page = mobile_context.new_page()
        mobile_page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        mobile_page.wait_for_timeout(800)
        
        # Quick unlock via UI
        mobile_page.click("#giftCardWrapper")
        mobile_page.wait_for_timeout(600)
        mobile_page.fill("#dateInput", "13-07-2025")
        mobile_page.click("#dateSubmitBtn")
        mobile_page.wait_for_timeout(1800)
        mobile_page.click("#btnYes")
        mobile_page.wait_for_timeout(2200)
        
        # Verify Chapter 1 active on mobile
        assert "page-active" in mobile_page.locator("#heroSection").get_attribute("class")
        print("✓ Mobile unlocked on Chapter 1!")
        mobile_page.screenshot(path="screenshot_book_mobile_ch1.png")
        
        # Verify no horizontal window overflow
        overflow = mobile_page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        assert not overflow, "Page should not have horizontal overflow on mobile"
        print("✓ Zero horizontal overflow on mobile viewport!")
        
        # Simulate Swipe Left (Next Chapter: from x=320 to x=60 at y=400)
        print("Simulating Touch Swipe Left (Next Chapter)...")
        mobile_page.evaluate("""() => {
            const el = document.getElementById("mainExperience");
            const tStart = new Touch({ identifier: 1, target: el, clientX: 320, clientY: 400, pageX: 320, pageY: 400 });
            el.dispatchEvent(new TouchEvent('touchstart', { touches: [tStart], changedTouches: [tStart] }));
            
            const tEnd = new Touch({ identifier: 1, target: el, clientX: 70, clientY: 405, pageX: 70, pageY: 405 });
            el.dispatchEvent(new TouchEvent('touchend', { touches: [], changedTouches: [tEnd] }));
        }""")
        mobile_page.wait_for_timeout(1000)
        
        m_timeline = mobile_page.locator("#chapterTimeline")
        assert "page-active" in m_timeline.get_attribute("class"), "Swipe left should turn to Chapter 2 (Timeline)"
        print("✓ Mobile Swipe Left turned page to Chapter 2!")
        mobile_page.screenshot(path="screenshot_book_mobile_ch2.png")
        
        # Simulate Swipe Right (Previous Chapter: from x=70 to x=320 at y=400)
        print("Simulating Touch Swipe Right (Previous Chapter)...")
        mobile_page.evaluate("""() => {
            const el = document.getElementById("mainExperience");
            const tStart = new Touch({ identifier: 2, target: el, clientX: 70, clientY: 400, pageX: 70, pageY: 400 });
            el.dispatchEvent(new TouchEvent('touchstart', { touches: [tStart], changedTouches: [tStart] }));
            
            const tEnd = new Touch({ identifier: 2, target: el, clientX: 320, clientY: 405, pageX: 320, pageY: 405 });
            el.dispatchEvent(new TouchEvent('touchend', { touches: [], changedTouches: [tEnd] }));
        }""")
        mobile_page.wait_for_timeout(1000)
        
        m_hero = mobile_page.locator("#heroSection")
        assert "page-active" in m_hero.get_attribute("class"), "Swipe right should turn back to Chapter 1 (Hero)"
        print("✓ Mobile Swipe Right returned page to Chapter 1!")
        
        mobile_context.close()
        browser.close()
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 3D Page Turns, Navigation, Swiping, and Keys are 100% Verified!")

if __name__ == "__main__":
    run_tests()
