import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Scroll Progress Bar CSS
old_progress_css = """    /* ---------- Scroll Progress Bar ---------- */
    #scrollProgressBar {
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 3px;
      background: linear-gradient(90deg, var(--cosmic-amethyst), var(--celestial-orchid), var(--starlight-blush));
      box-shadow: 0 0 10px var(--celestial-orchid);
      z-index: 9999;
      transition: width 0.1s linear;
      transform: translateZ(0);
    }"""

new_progress_css = """    /* ---------- Chapter Progress Bar (Repurposed from Scroll Progress Bar) ---------- */
    #chapterProgressBar,
    #scrollProgressBar {
      position: fixed;
      top: 0;
      left: 0;
      width: 12.5%;
      height: 3px;
      background: linear-gradient(90deg, var(--cosmic-amethyst), var(--celestial-orchid), var(--starlight-blush));
      box-shadow: 0 0 10px var(--celestial-orchid);
      z-index: 9999;
      transition: width 0.5s cubic-bezier(0.25, 1, 0.5, 1);
      transform: translateZ(0);
      pointer-events: none;
    }"""

if old_progress_css in content:
    content = content.replace(old_progress_css, new_progress_css)
    print("Updated progress bar CSS successfully!")
else:
    print("Warning: old_progress_css not found exactly.")

# 2. Update .site-main and section CSS
old_site_main_css = """    /* ==========================================================================
     MAIN SITE SECTIONS (UNLOCKED)
     ========================================================================== */
    .site-main {
      position: relative;
      z-index: 3;
      opacity: 0;
      transition: opacity 1.2s ease 0.3s;
    }

    .site-main.revealed {
      opacity: 1;
    }

    section {
      padding: 110px 0;
      position: relative;
    }

    @media (max-width: 768px) {
      section {
        padding: 75px 0;
      }
    }"""

