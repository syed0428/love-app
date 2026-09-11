import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

def test_device(vp_name, width, height, is_mobile):
    print(f"\n==========================================")
    print(f"Testing on {vp_name} ({width}x{height})")
    print(f"==========================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            is_mobile=is_mobile,
            has_touch=is_mobile
        )
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_timeout(500)

        # ----------------------------------------------------------------------
        # TEST 1: PROPOSAL DODGING "NO" BUTTON (BOUNDS + NO SCROLLBAR)
        # ----------------------------------------------------------------------
        # Open gift box and submit date
        page.click("#giftCardWrapper")
        page.wait_for_timeout(600)
        page.fill("#dateInput", "13-07-2025")
        page.click("#dateSubmitBtn")
        page.wait_for_timeout(1800)

        # Verify initial No button presence and position
        init_state = page.evaluate("""() => {
            const btnNo = document.getElementById('btnNo');
            const r = btnNo.getBoundingClientRect();
            const cs = window.getComputedStyle(btnNo);
            const spacer = document.querySelector('.no-spacer').getBoundingClientRect();
            return {
                display: cs.display,
                width: r.width,
                height: r.height,
                left: r.left,
                top: r.top,
                spacerLeft: spacer.left,
                spacerTop: spacer.top,
                scrollW: document.documentElement.scrollWidth,
                winW: window.innerWidth
            };
        }""")
        print(f"Initial No button: display={init_state['display']}, size={init_state['width']}x{init_state['height']}px at ({init_state['left']:.1f}, {init_state['top']:.1f})")
        assert init_state['display'] in ('inline-flex', 'flex'), f"Expected flex/inline-flex, got {init_state['display']}"
        assert abs(init_state['left'] - init_state['spacerLeft']) < 5, "No button should align with spacer initially"

        # Dodge 15 times and check strict viewport bounds & horizontal scrollbar
        print("Testing 15 consecutive dodges for bounds and scrollbar...")
        for dodge_i in range(15):
            dodge_info = page.evaluate("""() => {
                dodgeNoButton();
                const btnNo = document.getElementById('btnNo');
                const btnYes = document.getElementById('btnYes');
                const r = btnNo.getBoundingClientRect();
                const yR = btnYes.getBoundingClientRect();
                const winW = window.innerWidth;
                const winH = window.innerHeight;
                const scrollW = document.documentElement.scrollWidth;

                const noCenterX = r.left + r.width / 2;
                const noCenterY = r.top + r.height / 2;
                const yesCenterX = yR.left + yR.width / 2;
                const yesCenterY = yR.top + yR.height / 2;
                const distToYes = Math.hypot(noCenterX - yesCenterX, noCenterY - yesCenterY);

                return {
                    left: r.left,
                    right: r.right,
                    top: r.top,
                    bottom: r.bottom,
                    winW: winW,
                    winH: winH,
                    scrollW: scrollW,
                    hasScrollbar: scrollW > winW,
                    distToYes: distToYes,
                    isOffscreen: r.left < 0 || r.right > winW || r.top < 0 || r.bottom > winH
                };
            }""")
            
            # Assertions
            assert not dodge_info['hasScrollbar'], f"Dodge {dodge_i+1} caused horizontal scrollbar! scrollW={dodge_info['scrollW']}, winW={dodge_info['winW']}"
            assert not dodge_info['isOffscreen'], f"Dodge {dodge_i+1} went offscreen! {dodge_info}"
            assert dodge_info['left'] >= 15, f"Dodge {dodge_i+1} too close to left: {dodge_info['left']}"
            assert dodge_info['right'] <= dodge_info['winW'] - 15, f"Dodge {dodge_i+1} too close to right: {dodge_info['right']} vs winW={dodge_info['winW']}"
            assert dodge_info['top'] >= 15, f"Dodge {dodge_i+1} too close to top: {dodge_info['top']}"
            assert dodge_info['bottom'] <= dodge_info['winH'] - 15, f"Dodge {dodge_i+1} too close to bottom: {dodge_info['bottom']} vs winH={dodge_info['winH']}"

        print("-> All 15 dodges strictly constrained within viewport with zero scrollbar!")

        # Screenshot proposal after dodging
        page.screenshot(path=f"screenshot_proposal_dodge_{width}.png")

        # ----------------------------------------------------------------------
        # TEST 2: LOVE-NOTE ENVELOPES COMPACT DEFAULT & TOGGLE FLOW
        # ----------------------------------------------------------------------
        # Accept proposal
        page.click("#btnYes")
        page.wait_for_timeout(2000)

        # Scroll to Chapter 3 (Envelopes)
        page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterEnvelopes').scrollIntoView({ block: 'center' }); }")
        page.wait_for_timeout(400)

        # Check default closed state
        env_init = page.evaluate("""() => {
            const cards = Array.from(document.querySelectorAll('.envelope-card'));
            return cards.map((c, idx) => {
                const cont = c.querySelector('.env-content');
                const teaser = c.querySelector('.env-teaser');
                const r = c.getBoundingClientRect();
                const contStyle = window.getComputedStyle(cont);
                const teaserStyle = window.getComputedStyle(teaser);
                return {
                    idx: idx + 1,
                    cardHeight: r.height,
                    isOpen: c.classList.contains('open'),
                    contentDisplay: contStyle.display,
                    contentOpacity: parseFloat(contStyle.opacity),
                    contentMaxHeight: contStyle.maxHeight,
                    teaserDisplay: teaserStyle.display,
                    teaserVisible: teaserStyle.display !== 'none'
                };
            });
        }""")

        print("\nLove-note envelopes default closed state:")
        for c in env_init:
            print(f"Card {c['idx']}: height={c['cardHeight']:.1f}px, isOpen={c['isOpen']}, contentDisplay='{c['contentDisplay']}', teaserVisible={c['teaserVisible']}")
            assert not c['isOpen'], f"Card {c['idx']} should NOT be open on load"
            assert c['contentDisplay'] == 'none', f"Card {c['idx']} contentDisplay should be 'none'"
            assert c['cardHeight'] < 190, f"Card {c['idx']} should be compact (height < 190px), got {c['cardHeight']}"
            assert c['teaserVisible'], f"Card {c['idx']} teaser should be visible"

        page.screenshot(path=f"screenshot_envelopes_compact_{width}.png")
        print(f"Saved screenshot_envelopes_compact_{width}.png")

        # Click Card 1 to open it
        page.click(".envelope-card:nth-child(1)")
        page.wait_for_timeout(600)

        env_after_click1 = page.evaluate("""() => {
            const cards = Array.from(document.querySelectorAll('.envelope-card'));
            return cards.map((c, idx) => {
                const cont = c.querySelector('.env-content');
                const r = c.getBoundingClientRect();
                const contStyle = window.getComputedStyle(cont);
                return {
                    idx: idx + 1,
                    cardHeight: r.height,
                    isOpen: c.classList.contains('open'),
                    contentDisplay: contStyle.display,
                    contentOpacity: parseFloat(contStyle.opacity)
                };
            });
        }""")

        print("\nAfter clicking Card 1:")
        print(f"Card 1: height={env_after_click1[0]['cardHeight']:.1f}px, isOpen={env_after_click1[0]['isOpen']}, contentDisplay='{env_after_click1[0]['contentDisplay']}'")
        print(f"Card 2: height={env_after_click1[1]['cardHeight']:.1f}px, isOpen={env_after_click1[1]['isOpen']} (should remain compact!)")
        print(f"Card 3: height={env_after_click1[2]['cardHeight']:.1f}px, isOpen={env_after_click1[2]['isOpen']} (should remain compact!)")

        assert env_after_click1[0]['isOpen'], "Card 1 should be open"
        assert env_after_click1[0]['contentDisplay'] == 'block', "Card 1 content should be 'block'"
        assert env_after_click1[0]['cardHeight'] > 250, "Card 1 should expand to reveal full message"

        # Cards 2 and 3 should NOT stretch
        if width > 860:
            assert env_after_click1[1]['cardHeight'] < 190, f"Card 2 should remain compact (< 190px), got {env_after_click1[1]['cardHeight']}"
            assert env_after_click1[2]['cardHeight'] < 190, f"Card 3 should remain compact (< 190px), got {env_after_click1[2]['cardHeight']}"

        page.screenshot(path=f"screenshot_envelopes_opened_{width}.png")
        print(f"Saved screenshot_envelopes_opened_{width}.png")

        # Click Card 1 again to close it
        page.click(".envelope-card:nth-child(1)")
        page.wait_for_timeout(600)

        card1_closed = page.evaluate("""() => {
            const c = document.querySelector('.envelope-card:nth-child(1)');
            const cont = c.querySelector('.env-content');
            return {
                cardHeight: c.getBoundingClientRect().height,
                isOpen: c.classList.contains('open'),
                contentDisplay: window.getComputedStyle(cont).display
            };
        }""")
        print(f"\nAfter clicking Card 1 again (closing): height={card1_closed['cardHeight']:.1f}px, isOpen={card1_closed['isOpen']}")
        assert not card1_closed['isOpen'], "Card 1 should toggle back to closed"

        context.close()
        browser.close()
        print(f"ALL TESTS PASSED on {vp_name}!\n")

if __name__ == "__main__":
    test_device("Desktop", 1280, 800, False)
    test_device("Mobile Phone", 375, 667, True)
    print("ALL TESTS PASSED ACROSS BOTH DESKTOP AND MOBILE!")
