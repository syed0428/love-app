import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find each section
# The tags are:
# <header class="hero book-page page-active" id="heroSection"> ... </header>
# <section class="book-page" id="chapterTimeline"> ... </section>
# ...
# <section class="book-page closing-section" id="chapterClosing"> ... </section>

sec_ids = [
    ("heroSection", "header"),
    ("chapterTimeline", "section"),
    ("chapterGallery", "section"),
    ("chapterEnvelopes", "section"),
    ("chapterLetter", "section"),
    ("chapterQuiz", "section"),
    ("chapterVerses", "section"),
    ("chapterClosing", "section"),
]

for sid, tag in sec_ids:
    pattern = rf'(<{tag}[^>]*id="{sid}"[^>]*>)(.*?)(</{tag}>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(f"Found {sid} ({tag}): inner length = {len(match.group(2))}")
    else:
        print(f"FAILED to find {sid}")