new_site_main_css = """    /* ==========================================================================
     BOOK CONTAINER & 3D PAGE-TURN EXPERIENCE
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
      perspective: 2400px;
      -webkit-perspective: 2400px;
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      pointer-events: none;
    }

    .site-main.revealed {
      opacity: 1;
      pointer-events: auto;
    }

    /* Individual Chapter Book Pages */
    .book-page {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      overflow-y: auto;
      overflow-x: hidden;
      -webkit-overflow-scrolling: touch;
      padding-top: calc(28px + env(safe-area-inset-top, 0px));
      padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px));
      padding-left: max(16px, env(safe-area-inset-left, 0px));
      padding-right: max(16px, env(safe-area-inset-right, 0px));
      transform-origin: left center;
      -webkit-transform-origin: left center;
      transform-style: preserve-3d;
      -webkit-transform-style: preserve-3d;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      display: none;
      visibility: hidden;
      pointer-events: none;
      will-change: transform, opacity;
    }

    /* Page-curling shadow overlay pseudo-element */
    .book-page::after {
      content: '';
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 99;
      opacity: 0;
      background: linear-gradient(to right,
        rgba(0, 0, 0, 0.85) 0%,
        rgba(26, 7, 40, 0.5) 18%,
        rgba(244, 213, 224, 0.08) 55%,
        rgba(0, 0, 0, 0.6) 100%
      );
      transition: opacity 0.75s cubic-bezier(0.25, 1, 0.5, 1);
      will-change: opacity;
    }

    /* Active Page */
    .book-page.page-active {
      display: block;
      visibility: visible;
      pointer-events: auto;
      z-index: 10;
      transform: rotateY(0deg) translateZ(0);
      opacity: 1;
    }

    /* Page sitting underneath during flip */
    .book-page.page-under {
      display: block;
      visibility: visible;
      pointer-events: none;
      z-index: 5;
    }

    /* Special flex layout for Hero */
    .hero.book-page {
      min-height: 100%;
      box-sizing: border-box;
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .hero.book-page.page-active,
    .hero.book-page.page-under,
    .hero.book-page.turning-next-out,
    .hero.book-page.turning-next-in,
    .hero.book-page.turning-prev-in,
    .hero.book-page.turning-prev-out {
      display: flex !important;
    }

    /* 3D Page Turn Animation Classes */
    .book-page.turning-next-out {
      display: block !important;
      visibility: visible !important;
      z-index: 15 !important;
      animation: bookFlipNextOut 0.75s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      pointer-events: none;
    }

    .book-page.turning-next-out::after {
      opacity: 1;
    }

    .book-page.turning-next-in {
      display: block !important;
      visibility: visible !important;
      z-index: 6 !important;
      animation: bookRevealUnder 0.75s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      pointer-events: none;
    }

    .book-page.turning-prev-in {
      display: block !important;
      visibility: visible !important;
      z-index: 15 !important;
      animation: bookFlipPrevIn 0.75s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      pointer-events: none;
    }

    .book-page.turning-prev-in::after {
      animation: bookShadowFadeOut 0.75s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }

    .book-page.turning-prev-out {
      display: block !important;
      visibility: visible !important;
      z-index: 6 !important;
      animation: bookCoverUnder 0.75s cubic-bezier(0.25, 1, 0.5, 1) forwards;
      pointer-events: none;
    }

    /* Keyframes */
    @keyframes bookFlipNextOut {
      0% {
        transform: rotateY(0deg) translateZ(0);
        box-shadow: 0 0 0 rgba(0, 0, 0, 0);
      }
      35% {
        transform: rotateY(-35deg) translateZ(40px) skewY(-2deg);
        box-shadow: -20px 0 45px rgba(0, 0, 0, 0.6);
      }
      70% {
        transform: rotateY(-80deg) translateZ(50px) skewY(-3deg);
        box-shadow: -35px 0 65px rgba(0, 0, 0, 0.75);
      }
      100% {
        transform: rotateY(-125deg) translateZ(10px) skewY(0deg);
        box-shadow: -10px 0 25px rgba(0, 0, 0, 0.2);
        opacity: 0;
      }
    }

    @keyframes bookRevealUnder {
      0% {
        transform: scale(0.96) translateZ(-40px);
        filter: brightness(0.72);
        opacity: 0.85;
      }
      100% {
        transform: scale(1) translateZ(0);
        filter: brightness(1);
        opacity: 1;
      }
    }

    @keyframes bookFlipPrevIn {
      0% {
        transform: rotateY(-125deg) translateZ(10px) skewY(0deg);
        box-shadow: -10px 0 25px rgba(0, 0, 0, 0.2);
        opacity: 0;
      }
      30% {
        transform: rotateY(-80deg) translateZ(50px) skewY(-3deg);
        box-shadow: -35px 0 65px rgba(0, 0, 0, 0.75);
        opacity: 1;
      }
      65% {
        transform: rotateY(-35deg) translateZ(40px) skewY(-2deg);
        box-shadow: -20px 0 45px rgba(0, 0, 0, 0.6);
      }
      100% {
        transform: rotateY(0deg) translateZ(0);
        box-shadow: 0 0 0 rgba(0, 0, 0, 0);
        opacity: 1;
      }
    }

    @keyframes bookCoverUnder {
      0% {
        transform: scale(1) translateZ(0);
        filter: brightness(1);
        opacity: 1;
      }
      100% {
        transform: scale(0.96) translateZ(-40px);
        filter: brightness(0.72);
        opacity: 0.85;
      }
    }

    @keyframes bookShadowFadeOut {
      0% { opacity: 1; }
      100% { opacity: 0; }
    }

    /* Section padding reset within book pages */
    section.book-page {
      padding: calc(30px + env(safe-area-inset-top, 0px)) 0 calc(96px + env(safe-area-inset-bottom, 0px));
    }

    @media (max-width: 768px) {
      section.book-page {
        padding: calc(20px + env(safe-area-inset-top, 0px)) 0 calc(90px + env(safe-area-inset-bottom, 0px));
      }
    }

    /* Bottom Navigation Bar */
    .book-nav-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 999;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 10px 24px calc(12px + env(safe-area-inset-bottom, 0px));
      background: rgba(10, 4, 18, 0.84);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid rgba(232, 180, 208, 0.18);
      box-shadow: 0 -10px 35px rgba(0, 0, 0, 0.5);
      opacity: 0;
      transform: translateY(100%);
      transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.2, 0.9, 0.3, 1);
      pointer-events: none;
    }

    .book-nav-bar.visible {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }

    .book-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      border-radius: 24px;
      background: rgba(114, 52, 119, 0.3);
      border: 1px solid rgba(232, 180, 208, 0.3);
      color: var(--starlight-blush);
      font-family: var(--font-body);
      font-size: 0.92rem;
      font-weight: 500;
      letter-spacing: 0.04em;
      transition: all 0.25s ease;
      user-select: none;
      -webkit-user-select: none;
      cursor: pointer;
    }

    .book-nav-btn:hover {
      background: rgba(199, 116, 178, 0.45);
      border-color: var(--starlight-blush);
      box-shadow: 0 0 16px var(--celestial-orchid-glow);
      transform: translateY(-2px);
    }

    .book-nav-btn:active {
      transform: translateY(0) scale(0.96);
    }

    .book-nav-prev.hidden-btn {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .book-nav-center {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      text-align: center;
      flex: 1;
      min-width: 0;
    }

    .book-nav-label {
      font-family: var(--font-heading);
      font-size: 0.96rem;
      color: var(--starlight-blush);
      letter-spacing: 0.03em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      text-shadow: 0 0 10px rgba(199, 116, 178, 0.4);
    }

    .book-dots {
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }

    .book-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: rgba(232, 180, 208, 0.28);
      border: 1px solid rgba(232, 180, 208, 0.45);
      padding: 0;
      margin: 0;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
      position: relative;
    }

    .book-dot::before {
      content: '';
      position: absolute;
      inset: -8px; /* Expand touch target for mobile */
    }

    .book-dot:hover {
      background: rgba(232, 180, 208, 0.65);
      transform: scale(1.3);
    }

    .book-dot.active {
      width: 26px;
      border-radius: 12px;
      background: linear-gradient(90deg, var(--cosmic-amethyst), var(--celestial-orchid), var(--gold-starlight));
      border-color: var(--starlight-blush);
      box-shadow: 0 0 12px var(--celestial-orchid-glow);
    }

    @media (max-width: 600px) {
      .book-nav-bar {
        padding: 8px 12px calc(10px + env(safe-area-inset-bottom, 0px));
        gap: 8px;
      }
      .book-nav-btn {
        padding: 7px 12px;
        font-size: 0.85rem;
      }
      .book-nav-label {
        font-size: 0.82rem;
      }
      .book-dots {
        gap: 6px;
      }
      .book-dot {
        width: 8px;
        height: 8px;
      }
      .book-dot.active {
        width: 18px;
      }
    }"""

