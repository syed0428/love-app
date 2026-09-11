import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS block from BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE to /* Bottom Navigation Bar */
css_start = content.find("/* ==========================================================================\n     BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE")
if css_start == -1:
    css_start = content.find("BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE")
    # find the preceding comment start
    css_start = content.rfind("/*", 0, css_start)

css_end = content.find("/* Bottom Navigation Bar */")

new_css = """/* ==========================================================================
     AUTHENTIC 3D BOOK PAGE-TURN ARCHITECTURE
     ========================================================================== */
    .site-main {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100svh;
      height: 100dvh;
      overflow: hidden;
      z-index: 3;
      opacity: 0;
      transition: opacity 1.2s ease 0.3s;
      perspective: 1200px;
      -webkit-perspective: 1200px;
      perspective-origin: 50% 50%;
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      pointer-events: none;
    }

    .site-main.revealed {
      opacity: 1;
      pointer-events: auto;
    }

    /* The 3D Book Page Leaf (Rotates in true 3D space along left spine) */
    .book-page {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      transform-origin: 0% 50%;
      -webkit-transform-origin: 0% 50%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      display: none;
      visibility: hidden;
      pointer-events: none;
      will-change: transform;
      background: radial-gradient(circle at 45% 40%, rgba(32, 10, 44, 0.98), rgba(7, 2, 14, 0.99) 75%), var(--space-void);
      border-right: 1px solid rgba(244, 213, 224, 0.3);
      box-shadow: 0 10px 45px rgba(0, 0, 0, 0.85);
      overflow: visible !important;
    }

    /* Active Page (Resting flat at 0deg) */
    .book-page.page-active {
      display: block !important;
      visibility: visible !important;
      pointer-events: auto !important;
      z-index: 10 !important;
      transform: rotateY(0deg) translateZ(0) !important;
      opacity: 1 !important;
    }

    /* Page Resting Underneath (Ready to be revealed as top page turns) */
    .book-page.page-under {
      display: block !important;
      visibility: visible !important;
      pointer-events: none !important;
      z-index: 5 !important;
      transform: rotateY(0deg) translateZ(-4px) !important;
      opacity: 1 !important;
    }

    /* Internal Scroll Container (Handles scrolling without breaking parent 3D) */
    .book-page-scroll {
      width: 100%;
      height: 100%;
      overflow-y: auto;
      overflow-x: hidden;
      -webkit-overflow-scrolling: touch;
      box-sizing: border-box;
      padding-top: calc(28px + env(safe-area-inset-top, 0px));
      padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px));
      padding-left: max(16px, env(safe-area-inset-left, 0px));
      padding-right: max(16px, env(safe-area-inset-right, 0px));
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
    }

    /* Hero section centering inside scroll container */
    .hero .book-page-scroll {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100%;
      text-align: center;
    }

    /* Dynamic Page-Curl Fold Shadow (Darkens near the spine as page lifts) */
    .page-curl-shadow {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 50;
      opacity: 0;
      background: linear-gradient(
        to right,
        rgba(0, 0, 0, 0.96) 0%,
        rgba(22, 5, 32, 0.85) 12%,
        rgba(0, 0, 0, 0.35) 35%,
        rgba(244, 213, 224, 0.12) 65%,
        rgba(0, 0, 0, 0.8) 100%
      );
      box-shadow: inset 35px 0 70px rgba(0, 0, 0, 0.95);
    }

    /* Shadow Cast onto Underneath Page (Dissolves as top page lifts away) */
    .page-under-shadow {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 45;
      opacity: 0;
      background: linear-gradient(to right, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.35) 30%, transparent 60%);
    }

    /* 3D Page Turn Animation Classes */
    .book-page.turning-next-out {
      display: block !important;
      visibility: visible !important;
      z-index: 25 !important;
      animation: physicalPageFlipNext 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
      pointer-events: none !important;
      opacity: 1 !important;
    }

    .book-page.turning-next-out .page-curl-shadow {
      animation: foldShadowIntensify 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }

    .book-page.page-under .page-under-shadow {
      animation: underShadowDissolve 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }

    .book-page.turning-prev-in {
      display: block !important;
      visibility: visible !important;
      z-index: 25 !important;
      animation: physicalPageFlipPrev 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
      pointer-events: none !important;
      opacity: 1 !important;
    }

    .book-page.turning-prev-in .page-curl-shadow {
      animation: foldShadowDissolve 0.85s cubic-bezier(0.25, 1, 0.5, 1) forwards !important;
    }

    .book-page.turning-prev-out {
      display: block !important;
      visibility: visible !important;
      z-index: 5 !important;
      transform: rotateY(0deg) translateZ(-4px) !important;
      pointer-events: none !important;
      opacity: 1 !important;
    }

    /* Keyframes for Pure Physical 3D Flip (Visible Foreshortening & No Opacity Fade) */
    @keyframes physicalPageFlipNext {
      0% {
        transform: rotateY(0deg);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
      }
      20% {
        transform: rotateY(-22deg) skewY(-1.5deg);
        box-shadow: -15px 0 35px rgba(0, 0, 0, 0.7), 0 20px 40px rgba(0, 0, 0, 0.5);
      }
      50% {
        transform: rotateY(-62deg) skewY(-3.2deg);
        box-shadow: -38px 0 70px rgba(0, 0, 0, 0.88), 0 30px 60px rgba(0, 0, 0, 0.65);
      }
      80% {
        transform: rotateY(-105deg) skewY(-2deg);
        box-shadow: -50px 0 90px rgba(0, 0, 0, 0.95);
      }
      100% {
        transform: rotateY(-140deg) skewY(0deg);
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.4);
      }
    }

    @keyframes foldShadowIntensify {
      0% {
        opacity: 0;
      }
      20% {
        opacity: 0.5;
      }
      50% {
        opacity: 0.92;
      }
      80% {
        opacity: 1;
      }
      100% {
        opacity: 0.88;
      }
    }

    @keyframes underShadowDissolve {
      0% {
        opacity: 0.85;
      }
      40% {
        opacity: 0.5;
      }
      100% {
        opacity: 0;
      }
    }

    @keyframes physicalPageFlipPrev {
      0% {
        transform: rotateY(-140deg) skewY(0deg);
        box-shadow: -20px 0 40px rgba(0, 0, 0, 0.4);
      }
      25% {
        transform: rotateY(-105deg) skewY(-2deg);
        box-shadow: -50px 0 90px rgba(0, 0, 0, 0.95);
      }
      55% {
        transform: rotateY(-62deg) skewY(-3.2deg);
        box-shadow: -38px 0 70px rgba(0, 0, 0, 0.88);
      }
      80% {
        transform: rotateY(-22deg) skewY(-1.5deg);
        box-shadow: -15px 0 35px rgba(0, 0, 0, 0.7);
      }
      100% {
        transform: rotateY(0deg) skewY(0deg);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
      }
    }

    @keyframes foldShadowDissolve {
      0% {
        opacity: 0.95;
      }
      45% {
        opacity: 0.8;
      }
      75% {
        opacity: 0.35;
      }
      100% {
        opacity: 0;
      }
    }

    """

