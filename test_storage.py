import os
from playwright.sync_api import sync_playwright

file_path = os.path.abspath("index.html")
file_url = f"file:///{file_path.replace(os.sep, '/')}"

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto(file_url)
    res = page.evaluate("""async () => {
        const hasIDB = typeof window.indexedDB !== 'undefined';
        let idbWorks = false;
        try {
            const req = indexedDB.open('TestDB', 1);
            idbWorks = await new Promise((resolve) => {
                req.onupgradeneeded = (e) => {
                    e.target.result.createObjectStore('testStore');
                };
                req.onsuccess = (e) => {
                    const db = e.target.result;
                    const tx = db.transaction('testStore', 'readwrite');
                    tx.objectStore('testStore').put('hello', 'key1');
                    tx.oncomplete = () => {
                        db.close();
                        resolve(true);
                    };
                };
                req.onerror = () => resolve(false);
            });
        } catch (e) {
            idbWorks = false;
        }

        let lsWorks = false;
        try {
            localStorage.setItem('test_ls', 'val');
            lsWorks = localStorage.getItem('test_ls') === 'val';
            localStorage.removeItem('test_ls');
        } catch(e) {
            lsWorks = false;
        }

        return { hasIDB, idbWorks, lsWorks };
    }""")
    print("Storage Test Results:", res)
    b.close()
