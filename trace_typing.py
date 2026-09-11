import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///' + os.path.abspath('index.html').replace('\\', '/'))
    page.click('#giftCardWrapper')
    page.wait_for_timeout(2500)
    
    # Listen to console
    page.on('console', lambda msg: print('PAGE LOG:', msg.text))
    
    # Add debug listener in page
    page.evaluate('''() => {
      document.getElementById('dateInput').addEventListener('input', (e) => {
        console.log('INPUT EVENT val:', e.target.value, 'selectionStart:', e.target.selectionStart);
      });
    }''')
    
    input_el = page.locator('#dateInput')
    for ch in "13072025":
        input_el.type(ch)
        page.wait_for_timeout(50)
        print(f"Typed '{ch}', current value: '{input_el.input_value()}'")
        
    browser.close()
