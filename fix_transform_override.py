import os
import sys
import io
import time
from playwright.sync_api import sync_playwright

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove !important from transform on .page-active and .page-under
content = content.replace(
    "transform: rotateY(0deg) translateZ(0) !important;",
    "transform: rotateY(0deg) translateZ(0);"
)
content = content.replace(
    "transform: rotateY(0deg) translateZ(-4px) !important;",
    "transform: rotateY(0deg) translateZ(-4px);"
)

# In goToChapter, ensure curPage removes page-active immediately when turning starts:
old_next_start = """        // Current page on top rotates from rotateY(0deg) to rotateY(-140deg)
        curPage.classList.remove("page-under", "turning-prev-in", "turning-prev-out");
        curPage.classList.add("turning-next-out");"""

new_next_start = """        // Current page on top rotates from rotateY(0deg) to rotateY(-140deg)
        curPage.classList.remove("page-active", "page-under", "turning-prev-in", "turning-prev-out");
        curPage.classList.add("turning-next-out");"""

content = content.replace(old_next_start, new_next_start)

old_prev_start = """        // Current page sits underneath
        curPage.classList.remove("page-active", "turning-next-out", "turning-prev-in");
        curPage.classList.add("turning-prev-out");"""

new_prev_start = """        // Current page sits underneath
        curPage.classList.remove("page-active", "turning-next-out", "turning-prev-in");
        curPage.classList.add("turning-prev-out");"""
# (ensure targetPage also removes page-active if it had it)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied transform override fix!")