content = content[:css_start] + new_css + content[css_end:]
print("Replaced CSS block successfully!")

# 2. Wrap the 8 sections with .book-page-scroll, .page-curl-shadow, and .page-under-shadow
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
    if not match:
        print(f"ERROR: Could not find section {sid}")
        continue
    
    open_tag = match.group(1)
    inner_html = match.group(2)
    close_tag = match.group(3)
    
    # If already wrapped, skip wrapping
    if 'class="book-page-scroll"' in inner_html:
        print(f"{sid} is already wrapped.")
        continue
        
    wrapped_inner = f"""\n      <div class="book-page-scroll">{inner_html}      </div>\n      <div class="page-curl-shadow"></div>\n      <div class="page-under-shadow"></div>\n    """
    new_section_block = open_tag + wrapped_inner + close_tag
    content = content[:match.start()] + new_section_block + content[match.end():]
    print(f"Wrapped {sid} successfully!")

# 3. Update JavaScript goToChapter to 850ms and scroll container resetting
old_js_goto = """    function goToChapter(targetIndex, explicitDirection) {
      if (isFlipping || targetIndex === currentChapterIndex || targetIndex < 0 || targetIndex >= CHAPTERS.length) {
        return;
      }

      const direction = explicitDirection || (targetIndex > currentChapterIndex ? "next" : "prev");
      isFlipping = true;

      const curPage = document.getElementById(CHAPTERS[currentChapterIndex].id);
      const targetPage = document.getElementById(CHAPTERS[targetIndex].id);

      if (!curPage || !targetPage) {
        isFlipping = false;
        return;
      }

      const durationMs = 750;

      if (direction === "next") {
        // Forward 3D page turn: curPage lifts and curls left; targetPage revealed underneath
        targetPage.classList.remove("page-active", "turning-next-out", "turning-next-in", "turning-prev-in", "turning-prev-out");
        targetPage.classList.add("page-under", "turning-next-in");
        targetPage.style.display = targetPage.classList.contains("hero") ? "flex" : "block";
        targetPage.scrollTop = 0;

        curPage.classList.remove("page-under", "turning-next-in", "turning-prev-in", "turning-prev-out");
        curPage.classList.add("turning-next-out");
        curPage.style.display = curPage.classList.contains("hero") ? "flex" : "block";

        setTimeout(() => {
          curPage.classList.remove("page-active", "turning-next-out");
          curPage.style.display = "none";

          targetPage.classList.remove("page-under", "turning-next-in");
          targetPage.classList.add("page-active");
          targetPage.style.display = targetPage.classList.contains("hero") ? "flex" : "block";

          currentChapterIndex = targetIndex;
          updateNavUI(targetIndex);
          isFlipping = false;

          if (targetIndex === 7) {
            triggerTypingEffect();
          }
        }, durationMs);

      } else {
        // Backward 3D page turn: targetPage flips from left fold over curPage
        curPage.classList.remove("page-active", "turning-next-out", "turning-next-in", "turning-prev-in");
        curPage.classList.add("page-under", "turning-prev-out");
        curPage.style.display = curPage.classList.contains("hero") ? "flex" : "block";

        targetPage.classList.remove("page-under", "turning-next-out", "turning-next-in", "turning-prev-out");
        targetPage.classList.add("turning-prev-in");
        targetPage.style.display = targetPage.classList.contains("hero") ? "flex" : "block";
        targetPage.scrollTop = 0;

        setTimeout(() => {
          curPage.classList.remove("page-under", "turning-prev-out");
          curPage.style.display = "none";

          targetPage.classList.remove("turning-prev-in");
          targetPage.classList.add("page-active");
          targetPage.style.display = targetPage.classList.contains("hero") ? "flex" : "block";

          currentChapterIndex = targetIndex;
          updateNavUI(targetIndex);
          isFlipping = false;

          if (targetIndex === 7) {
            triggerTypingEffect();
          }
        }, durationMs);
      }
    }"""

