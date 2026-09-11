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
    page.wait_for_timeout(1000)
    page.click("#btnYes")
    page.wait_for_timeout(2000)

    # Scroll to envelopes without clicking them
    page.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; document.getElementById('chapterEnvelopes').scrollIntoView({ block: 'center' }); }")
    page.wait_for_timeout(500)

    info = page.evaluate("""() => {
        const cards = Array.from(document.querySelectorAll('.envelope-card'));
        return cards.map(c => {
            const content = c.querySelector('.env-content');
            const teaser = c.querySelector('.env-teaser');
            const cRect = c.getBoundingClientRect();
            const contRect = content.getBoundingClientRect();
            const cStyle = window.getComputedStyle(c);
            const contStyle = window.getComputedStyle(content);
            return {
                cardHeight: cRect.height,
                cardWidth: cRect.width,
                contentHeight: contRect.height,
                contentOpacity: contStyle.opacity,
                contentMaxHeight: contStyle.maxHeight,
                contentDisplay: contStyle.display,
                contentOverflow: contStyle.overflow,
                isOpen: c.classList.contains('open'),
                teaserDisplay: window.getComputedStyle(teaser).display,
                teaserText: teaser.textContent
            };
        });
    }""")
    print("Initial envelopes state (closed):")
    for i, card in enumerate(info):
        print(f"Card {i+1}: cardHeight={card['cardHeight']}, contentHeight={card['contentHeight']}, contentOpacity={card['contentOpacity']}, isOpen={card['isOpen']}")

    page.screenshot(path="screenshot_envelopes_fresh.png")
    print("Saved screenshot_envelopes_fresh.png")

    # Now click card 1
    page.click(".envelope-card:nth-child(1)")
    page.wait_for_timeout(600)
    
    info_opened = page.evaluate("""() => {
        const cards = Array.from(document.querySelectorAll('.envelope-card'));
        return cards.map(c => {
            const content = c.querySelector('.env-content');
            return {
                cardHeight: c.getBoundingClientRect().height,
                contentHeight: content.getBoundingClientRect().height,
                isOpen: c.classList.contains('open')
            };
        });
    }""")
    print("\nAfter clicking Card 1:")
    for i, card in enumerate(info_opened):
        print(f"Card {i+1}: cardHeight={card['cardHeight']}, contentHeight={card['contentHeight']}, isOpen={card['isOpen']}")
        
    page.screenshot(path="screenshot_envelopes_card1_open.png")
    print("Saved screenshot_envelopes_card1_open.png")

    # Click Card 1 again to toggle close
    page.click(".envelope-card:nth-child(1)")
    page.wait_for_timeout(600)
    info_closed = page.evaluate("""() => {
        const c = document.querySelector('.envelope-card:nth-child(1)');
        return {
            cardHeight: c.getBoundingClientRect().height,
            contentHeight: c.querySelector('.env-content').getBoundingClientRect().height,
            isOpen: c.classList.contains('open')
        };
    }""")
    print(f"\nAfter clicking Card 1 again: cardHeight={info_closed['cardHeight']}, contentHeight={info_closed['contentHeight']}, isOpen={info_closed['isOpen']}")

    browser.close()
