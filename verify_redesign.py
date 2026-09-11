import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"
sample_img = os.path.abspath("nebula_backdrop.jpg")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop Test (1280x800)
    print("\n--- Testing on Desktop (1280x800) ---")
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Unlock gate
    page.click("#giftCardWrapper")
    page.wait_for_timeout(600)
    page.fill("#dateInput", "13-07-2025")
    page.click("#dateSubmitBtn")
    page.wait_for_timeout(1800)
    page.click("#btnYes")
    page.wait_for_timeout(2000)

    # Scroll to gallery
    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterGallery').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(400)

    desktop_check = page.evaluate("""() => {
        const frames = Array.from(document.querySelectorAll('.photo-frame'));
        const hearts = document.querySelectorAll('.memory-heart-icon');
        const addBtns = document.querySelectorAll('.btn-add-photo');
        const stars = document.querySelectorAll('.star-icon');
        const winW = window.innerWidth;
        const scrollW = document.documentElement.scrollWidth;
        
        return {
            framesCount: frames.length,
            heartsCount: hearts.length,
            starsCount: stars.length,
            addBtnsCount: addBtns.length,
            hasOverflow: scrollW > winW,
            rotations: frames.map(f => window.getComputedStyle(f).transform),
            aspectRatios: frames.map(f => window.getComputedStyle(f.querySelector('.frame-inner')).aspectRatio)
        };
    }""")

    print(f"Frames count: {desktop_check['framesCount']}")
    print(f"Hearts count: {desktop_check['heartsCount']} (Stars count: {desktop_check['starsCount']} - should be 0!)")
    print(f"Add memory buttons: {desktop_check['addBtnsCount']}")
    print(f"Horizontal scroll overflow: {desktop_check['hasOverflow']}")
    assert desktop_check['starsCount'] == 0, "Star icons should be completely removed!"
    assert desktop_check['heartsCount'] == 6, "Delicate heart icons should be present on all 6 frames!"
    assert not desktop_check['hasOverflow'], "Desktop layout should have no horizontal overflow!"

    page.screenshot(path="screenshot_redesign_desktop.png")
    print("Saved screenshot_redesign_desktop.png")

    # Upload a photo to Frame 1 to test polaroid rendering & hover change button
    page.set_input_files("#photoInput1", sample_img)
    page.wait_for_timeout(1000)

    hover_test = page.evaluate("""() => {
        const frame1 = document.getElementById('photoFrame1');
        const btnChange = document.getElementById('btnChange1');
        const img1 = document.getElementById('galleryImg1');
        
        // Initial state before hover on desktop
        const initialOpacity = parseFloat(window.getComputedStyle(btnChange).opacity);
        return {
            hasPhotoClass: frame1.classList.contains('has-photo'),
            imgDisplayed: img1.style.display === 'block',
            initialBtnOpacity: initialOpacity
        };
    }""")
    print(f"After photo upload: hasPhotoClass={hover_test['hasPhotoClass']}, imgDisplayed={hover_test['imgDisplayed']}")
    assert hover_test['hasPhotoClass'], "Frame should have .has-photo class"
    assert hover_test['imgDisplayed'], "Image should be displayed"

    # Hover over Frame 1
    page.hover("#photoFrame1")
    page.wait_for_timeout(300)

    hover_active = page.evaluate("""() => {
        const btnChange = document.getElementById('btnChange1');
        return {
            hoverBtnOpacity: parseFloat(window.getComputedStyle(btnChange).opacity),
            hoverBtnDisplay: window.getComputedStyle(btnChange).display
        };
    }""")
    print(f"Hover state over photo frame: opacity={hover_active['hoverBtnOpacity']}, display='{hover_active['hoverBtnDisplay']}'")
    assert hover_active['hoverBtnOpacity'] > 0.5, "Change button should be visible on hover"

    page.screenshot(path="screenshot_redesign_photo_hover.png")
    print("Saved screenshot_redesign_photo_hover.png")

    page.close()

    # 2. Mobile Viewport Test (375x667)
    print("\n--- Testing on Mobile (375x667) ---")
    page_m = browser.new_page(viewport={"width": 375, "height": 667}, is_mobile=True, has_touch=True)
    page_m.goto(file_url)
    page_m.wait_for_timeout(500)

    # Unlock gate
    page_m.click("#giftCardWrapper")
    page_m.wait_for_timeout(600)
    page_m.fill("#dateInput", "13-07-2025")
    page_m.click("#dateSubmitBtn")
    page_m.wait_for_timeout(1800)
    page_m.click("#btnYes")
    page_m.wait_for_timeout(2000)

    # Scroll to gallery
    page_m.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterGallery').scrollIntoView({ block: 'center' }); }")
    page_m.wait_for_timeout(400)

    mobile_check = page_m.evaluate("""() => {
        const winW = window.innerWidth;
        const scrollW = document.documentElement.scrollWidth;
        const frames = Array.from(document.querySelectorAll('.photo-frame'));
        return {
            winW, scrollW,
            hasOverflow: scrollW > winW,
            framesCount: frames.length,
            firstFrameW: frames[0].getBoundingClientRect().width
        };
    }""")
    print(f"Mobile check: winW={mobile_check['winW']}, scrollW={mobile_check['scrollW']}, hasOverflow={mobile_check['hasOverflow']}, frameWidth={mobile_check['firstFrameW']:.1f}px")
    assert not mobile_check['hasOverflow'], "Mobile layout should have no horizontal overflow!"

    page_m.screenshot(path="screenshot_redesign_mobile.png")
    print("Saved screenshot_redesign_mobile.png")

    # Reset IndexedDB for user
    page_m.evaluate("""() => {
        indexedDB.deleteDatabase("HayathiLoveGalleryDB");
        for (let i = 1; i <= 6; i++) {
            localStorage.removeItem("hayathi_gallery_" + i);
        }
    }""")
    print("Reset gallery DB for fresh user experience.")

    browser.close()
    print("\nALL ROMANTIC MEMORY WALL REDESIGN TESTS PASSED!")
