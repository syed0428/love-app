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
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(file_url)
    page.wait_for_timeout(500)

    # 1. Unlock gate
    page.click("#giftCardWrapper")
    page.wait_for_timeout(600)
    page.fill("#dateInput", "13-07-2025")
    page.click("#dateSubmitBtn")
    page.wait_for_timeout(1800)
    page.click("#btnYes")
    page.wait_for_timeout(2000)

    # 2. Scroll to gallery
    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterGallery').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(400)

    # 3. Check initial empty state: "Add Photo" buttons present, NO delete buttons
    initial_check = page.evaluate("""() => {
        const addBtns = document.querySelectorAll('.btn-add-photo');
        const deleteBtns = document.querySelectorAll('.btn-delete, .btn-remove, [data-action="delete"]');
        const img1 = document.getElementById('galleryImg1');
        const placeholder1 = document.getElementById('placeholder1');
        const change1 = document.getElementById('btnChange1');
        return {
            addBtnsCount: addBtns.length,
            deleteBtnsCount: deleteBtns.length,
            img1Visible: window.getComputedStyle(img1).display !== 'none',
            placeholder1Visible: window.getComputedStyle(placeholder1).display !== 'none',
            change1Visible: window.getComputedStyle(change1).display !== 'none'
        };
    }""")

    print("Initial Gallery State:", initial_check)
    assert initial_check['addBtnsCount'] == 6, f"Expected 6 Add Photo buttons, found {initial_check['addBtnsCount']}"
    assert initial_check['deleteBtnsCount'] == 0, f"Critical constraint: found {initial_check['deleteBtnsCount']} delete buttons (should be 0)!"
    assert initial_check['placeholder1Visible'], "Placeholder 1 should be visible"
    assert not initial_check['img1Visible'], "Image 1 should be hidden initially"
    assert not initial_check['change1Visible'], "Change button should be hidden initially"

    page.screenshot(path="screenshot_gallery_upload_empty.png")
    print("Saved screenshot_gallery_upload_empty.png")

    # 4. Upload photo to Frame 1
    print("\nUploading photo to Frame 1...")
    page.set_input_files("#photoInput1", sample_img)
    page.wait_for_timeout(1200)

    uploaded_check = page.evaluate("""() => {
        const img1 = document.getElementById('galleryImg1');
        const placeholder1 = document.getElementById('placeholder1');
        const change1 = document.getElementById('btnChange1');
        return {
            img1SrcLen: img1.src.length,
            img1IsDataUrl: img1.src.startsWith('data:image/'),
            img1Visible: img1.style.display === 'block',
            placeholder1Visible: placeholder1.style.display !== 'none',
            change1Visible: change1.style.display === 'inline-flex'
        };
    }""")
    print("After Uploading to Frame 1:", uploaded_check)
    assert uploaded_check['img1IsDataUrl'], "Image 1 src should be a base64 data URL"
    assert uploaded_check['img1Visible'], "Image 1 should now be visible (display: block)"
    assert not uploaded_check['placeholder1Visible'], "Placeholder 1 should be hidden"
    assert uploaded_check['change1Visible'], "Change button should now be visible"

    page.screenshot(path="screenshot_gallery_upload_with_photo.png")
    print("Saved screenshot_gallery_upload_with_photo.png")

    # 5. Test Persistence Across Page Reload
    print("\nReloading page to test IndexedDB persistence...")
    page.reload()
    page.wait_for_timeout(800)

    # Fast forward through gate
    page.click("#giftCardWrapper")
    page.wait_for_timeout(600)
    page.fill("#dateInput", "13-07-2025")
    page.click("#dateSubmitBtn")
    page.wait_for_timeout(1800)
    page.click("#btnYes")
    page.wait_for_timeout(2000)

    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterGallery').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(600)

    persisted_check = page.evaluate("""() => {
        const img1 = document.getElementById('galleryImg1');
        const placeholder1 = document.getElementById('placeholder1');
        const change1 = document.getElementById('btnChange1');
        return {
            img1SrcLen: img1.src.length,
            img1IsDataUrl: img1.src.startsWith('data:image/'),
            img1Visible: img1.style.display === 'block',
            placeholder1Visible: placeholder1.style.display !== 'none',
            change1Visible: change1.style.display === 'inline-flex'
        };
    }""")
    print("After Page Reload (Persistence Check):", persisted_check)
    assert persisted_check['img1IsDataUrl'], "Image 1 should still have data URL from IndexedDB after reload"
    assert persisted_check['img1Visible'], "Image 1 should be automatically displayed after reload"
    assert not persisted_check['placeholder1Visible'], "Placeholder 1 should remain hidden after reload"
    assert persisted_check['change1Visible'], "Change button should be visible after reload"

    # 6. Verify NO delete buttons exist after upload or reload
    delete_check = page.evaluate("() => document.querySelectorAll('.btn-delete, .btn-remove, [data-action=\"delete\"]').length")
    assert delete_check == 0, "No delete buttons should exist anywhere!"
    print(f"Zero delete buttons verified (count = {delete_check})")

    browser.close()
    print("\nALL IN-BROWSER PHOTO UPLOAD & INDEXEDDB TESTS PASSED PERFECTLY!")