if old_site_main_css in content:
    content = content.replace(old_site_main_css, new_site_main_css)
    print("Updated site-main CSS successfully!")
else:
    print("Warning: old_site_main_css not found exactly.")

# 3. Add book-page class to sections in DOM
section_replaces = [
    ('<header class="hero" id="heroSection">', '<header class="hero book-page page-active" id="heroSection">'),
    ('<section id="chapterTimeline">', '<section class="book-page" id="chapterTimeline">'),
    ('<section id="chapterGallery">', '<section class="book-page" id="chapterGallery">'),
    ('<section id="chapterEnvelopes">', '<section class="book-page" id="chapterEnvelopes">'),
    ('<section id="chapterLetter">', '<section class="book-page" id="chapterLetter">'),
    ('<section id="chapterQuiz">', '<section class="book-page" id="chapterQuiz">'),
    ('<section id="chapterVerses">', '<section class="book-page" id="chapterVerses">'),
    ('<section class="closing-section" id="chapterClosing">', '<section class="book-page closing-section" id="chapterClosing">'),
]

for old_sec, new_sec in section_replaces:
    if old_sec in content:
        content = content.replace(old_sec, new_sec, 1)
        print(f"Replaced section tag: {old_sec[:30]}...")
    else:
        print(f"Warning: {old_sec} not found.")

# 4. Move footer inside chapterClosing and add bookNavBar after </main>
old_closing_and_footer = """        <!-- Reserved slot for Voice Message -->
          <div class="voice-note-wrap" id="voiceNoteWrap">
            <audio controls style="width: 100%;">
              <source src="voice_message.mp3" type="audio/mpeg">
              Your browser does not support audio playback.
            </audio>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer>
      <div class="container">
        Made with endless love & sincere duas by Umar for Hayathi • September 13
      </div>
    </footer>

  </main>"""

