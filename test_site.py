import os
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

def run_tests():
    file_path = "file:///" + os.path.abspath("index.html").replace("\\", "/")
    print("Testing URL:", file_path)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # Listen for console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # 1. Load Page
        page.goto(file_path)
        page.wait_for_timeout(1000)
        page.screenshot(path="screenshot_1_gift_box.png")
        print("✓ Screenshot 1: Gift box loaded")

        # 2. Click Gift Card Wrapper
        page.click("#giftCardWrapper")
        print("Clicked gift box, waiting for transition...")
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot_2_date_gate.png")
        print("✓ Screenshot 2: Date gate appeared")

        # 3. Test Date Input Auto-formatting & Unlock
        page.fill("#dateInput", "13072025")
        val = page.input_value("#dateInput")
        print("Input formatted value:", val)
        assert "13 / 07 / 2025" in val or "13/07/2025" in val, f"Formatting unexpected: {val}"

        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1500)
        page.screenshot(path="screenshot_3_proposal.png")
        print("✓ Screenshot 3: Proposal appeared")

        # 4. Test Dodging No Button
        no_btn = page.locator("#btnNo")
        init_box = no_btn.bounding_box()
        page.hover("#btnNo")
        page.wait_for_timeout(500)
        new_box = no_btn.bounding_box()
        print(f"No button moved from ({init_box['x']}, {init_box['y']}) to ({new_box['x']}, {new_box['y']})")
        assert (init_box['x'] != new_box['x']) or (init_box['y'] != new_box['y']), "No button failed to dodge!"

        # 5. Click YES Button -> Confetti and Unlock
        page.click("#btnYes")
        page.wait_for_timeout(500)
        page.screenshot(path="screenshot_4_confetti.png")
        print("✓ Screenshot 4: Confetti burst on Yes")

        page.wait_for_timeout(2000)
        page.screenshot(path="screenshot_5_hero_unlocked.png")
        print("✓ Screenshot 5: Main site unlocked")

        # 6. Test Envelopes
        page.evaluate("window.scrollTo(0, 1600)")
        page.wait_for_timeout(800)
        first_env = page.locator(".envelope-card").first
        first_env.click()
        page.wait_for_timeout(600)
        page.screenshot(path="screenshot_6_envelope_open.png")
        print("✓ Screenshot 6: Envelope opened")

        # 7. Test Wax Seal
        page.evaluate("window.scrollTo(0, 2400)")
        page.wait_for_timeout(800)
        wax_btn = page.locator("#waxSealBtn")
        wax_btn.click()
        page.wait_for_timeout(800)
        page.screenshot(path="screenshot_7_wax_letter.png")
        print("✓ Screenshot 7: Wax letter unrolled")

        # 8. Test Quiz
        page.evaluate("window.scrollTo(0, 3200)")
        page.wait_for_timeout(800)
        quiz1_correct = page.locator("#quizCard1 .quiz-btn").nth(1)
        quiz1_correct.click()
        page.wait_for_timeout(500)
        page.screenshot(path="screenshot_8_quiz.png")
        print("✓ Screenshot 8: Quiz answered")

        # 9. Test Verses Generator
        page.evaluate("window.scrollTo(0, 4000)")
        page.wait_for_timeout(800)
        verse_btn = page.locator("#btnNextVerse")
        verse_btn.click()
        page.wait_for_timeout(800)

        # 10. Test Secret Panel
        page.evaluate("window.scrollTo(0, 4800)")
        page.wait_for_timeout(1200) # let typing effect complete
        secret_btn = page.locator(".secret-trigger")
        secret_btn.click()
        page.wait_for_timeout(800)
        page.screenshot(path="screenshot_9_secret_panel.png")
        print("✓ Screenshot 9: Secret panel opened")

        print("Console errors:", console_errors)
        assert len(console_errors) == 0, f"Encountered console errors: {console_errors}"
        print("ALL TESTS PASSED SUCCESSFULLY! 🎉")

        browser.close()

if __name__ == "__main__":
    run_tests()
