import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def verify_date_gate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        html_path = os.path.abspath("index.html")
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        page.wait_for_timeout(800)
        
        # Open gift box
        page.click("#giftCardWrapper")
        page.wait_for_timeout(600)
        
        # Check prompt text
        prompt = page.locator("#dateGateDialog p").text_content()
        print(f"Gate Prompt Text: '{prompt}'")
        assert "first day" in prompt.lower(), f"Prompt should mention 'first day', got: {prompt}"
        
        # Test wrong attempts and progressive hints
        date_input = page.locator("#dateInput")
        btn_submit = page.locator("#dateSubmitBtn")
        feedback = page.locator("#dateFeedback")
        
        # Attempt 1 (Wrong)
        date_input.fill("01-01-2020")
        btn_submit.click()
        page.wait_for_timeout(300)
        hint1 = feedback.text_content()
        print(f"Hint 1 after wrong attempt 1: '{hint1}'")
        assert "January 2023" in hint1, f"Expected January 2023 in hint 1, got: {hint1}"
        
        # Attempt 2 (Wrong)
        date_input.fill("02-02-2022")
        btn_submit.click()
        page.wait_for_timeout(300)
        hint2 = feedback.text_content()
        print(f"Hint 2 after wrong attempt 2: '{hint2}'")
        assert "28-01-2023" in hint2, f"Expected 28-01-2023 in hint 2, got: {hint2}"
        
        # Attempt 3 (Wrong: Old July 2025 date should fail!)
        date_input.fill("13-07-2025")
        btn_submit.click()
        page.wait_for_timeout(300)
        hint3 = feedback.text_content()
        print(f"Hint 3 after old date attempt: '{hint3}'")
        assert "28 / 01 / 2023" in hint3, f"Expected 28 / 01 / 2023 in hint 3, got: {hint3}"
        
        # Test Correct Date: 28012023
        date_input.fill("28012023")
        page.wait_for_timeout(1000)
        
        # Verify auto-format and successful unlock
        formatted_val = date_input.input_value()
        print(f"Formatted input value: '{formatted_val}'")
        assert formatted_val == "28 / 01 / 2023", f"Expected '28 / 01 / 2023', got {formatted_val}"
        
        # Wait for transition to proposal dialog
        page.wait_for_timeout(1500)
        propose_dialog = page.locator("#proposeGateDialog")
        assert "active" in propose_dialog.get_attribute("class"), "Proposal dialog should be active"
        print("✓ Correct date 28/01/2023 successfully unlocked the date gate!")
        
        # Click YES to check Day Counter
        page.click("#btnYes")
        page.wait_for_timeout(2200)
        
        counter_text = page.locator("#daysCounterText").text_content()
        print(f"Days Counter on Chapter 1: '{counter_text}'")
        assert "days of us" in counter_text
        
        page.screenshot(path="screenshot_new_date_gate_verified.png")
        browser.close()
        print("🎉 ALL DATE-GATE VERIFICATION TESTS PASSED 100%!")

if __name__ == "__main__":
    verify_date_gate()