new_js_goto = """    function goToChapter(targetIndex, explicitDirection) {
      if (isFlipping || targetIndex === currentChapterIndex || targetIndex < 0 || targetIndex >= CHAPTERS.length) {
        return;
      }

      const direction = explicitDirection || (targetIndex > currentChapterIndex ? "next" : "prev");
      isFlipping = true;

      const curPage = document.getElementById(CHAPTERS[currentChapterIndex].id);
      const targetPage = document.getElementById(CHAPTERS[targetIndex].id);

      if (!curPage || !targetPage) {
        isFlipping = false;
        return;
      }

      const durationMs = 850;

      if (direction === "next") {
        // Target page is positioned underneath at rotateY(0deg) translateZ(-4px)
        targetPage.classList.remove("page-active", "turning-next-out", "turning-prev-in", "turning-prev-out");
        targetPage.classList.add("page-under");
        targetPage.style.display = "block";
        const targetScroll = targetPage.querySelector(".book-page-scroll");
        if (targetScroll) targetScroll.scrollTop = 0;

        // Current page on top rotates from rotateY(0deg) to rotateY(-140deg)
        curPage.classList.remove("page-under", "turning-prev-in", "turning-prev-out");
        curPage.classList.add("turning-next-out");
        curPage.style.display = "block";

        setTimeout(() => {
          curPage.classList.remove("page-active", "turning-next-out");
          curPage.style.display = "none";

          targetPage.classList.remove("page-under");
          targetPage.classList.add("page-active");
          targetPage.style.display = "block";

          currentChapterIndex = targetIndex;
          updateNavUI(targetIndex);
          isFlipping = false;

          if (targetIndex === 7) {
            triggerTypingEffect();
          }
        }, durationMs);

      } else {
        // Current page sits underneath
        curPage.classList.remove("page-active", "turning-next-out", "turning-prev-in");
        curPage.classList.add("turning-prev-out");
        curPage.style.display = "block";

        // Target page returns from left fold: rotates from rotateY(-140deg) to rotateY(0deg)
        targetPage.classList.remove("page-under", "turning-next-out", "turning-prev-out");
        targetPage.classList.add("turning-prev-in");
        targetPage.style.display = "block";
        const targetScroll = targetPage.querySelector(".book-page-scroll");
        if (targetScroll) targetScroll.scrollTop = 0;

        setTimeout(() => {
          curPage.classList.remove("turning-prev-out");
          curPage.style.display = "none";

          targetPage.classList.remove("turning-prev-in");
          targetPage.classList.add("page-active");
          targetPage.style.display = "block";

          currentChapterIndex = targetIndex;
          updateNavUI(targetIndex);
          isFlipping = false;

          if (targetIndex === 7) {
            triggerTypingEffect();
          }
        }, durationMs);
      }
    }"""

if old_js_goto in content:
    content = content.replace(old_js_goto, new_js_goto)
    print("Updated goToChapter JavaScript successfully!")
else:
    print("Warning: old_js_goto not found exactly.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated index.html successfully!")