new_closing_and_footer = """        <!-- Reserved slot for Voice Message -->
          <div class="voice-note-wrap" id="voiceNoteWrap">
            <audio controls style="width: 100%;">
              <source src="voice_message.mp3" type="audio/mpeg">
              Your browser does not support audio playback.
            </audio>
          </div>
        </div>

        <!-- FOOTER (Inside Chapter 8) -->
        <footer style="margin-top: 50px; text-align: center; color: var(--text-muted); font-size: 0.9rem; padding: 20px 0;">
          Made with endless love & sincere duas by Umar for Hayathi • September 13
        </footer>

      </div>
    </section>

  </main>

  <!-- ==========================================================================
     BOOK CHAPTER BOTTOM NAVIGATION BAR
     ========================================================================== -->
  <nav class="book-nav-bar" id="bookNavBar" aria-label="Book Chapter Navigation">
    <button type="button" class="book-nav-btn book-nav-prev hidden-btn clickable" id="btnBookPrev" aria-label="Previous Chapter">
      <span>←</span> <span>Back</span>
    </button>
    <div class="book-nav-center">
      <div class="book-nav-label" id="bookNavLabel">Chapter 1 of 8 • Happy Birthday</div>
      <div class="book-dots" id="bookDotsContainer" role="tablist" aria-label="Chapters"></div>
    </div>
    <button type="button" class="book-nav-btn book-nav-next clickable" id="btnBookNext" aria-label="Next Chapter">
      <span class="nav-btn-text">Next</span> <span>→</span>
    </button>
  </nav>"""

if old_closing_and_footer in content:
    content = content.replace(old_closing_and_footer, new_closing_and_footer)
    print("Replaced closing section, footer, and added bookNavBar!")
else:
    print("Warning: old_closing_and_footer not found exactly.")

# 5. In JS: Update proposal unlock to initialize book experience
old_unlock_js = """        // Unlock after 1.5s
        setTimeout(() => {
          const gate = document.getElementById("gateOverlay");
          const main = document.getElementById("mainExperience");
          gate.classList.add("hidden");
          gate.style.display = "none";
          main.classList.add("revealed");
          btnNo.style.display = "none";
          initTypingEffect();
        }, 1400);"""

new_unlock_js = """        // Unlock after 1.5s
        setTimeout(() => {
          const gate = document.getElementById("gateOverlay");
          const main = document.getElementById("mainExperience");
          gate.classList.add("hidden");
          gate.style.display = "none";
          main.classList.add("revealed");
          btnNo.style.display = "none";
          initBookExperience();
        }, 1400);"""

if old_unlock_js in content:
    content = content.replace(old_unlock_js, new_unlock_js)
    print("Updated proposal unlock JS!")
else:
    print("Warning: old_unlock_js not found.")

# 6. Update typing effect logic and append Book Chapter Navigation Engine
old_typing_code = """    let typingDone = false;
    function initTypingEffect() {
      if (typingDone) return;
      const text = "Insha allah life sikiram marum, namalum senthu happy yaa irrupom...";
      const el = document.getElementById("typingText");
      if (!el) return;

      // Trigger typing when user scrolls near closing
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !typingDone) {
            typingDone = true;
            let idx = 0;
            const timer = setInterval(() => {
              if (idx < text.length) {
                el.textContent += text.charAt(idx);
                idx++;
              } else {
                clearInterval(timer);
              }
            }, 60);
          }
        });
      }, { threshold: 0.3 });

      const closingSection = document.getElementById("chapterClosing");
      if (closingSection) observer.observe(closingSection);
    }"""

