import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 960})
        page = await context.new_page()
        
        url = "http://127.0.0.1:8080/index.html"
        await page.goto(url, wait_until="networkidle")
        
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
            if (typeof initBookExperience === 'function') {
                initBookExperience();
            }
            if (typeof goToChapter === 'function') {
                goToChapter(2);
            }
        }""")
        
        await page.wait_for_timeout(1500)
        
        # Scroll the chapter scroll container down
        await page.evaluate("""() => {
            const scroller = document.querySelector('#chapterGallery .book-page-scroll');
            if (scroller) {
                scroller.scrollTop = 420;
            }
        }""")
        await page.wait_for_timeout(500)
        
        await page.screenshot(path="screenshot_gallery_bottom_row.png", full_page=False)
        print("Captured screenshot_gallery_bottom_row.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
