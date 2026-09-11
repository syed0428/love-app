import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1000, "height": 700})
    page.goto(file_url)
    page.wait_for_timeout(500)

    # Unlock first dialog to get to propose dialog
    page.click("#giftCardWrapper")
    page.wait_for_timeout(600)
    page.fill("#dateInput", "13-07-2025")
    page.click("#dateSubmitBtn")
    page.wait_for_timeout(1800)

    # Check btnNo's containing block and offsetParent
    parent_info = page.evaluate("""() => {
        const btn = document.getElementById('btnNo');
        const dialog = document.getElementById('proposeGateDialog');
        const gate = document.getElementById('gateOverlay');
        
        let p = btn.parentElement;
        const ancestors = [];
        while (p) {
            const cs = window.getComputedStyle(p);
            ancestors.push({
                tag: p.tagName,
                id: p.id,
                className: p.className,
                transform: cs.transform,
                backdropFilter: cs.backdropFilter || cs.webkitBackdropFilter,
                filter: cs.filter,
                perspective: cs.perspective
            });
            p = p.parentElement;
        }
        return {
            offsetParent: btn.offsetParent ? btn.offsetParent.id || btn.offsetParent.className : 'null',
            ancestorsWithContainingBlockProps: ancestors.filter(a => 
                a.transform !== 'none' || 
                (a.backdropFilter && a.backdropFilter !== 'none') || 
                (a.filter && a.filter !== 'none')
            )
        };
    }""")
    print("Containing block diagnosis:", parent_info)

    # Test dodge 5 times and check bounding rect & scrollWidth
    for i in range(5):
        pos = page.evaluate("""() => {
            dodgeNoButton();
            const btn = document.getElementById('btnNo');
            const r = btn.getBoundingClientRect();
            return {
                styleLeft: btn.style.left,
                styleTop: btn.style.top,
                rectLeft: r.left,
                rectRight: r.right,
                rectTop: r.top,
                rectBottom: r.bottom,
                winW: window.innerWidth,
                winH: window.innerHeight,
                docScrollW: document.documentElement.scrollWidth,
                bodyScrollW: document.body.scrollWidth
            };
        }""")
        print(f"Dodge {i+1}: style=({pos['styleLeft']}, {pos['styleTop']}) | rect=({pos['rectLeft']:.1f}, {pos['rectRight']:.1f}) | winW={pos['winW']} | scrollW={pos['docScrollW']}")

    browser.close()