new_typing_and_book_engine = """    let typingDone = false;
    function triggerTypingEffect() {
      if (typingDone) return;
      const text = "Insha allah life sikiram marum, namalum senthu happy yaa irrupom...";
      const el = document.getElementById("typingText");
      if (!el) return;

      typingDone = true;
      el.textContent = "";
      let idx = 0;
      const timer = setInterval(() => {
        if (idx < text.length) {
          el.textContent += text.charAt(idx);
          idx++;
        } else {
          clearInterval(timer);
        }
      }, 60);
    }

    function initTypingEffect() {
      // Maintained for backward compatibility; actual trigger happens on Chapter 8 active
      const closingSection = document.getElementById("chapterClosing");
      if (closingSection && closingSection.classList.contains("page-active")) {
        triggerTypingEffect();
      }
    }

    // ==========================================================================
    // CHAPTER-BY-CHAPTER BOOK NAVIGATION & 3D PAGE-TURN ENGINE
    // ==========================================================================
    const CHAPTERS = [
      { id: "heroSection", num: 1, title: "Happy Birthday", subtitle: "Introduction" },
      { id: "chapterTimeline", num: 2, title: "Our Story", subtitle: "Timeline" },
      { id: "chapterGallery", num: 3, title: "A Few Frames of Us", subtitle: "Photo Memories" },
      { id: "chapterEnvelopes", num: 4, title: "Open When You Want to Smile", subtitle: "Love Notes" },
      { id: "chapterLetter", num: 5, title: "A Letter For Your Birthday", subtitle: "Sealed Letter" },
      { id: "chapterQuiz", num: 6, title: "How Well Do You Know Us?", subtitle: "Our Quiz" },
      { id: "chapterVerses", num: 7, title: "A Small Dua & Reflection", subtitle: "Sacred Dua" },
      { id: "chapterClosing", num: 8, title: "Forever Yours", subtitle: "Closing & Secret" }
    ];

    let currentChapterIndex = 0;
    let isFlipping = false;
    let bookInitialized = false;

    function initBookExperience() {
      if (bookInitialized) return;
      bookInitialized = true;

      const navBar = document.getElementById("bookNavBar");
      const dotsContainer = document.getElementById("bookDotsContainer");

      // Generate Interactive Chapter Dots
      if (dotsContainer) {
        dotsContainer.innerHTML = "";
        CHAPTERS.forEach((ch, idx) => {
          const dot = document.createElement("button");
          dot.type = "button";
          dot.className = "book-dot clickable" + (idx === 0 ? " active" : "");
          dot.setAttribute("data-index", idx);
          dot.setAttribute("aria-label", `Jump to Chapter ${ch.num}: ${ch.title}`);
          dot.setAttribute("title", `Chapter ${ch.num}: ${ch.title}`);
          dot.addEventListener("click", () => {
            goToChapter(idx);
          });
          dotsContainer.appendChild(dot);
        });
      }

      // Attach Previous / Next Button Handlers
      const btnPrev = document.getElementById("btnBookPrev");
      const btnNext = document.getElementById("btnBookNext");

      if (btnPrev) {
        btnPrev.addEventListener("click", () => {
          goToPrevChapter();
        });
      }

      if (btnNext) {
        btnNext.addEventListener("click", () => {
          goToNextChapter();
        });
      }

      // Set Initial Active Page (Chapter 1)
      CHAPTERS.forEach((ch, idx) => {
        const p = document.getElementById(ch.id);
        if (p) {
          if (idx === 0) {
            p.classList.add("page-active");
            p.style.display = p.classList.contains("hero") ? "flex" : "block";
          } else {
            p.classList.remove("page-active", "page-under", "turning-next-out", "turning-next-in", "turning-prev-in", "turning-prev-out");
            p.style.display = "none";
          }
        }
      });

      updateNavUI(0);

      if (navBar) {
        navBar.classList.add("visible");
      }

      // Allow clicking the "Scroll into our story" prompt on Hero to turn page
      const heroScrollPrompt = document.querySelector(".hero-scroll");
      if (heroScrollPrompt) {
        heroScrollPrompt.classList.add("clickable");
        heroScrollPrompt.style.cursor = "pointer";
        const promptSpan = heroScrollPrompt.querySelector("span");
        if (promptSpan) promptSpan.textContent = "Turn page into our story →";
        heroScrollPrompt.addEventListener("click", () => {
          goToNextChapter();
        });
      }

      // Desktop Keyboard Navigation
      window.addEventListener("keydown", (e) => {
        const main = document.getElementById("mainExperience");
        if (!main || !main.classList.contains("revealed")) return;

        if (e.key === "ArrowRight") {
          goToNextChapter();
        } else if (e.key === "ArrowLeft") {
          goToPrevChapter();
        }
      });

      // Mobile Touch Swipe Navigation
      initSwipeGestures();
    }

    function goToNextChapter() {
      if (currentChapterIndex < CHAPTERS.length - 1) {
        goToChapter(currentChapterIndex + 1, "next");
      } else {
        // If at closing chapter, loop back to beginning
        goToChapter(0, "prev");
      }
    }

    function goToPrevChapter() {
      if (currentChapterIndex > 0) {
        goToChapter(currentChapterIndex - 1, "prev");
      }
    }

    function goToChapter(targetIndex, explicitDirection) {
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
    }

    function updateNavUI(index) {
      const ch = CHAPTERS[index];
      const label = document.getElementById("bookNavLabel");
      if (label) {
        label.textContent = `Chapter ${ch.num} of ${CHAPTERS.length} • ${ch.title}`;
      }

      // Update Chapter Dots
      const dots = document.querySelectorAll(".book-dot");
      dots.forEach((d, i) => {
        if (i === index) {
          d.classList.add("active");
        } else {
          d.classList.remove("active");
        }
      });

      // Update Previous Button visibility
      const btnPrev = document.getElementById("btnBookPrev");
      if (btnPrev) {
        if (index === 0) {
          btnPrev.classList.add("hidden-btn");
        } else {
          btnPrev.classList.remove("hidden-btn");
        }
      }

      // Update Next Button text
      const btnNext = document.getElementById("btnBookNext");
      if (btnNext) {
        const nextText = btnNext.querySelector(".nav-btn-text");
        if (index === CHAPTERS.length - 1) {
          if (nextText) nextText.textContent = "Start Again ↺";
        } else {
          if (nextText) nextText.textContent = "Next";
        }
      }

      // Update Top Progress Bar
      const progressBar = document.getElementById("chapterProgressBar") || document.getElementById("scrollProgressBar");
      if (progressBar) {
        const pct = ((index + 1) / CHAPTERS.length) * 100;
        progressBar.style.width = pct + "%";
      }
    }

    // Touch Swipe Gesture Listener (Mobile)
    function initSwipeGestures() {
      let touchStartX = 0;
      let touchStartY = 0;
      let touchStartTime = 0;

      const touchArea = document.getElementById("mainExperience") || document.body;

      touchArea.addEventListener("touchstart", (e) => {
        if (e.touches.length === 1) {
          touchStartX = e.touches[0].clientX;
          touchStartY = e.touches[0].clientY;
          touchStartTime = Date.now();
        }
      }, { passive: true });

      touchArea.addEventListener("touchend", (e) => {
        if (e.changedTouches.length === 1) {
          const deltaX = e.changedTouches[0].clientX - touchStartX;
          const deltaY = e.changedTouches[0].clientY - touchStartY;
          const deltaTime = Date.now() - touchStartTime;

          // Do not trigger swipe if user was interacting with form controls or audio
          const target = e.target;
          if (target && target.closest("input, button, audio, .wax-seal, .quiz-choice, .polaroid-action-btn")) {
            return;
          }

          // Horizontal swipe detection: distance >= 50px, predominantly horizontal, within 800ms
          if (Math.abs(deltaX) >= 50 && Math.abs(deltaX) > 1.4 * Math.abs(deltaY) && deltaTime < 800) {
            if (deltaX < 0) {
              // Swiped Left -> Next Chapter
              goToNextChapter();
            } else {
              // Swiped Right -> Previous Chapter
              goToPrevChapter();
            }
          }
        }
      }, { passive: true });
    }

    // Expose functions globally for testing and programmatic navigation
    window.initBookExperience = initBookExperience;
    window.goToChapter = goToChapter;
    window.goToNextChapter = goToNextChapter;
    window.goToPrevChapter = goToPrevChapter;"""

if old_typing_code in content:
    content = content.replace(old_typing_code, new_typing_and_book_engine)
    print("Replaced typing effect code and appended Book Navigation Engine!")
else:
    print("Warning: old_typing_code not found.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully written to index.html!")
