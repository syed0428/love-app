import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 960})
        page = await context.new_page()
        
        url = "http://127.0.0.1:8080/index.html"
        await page.goto(url, wait_until="networkidle")
        
        # Unlock everything and jump straight to Chapter 3 (Gallery)
        await page.evaluate("""() => {
            const gift = document.getElementById("introOverlay");
            if (gift) gift.style.display = "none";
            const gate = document.getElementById("gateOverlay");
            if (gate) {
                gate.classList.add("hidden");
                gate.style.display = "none";
            }
            const main = document.getElementById("mainExperience");
            if (main) {
                main.classList.add("revealed");
                main.style.opacity = "1";
                main.style.display = "block";
            }
            
            // Init book and jump to Chapter 3
            if (typeof initBookExperience === 'function') {
                initBookExperience();
            }
            if (typeof goToChapter === 'function') {
                goToChapter(2); // index 2 is Chapter 3
            }
        }""")
        
        await page.wait_for_timeout(1500)
        
        # Capture screenshot of gallery
        await page.screenshot(path="screenshot_gallery_loaded_full.png", full_page=False)
        print("Captured screenshot_gallery_loaded_full.png")
        
        # Check details of each image frame
        for i in range(1, 7):
            info = await page.evaluate(f"""() => {{
                const img = document.getElementById('galleryImg{i}');
                const p = document.getElementById('placeholder{i}');
                const cap = document.querySelector('#photoFrame{i} .frame-caption').innerText;
                const rect = img.getBoundingClientRect();
                return {{
                    src: img.getAttribute('src'),
                    display: window.getComputedStyle(img).display,
                    renderedSize: `${{Math.round(rect.width)}}x${{Math.round(rect.height)}}`,
                    caption: cap
                }};
            }}""")
            print(f"Frame {i}: {info}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
