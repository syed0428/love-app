import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()
        
        # Navigate to local server
        url = "http://127.0.0.1:8080/index.html"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")
        
        # 1. Open Gift Box
        gift_box = page.locator("#giftBoxContainer")
        if await gift_box.is_visible():
            print("Clicking gift box...")
            await gift_box.click()
            await page.wait_for_timeout(1000)
            
        # 2. Date Gate: enter 28012023
        date_input = page.locator("#dateInput")
        if await date_input.is_visible():
            print("Entering date 28012023...")
            await date_input.fill("28012023")
            await page.wait_for_timeout(500)
            unlock_btn = page.locator("#btnDateUnlock")
            await unlock_btn.click()
            await page.wait_for_timeout(1500)
            
        # 3. Proposal: Click Yes
        yes_btn = page.locator("#btnProposalYes")
        if await yes_btn.is_visible():
            print("Clicking Yes...")
            await yes_btn.click()
            await page.wait_for_timeout(2000)
            
        # 4. Navigate to Chapter 3 (Gallery)
        # Check current chapter
        label = await page.locator("#bookNavLabel").inner_text()
        print(f"Current Book Chapter: {label}")
        
        # Jump to chapter 3 directly via dot or next button
        dots = page.locator(".book-dot")
        count = await dots.count()
        print(f"Total dots: {count}")
        if count >= 3:
            print("Clicking dot 3...")
            await dots.nth(2).click()
            await page.wait_for_timeout(1500)
            
        label = await page.locator("#bookNavLabel").inner_text()
        print(f"Now on Book Chapter: {label}")
        
        # 5. Check all 6 gallery images
        expected_captions = [
            "your favourite photo of us",
            "a trip you both loved",
            "her, mid-laugh",
            "a quiet ordinary day",
            "the two of you, together",
            "one more, just because"
        ]
        
        print("\n=== VERIFYING GALLERY FRAMES ===")
        all_passed = True
        for i in range(1, 7):
            img = page.locator(f"#galleryImg{i}")
            src = await img.get_attribute("src")
            display = await img.evaluate("el => window.getComputedStyle(el).display")
            natural_w = await img.evaluate("el => el.naturalWidth")
            natural_h = await img.evaluate("el => el.naturalHeight")
            caption_el = page.locator(f"#photoFrame{i} .frame-caption")
            caption_text = (await caption_el.inner_text()).strip()
            
            exp_cap = expected_captions[i-1]
            cap_matches = exp_cap.lower() in caption_text.lower()
            
            print(f"Frame {i}:")
            print(f"  src: {src}")
            print(f"  display: {display}")
            print(f"  natural dimensions: {natural_w}x{natural_h}")
            print(f"  caption: '{caption_text}' (matches expected: {cap_matches})")
            
            if src != f"image/photo{i}.jpg" and src != f"image/photo{i}.jpg.jpeg":
                print(f"  [FAIL] Unexpected src: {src}")
                all_passed = False
            if natural_w == 0 or natural_h == 0:
                print(f"  [FAIL] Image failed to decode: natural size is 0")
                all_passed = False
            if not cap_matches:
                print(f"  [FAIL] Caption does not match expected: {exp_cap}")
                all_passed = False
                
        # 6. Test onerror fallback behavior
        print("\n=== TESTING ONERROR FALLBACK ===")
        # Inject an invalid src into frame 1 and dispatch error event
        res = await page.evaluate("""() => {
            const img = document.getElementById("galleryImg1");
            const oldSrc = img.src;
            img.dispatchEvent(new Event("error"));
            const displayAfterError = window.getComputedStyle(img).display;
            const caption = document.querySelector("#photoFrame1 .frame-caption").innerText;
            // restore
            img.src = oldSrc;
            img.style.display = "block";
            return { displayAfterError, caption };
        }""")
        print(f"Onerror result: display={res['displayAfterError']}, caption still visible='{res['caption']}'")
        
        # Take screenshot of the gallery
        screenshot_path = "screenshot_gallery_real_photos.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"\nScreenshot saved to {screenshot_path}")
        
        if all_passed:
            print("\n>>> ALL VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<")
        else:
            print("\n>>> SOME CHECKS FAILED! <<<")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
