import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
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

    # Scroll to Gallery
    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterGallery').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(400)

    # Verify all 6 frames have correct src, alt, caption and fallback behavior
    frames_data = page.evaluate("""() => {
        const frames = Array.from(document.querySelectorAll('.photo-frame'));
        return frames.map((f, i) => {
            const img = f.querySelector('img');
            const caption = f.querySelector('.frame-caption');
            const placeholder = f.querySelector('.placeholder-card');
            return {
                frame: i + 1,
                src: img.getAttribute('src'),
                alt: img.getAttribute('alt'),
                caption: caption.textContent.trim(),
                imgHiddenOnError: img.style.display === 'none',
                placeholderVisible: window.getComputedStyle(placeholder).display !== 'none'
            };
        });
    }""")

    print("Gallery frames verification:")
    for f in frames_data:
        print(f"Frame {f['frame']}: src='{f['src']}' | alt='{f['alt']}' | caption={f['caption']} | imgHidden={f['imgHiddenOnError']} | placeholderVisible={f['placeholderVisible']}")
        assert f['src'] == f"photo{f['frame']}.jpg", f"Mismatch in src: {f['src']}"
        assert f['imgHiddenOnError'], "Broken image icon should be hidden by onerror handler"
        assert f['placeholderVisible'], "Placeholder card should remain visible when photo not yet added"

    page.screenshot(path="screenshot_gallery_ready.png")
    print("Saved screenshot_gallery_ready.png")

    browser.close()
    print("ALL GALLERY CHECKS PASSED!")
