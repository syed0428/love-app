import os
import sys
import io

# Ensure UTF-8 output for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def run_tests():
    file_path = os.path.abspath("index.html")
    file_url = f"file:///{file_path.replace(os.sep, '/')}"

    viewports = [
        {"name": "iPhone SE (375x667)", "width": 375, "height": 667, "is_mobile": True},
        {"name": "iPhone 12 (390x844)", "width": 390, "height": 844, "is_mobile": True},
        {"name": "iPhone XR (414x896)", "width": 414, "height": 896, "is_mobile": True},
        {"name": "iPad Tablet (768x1024)", "width": 768, "height": 1024, "is_mobile": False},
        {"name": "Small Laptop (1024x768)", "width": 1024, "height": 768, "is_mobile": False},
        {"name": "Desktop (1440x900)", "width": 1440, "height": 900, "is_mobile": False},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for vp in viewports:
            print(f"\n==========================================")
            print(f"Testing viewport: {vp['name']}")
            print(f"==========================================")
            
            context = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                is_mobile=vp["is_mobile"],
                has_touch=vp["is_mobile"]
            )
            page = context.new_page()
            page.goto(file_url)
            page.wait_for_timeout(500)

            # 1. Test Quran Verse Section Hidden on Load
            # Check #verseBodyWrap
            wrap_display = page.evaluate("""() => {
                const wrap = document.getElementById('verseBodyWrap');
                const rect = wrap.getBoundingClientRect();
                const style = window.getComputedStyle(wrap);
                const btn = document.getElementById('btnNextVerse');
                return {
                    height: rect.height,
                    opacity: parseFloat(style.opacity),
                    maxHeight: style.maxHeight,
                    btnText: btn.textContent.trim(),
                    arabicText: document.getElementById('verseArabic').textContent.trim()
                };
            }""")
            print(f"Quran initial state: height={wrap_display['height']}, opacity={wrap_display['opacity']}, btn='{wrap_display['btnText']}', arabicText='{wrap_display['arabicText']}'")
            assert wrap_display['height'] == 0, f"Expected height 0 on load, got {wrap_display['height']}"
            assert wrap_display['opacity'] == 0, f"Expected opacity 0 on load, got {wrap_display['opacity']}"
            assert wrap_display['btnText'] == "Reveal an Ayah ✧", f"Unexpected button text: {wrap_display['btnText']}"
            assert wrap_display['arabicText'] == "", f"Expected empty arabic text on load"

            # 2. Test Unlocking Gate
            page.click("#giftCardWrapper")
            page.wait_for_timeout(700)
            page.fill("#dateInput", "13-07-2025")
            page.click("#dateSubmitBtn")
            page.wait_for_timeout(1000)

            # Accept proposal
            page.click("#btnYes")
            page.wait_for_timeout(1000)

            # 3. Test Quran Verse Reveal on Click
            page.evaluate("() => document.getElementById('chapterVerses').scrollIntoView()")
            page.wait_for_timeout(500)
            
            # Click Reveal button
            page.click("#btnNextVerse")
            page.wait_for_timeout(800)

            first_reveal = page.evaluate("""() => {
                const wrap = document.getElementById('verseBodyWrap');
                const rect = wrap.getBoundingClientRect();
                const style = window.getComputedStyle(wrap);
                const btn = document.getElementById('btnNextVerse');
                return {
                    height: rect.height,
                    opacity: parseFloat(style.opacity),
                    hasRevealedClass: wrap.classList.contains('revealed'),
                    btnText: btn.textContent.trim(),
                    arabicText: document.getElementById('verseArabic').textContent.trim(),
                    refText: document.getElementById('verseReference').textContent.trim()
                };
            }""")
            print(f"Quran first click: height={first_reveal['height']}, opacity={first_reveal['opacity']}, btn='{first_reveal['btnText']}', ref='{first_reveal['refText']}'")
            assert first_reveal['height'] > 30, f"Expected verse to expand, height is {first_reveal['height']}"
            assert first_reveal['opacity'] == 1, f"Expected opacity 1, got {first_reveal['opacity']}"
            assert first_reveal['hasRevealedClass'], "Expected 'revealed' class"
            assert first_reveal['btnText'] == "Show Me Another Ayah ✧", f"Unexpected button text: {first_reveal['btnText']}"
            assert len(first_reveal['arabicText']) > 5, "Arabic text should be populated"

            # Click again for next verse
            prev_ref = first_reveal['refText']
            page.click("#btnNextVerse")
            page.wait_for_timeout(600)

            second_reveal = page.evaluate("""() => {
                const btn = document.getElementById('btnNextVerse');
                return {
                    arabicText: document.getElementById('verseArabic').textContent.trim(),
                    refText: document.getElementById('verseReference').textContent.trim(),
                    btnText: btn.textContent.trim()
                };
            }""")
            print(f"Quran second click: ref='{second_reveal['refText']}' (previous='{prev_ref}')")
            assert second_reveal['refText'] != prev_ref, "Second click should produce a different verse"

            # 4. Test Touch Target sizes on mobile
            btn_sizes = page.evaluate("""() => {
                const targets = [
                    { id: 'btnNextVerse', el: document.getElementById('btnNextVerse') },
                    { id: 'quizBtn', el: document.querySelector('.quiz-btn') },
                    { id: 'envelopeCard', el: document.querySelector('.envelope-card') }
                ];
                return targets.map(t => {
                    const r = t.el.getBoundingClientRect();
                    return { id: t.id, width: r.width, height: r.height };
                });
            }""")
            for t in btn_sizes:
                print(f"Target size: {t['id']} -> {t['width']}x{t['height']}px")
                assert t['height'] >= 42, f"Target {t['id']} too small: height is {t['height']}"

            # 5. Test Envelope Opening & reflow
            page.evaluate("() => document.getElementById('chapterEnvelopes').scrollIntoView()")
            page.wait_for_timeout(300)
            page.click(".envelope-card")
            page.wait_for_timeout(500)
            env_open = page.evaluate("""() => {
                const env = document.querySelector('.envelope-card');
                const content = env.querySelector('.env-content');
                return {
                    isOpen: env.classList.contains('open'),
                    contentHeight: content.getBoundingClientRect().height
                };
            }""")
            assert env_open['isOpen'], "Envelope should be open"
            assert env_open['contentHeight'] > 20, "Envelope content should be visible"

            # 6. Test Horizontal Overflow across the entire page
            overflow_check = page.evaluate("""() => {
                const docWidth = document.documentElement.offsetWidth;
                const winWidth = window.innerWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                const elementsWithOverflow = [];
                document.querySelectorAll('*').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > winWidth + 1) {
                        elementsWithOverflow.push({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            right: rect.right,
                            winWidth: winWidth
                        });
                    }
                });
                return {
                    docWidth, winWidth, scrollWidth,
                    hasOverflow: scrollWidth > winWidth,
                    elementsCount: elementsWithOverflow.length,
                    elements: elementsWithOverflow.slice(0, 5)
                };
            }""")
            print(f"Horizontal check: scrollWidth={overflow_check['scrollWidth']}, winWidth={overflow_check['winWidth']}, hasOverflow={overflow_check['hasOverflow']}")
            assert not overflow_check['hasOverflow'], f"Horizontal overflow detected: {overflow_check}"

            # 7. Test Dodging No Button Bounds on mobile
            if vp['is_mobile']:
                page.evaluate("() => { if (typeof dodgeNoButton === 'function') dodgeNoButton(); }")
                no_btn_pos = page.evaluate("""() => {
                    const b = document.getElementById('btnNo');
                    const r = b.getBoundingClientRect();
                    return {
                        left: r.left,
                        top: r.top,
                        right: r.right,
                        bottom: r.bottom,
                        winW: window.innerWidth,
                        winH: window.innerHeight
                    };
                }""")
                print(f"Dodging No button position on mobile: left={no_btn_pos['left']}, right={no_btn_pos['right']}, winW={no_btn_pos['winW']}")
                assert no_btn_pos['left'] >= 0, "No button left offscreen"
                assert no_btn_pos['right'] <= no_btn_pos['winW'] + 2, "No button right offscreen"

            # Capture screenshot
            screenshot_path = f"screenshot_verify_{vp['width']}.png"
            page.screenshot(path=screenshot_path)
            print(f"Saved screenshot to {screenshot_path}")

            context.close()

        browser.close()
        print("\nALL RESPONSIVE AND QURAN VERSE TESTS PASSED CLEANLY!")

if __name__ == "__main__":
    run_tests()
