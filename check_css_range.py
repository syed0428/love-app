import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
old_css_start = content.find("/* ==========================================================================\n     BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE")
if old_css_start == -1:
    old_css_start = content.find("BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE")

old_css_end = content.find("/* Section padding reset within book pages */")
if old_css_end == -1:
    old_css_end = content.find("/* Bottom Navigation Bar */")

print(f"Found CSS block from {old_css_start} to {old_css_end}")
