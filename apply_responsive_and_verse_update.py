import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================================
# 1. VIEWPORT META TAG UPDATE (iOS Safari Notch / Safe Area Inset Support)
# ==============================================================================
content = content.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
)

# ==============================================================================
# 2. CSS RESPONSIVE AUDIT & HOVER-GUARD UPDATES
# ==============================================================================

# Ensure html and body strictly prevent horizontal scrolling & handle iOS safe areas
old_body_css = """  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }

  body {
    background-color: var(--space-void);
    color: var(--starlight-white);
    font-family: var(--font-body);
    font-weight: 300;
    line-height: 1.68;
    overflow-x: hidden;
    position: relative;
    cursor: default;
  }"""

new_body_css = """  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
  html { 
    scroll-behavior: smooth;
    overflow-x: hidden;
    width: 100%;
    max-width: 100vw;
  }

  body {
    background-color: var(--space-void);
    color: var(--starlight-white);
    font-family: var(--font-body);
    font-weight: 300;
    line-height: 1.68;
    overflow-x: hidden;
    width: 100%;
    max-width: 100vw;
    position: relative;
    cursor: default;
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
  }"""

content = content.replace(old_body_css, new_body_css)

# Update scroll progress bar for iOS safe-area-inset
content = content.replace(
    """  #scrollProgressBar {
    position: fixed;
    top: 0; left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, var(--cosmic-amethyst), var(--celestial-orchid), var(--starlight-blush));
    box-shadow: 0 0 10px var(--celestial-orchid);
    z-index: 9999;
    transition: width 0.1s linear;
  }""",
    """  #scrollProgressBar {
    position: fixed;
    top: 0; left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, var(--cosmic-amethyst), var(--celestial-orchid), var(--starlight-blush));
    box-shadow: 0 0 10px var(--celestial-orchid);
    z-index: 9999;
    transition: width 0.1s linear;
    transform: translateZ(0);
  }"""
)

# Update .gate for 100svh/dvh & scrollable fallback on small or landscape mobile viewports
old_gate_css = """  .gate {
    position: fixed; inset: 0;
    z-index: 500;
    background: radial-gradient(circle at center, #350c44 0%, #210535 55%, #0d0216 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.8s ease;
  }"""

new_gate_css = """  .gate {
    position: fixed; inset: 0;
    width: 100%; width: 100vw;
    height: 100vh; height: 100svh; height: 100dvh;
    z-index: 500;
    background: radial-gradient(circle at center, #350c44 0%, #210535 55%, #0d0216 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: calc(16px + env(safe-area-inset-top, 0px)) 16px calc(16px + env(safe-area-inset-bottom, 0px));
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.8s ease;
  }"""

content = content.replace(old_gate_css, new_gate_css)

# Update .hero for 100svh/dvh & responsive padding
old_hero_css = """  .hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    padding: 80px 24px 60px;
    perspective: 1000px;
  }"""

new_hero_css = """  .hero {
    min-height: 100vh;
    min-height: 100svh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    padding: calc(90px + env(safe-area-inset-top, 0px)) 20px 60px;
    perspective: 1000px;
  }"""

content = content.replace(old_hero_css, new_hero_css)

# Update .gate-dialog and date-input responsive sizing
old_gate_dialog_css = """  .gate-dialog {
    position: relative;
    max-width: 480px;
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    box-shadow: var(--glass-glow), 0 20px 60px rgba(0, 0, 0, 0.6);
    border-radius: 20px;
    padding: 44px 36px;
    text-align: center;
    opacity: 0;
    transform: translateY(24px) scale(0.96);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    display: none;
    z-index: 20;
  }"""

new_gate_dialog_css = """  .gate-dialog {
    position: relative;
    max-width: 480px;
    width: 100%;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    box-shadow: var(--glass-glow), 0 20px 60px rgba(0, 0, 0, 0.6);
    border-radius: 20px;
    padding: 40px 32px;
    text-align: center;
    opacity: 0;
    transform: translateY(24px) scale(0.96);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    display: none;
    z-index: 20;
  }
  @media (max-width: 480px) {
    .gate-dialog {
      padding: 30px 18px;
      border-radius: 16px;
    }
  }"""

content = content.replace(old_gate_dialog_css, new_gate_dialog_css)

# Update .date-input font size clamp
old_date_input_css = """  .date-input {
    width: 100%;
    background: rgba(18, 6, 28, 0.85);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 1.4rem;
    letter-spacing: 0.18em;
    text-align: center;
    color: var(--starlight-white);
    font-family: var(--font-body);
    font-weight: 500;
    outline: none;
    transition: all 0.3s ease;
  }"""

new_date_input_css = """  .date-input {
    width: 100%;
    background: rgba(18, 6, 28, 0.85);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 14px 12px;
    font-size: clamp(1.05rem, 4.5vw, 1.35rem);
    letter-spacing: clamp(0.06em, 1.5vw, 0.16em);
    text-align: center;
    color: var(--starlight-white);
    font-family: var(--font-body);
    font-weight: 500;
    outline: none;
    transition: all 0.3s ease;
  }"""

content = content.replace(old_date_input_css, new_date_input_css)

# Update touch target sizes for mobile buttons
old_btn_submit_css = """  .btn-submit {
    width: 100%;
    background: linear-gradient(135deg, var(--cosmic-amethyst), var(--celestial-orchid));
    color: var(--starlight-white);
    border: none;
    padding: 15px 28px;
    font-size: 1.05rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(114, 52, 119, 0.4);
  }"""

new_btn_submit_css = """  .btn-submit {
    width: 100%;
    min-height: 48px;
    background: linear-gradient(135deg, var(--cosmic-amethyst), var(--celestial-orchid));
    color: var(--starlight-white);
    border: none;
    padding: 14px 24px;
    font-size: 1.05rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 20px rgba(114, 52, 119, 0.4);
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .btn-submit:active {
    transform: scale(0.98);
  }"""

content = content.replace(old_btn_submit_css, new_btn_submit_css)

# Update proposal buttons for small screens
old_propose_css = """  .propose-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    margin-top: 32px;
    position: relative;
    min-height: 60px;
  }

  .btn-yes {
    background: linear-gradient(135deg, var(--cosmic-amethyst), var(--celestial-orchid));
    color: var(--starlight-white);
    border: none;
    padding: 14px 38px;
    font-size: 1.15rem;
    font-weight: 600;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 25px rgba(190, 111, 171, 0.5);
    transition: all 0.25s ease;
    position: relative;
    z-index: 50;
  }"""

new_propose_css = """  .propose-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin-top: 30px;
    position: relative;
    min-height: 60px;
  }
  @media (max-width: 480px) {
    .propose-buttons {
      gap: 14px;
    }
  }

  .btn-yes {
    min-height: 48px;
    background: linear-gradient(135deg, var(--cosmic-amethyst), var(--celestial-orchid));
    color: var(--starlight-white);
    border: none;
    padding: 13px 32px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 25px rgba(190, 111, 171, 0.5);
    transition: all 0.25s ease;
    position: relative;
    z-index: 50;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .btn-yes:active {
    transform: scale(0.96);
  }
  @media (max-width: 480px) {
    .btn-yes {
      padding: 12px 24px;
      font-size: 1rem;
    }
  }"""

content = content.replace(old_propose_css, new_propose_css)

# Update .no-spacer and .btn-no-dodger for small screens
old_no_css = """  .no-spacer {
    width: 120px;
    height: 50px;
    visibility: hidden;
    pointer-events: none;
  }

  /* Floating Dodging No Button */
  .btn-no-dodger {
    position: fixed;
    background: rgba(45, 13, 56, 0.75);
    color: var(--text-muted);
    border: 1px solid var(--glass-border);
    padding: 13px 34px;
    font-size: 1.05rem;
    font-weight: 400;
    border-radius: 30px;
    cursor: pointer;
    backdrop-filter: blur(8px);
    transition: left 0.25s cubic-bezier(0.18, 0.89, 0.32, 1.28), top 0.25s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    z-index: 45;
    user-select: none;
    white-space: nowrap;
  }"""

new_no_css = """  .no-spacer {
    width: 110px;
    height: 48px;
    visibility: hidden;
    pointer-events: none;
  }
  @media (max-width: 480px) {
    .no-spacer {
      width: 86px;
      height: 44px;
    }
  }

  /* Floating Dodging No Button */
  .btn-no-dodger {
    position: fixed;
    min-height: 44px;
    background: rgba(45, 13, 56, 0.88);
    color: var(--text-muted);
    border: 1px solid var(--glass-border);
    padding: 12px 28px;
    font-size: 1rem;
    font-weight: 400;
    border-radius: 30px;
    cursor: pointer;
    backdrop-filter: blur(8px);
    transition: left 0.25s cubic-bezier(0.18, 0.89, 0.32, 1.28), top 0.25s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    z-index: 45;
    user-select: none;
    white-space: nowrap;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  @media (max-width: 480px) {
    .btn-no-dodger {
      padding: 10px 20px;
      font-size: 0.95rem;
    }
  }"""

content = content.replace(old_no_css, new_no_css)

# Update envelope content max-height so mobile long text never clips
content = content.replace(
    """  .envelope-card.open .env-content {
    max-height: 320px;
    opacity: 1;
    margin-top: 20px;
    padding-top: 18px;
    border-color: var(--glass-border);
  }""",
    """  .envelope-card.open .env-content {
    max-height: 600px;
    opacity: 1;
    margin-top: 20px;
    padding-top: 18px;
    border-color: var(--glass-border);
  }"""
)

# Update secret panel max-height so mobile wrapped text never clips
content = content.replace(
    """  .secret-panel.revealed {
    max-height: 500px;
    opacity: 1;
    padding: 34px;
  }""",
    """  .secret-panel.revealed {
    max-height: 900px;
    opacity: 1;
    padding: 32px 24px;
  }
  @media (max-width: 480px) {
    .secret-panel.revealed {
      padding: 24px 16px;
    }
  }"""
)

# Guard all hover-only effects inside @media (hover: hover) and (pointer: fine)
old_hover_effects = """  .gift-card-wrapper:hover .gift-svg {
    transform: scale(1.03) translateY(-4px);
    filter: drop-shadow(0 20px 55px rgba(190, 111, 171, 0.6));
  }"""

# Let's add hover media query wrap for gift, cards, and buttons
# Also add responsive refinement for timeline on <= 480px
responsive_additions = """
  /* Responsive refinements for small screens (<= 480px) */
  @media (max-width: 480px) {
    .container {
      padding: 0 16px;
    }
    section {
      padding: 55px 0;
    }
    .section-head {
      margin-bottom: 35px;
    }
    .hero h1 {
      font-size: clamp(2.8rem, 13vw, 4.5rem);
    }
    .hero-bismillah {
      font-size: clamp(1.45rem, 5.5vw, 2.2rem);
      margin-bottom: 16px;
    }
    .hero-badge {
      padding: 6px 16px;
      font-size: 0.84rem;
      max-width: 95vw;
    }
    .hero-sub {
      font-size: 1rem;
    }
    /* Timeline compact mobile layout */
    .timeline::before {
      left: 15px !important;
    }
    .timeline-item {
      padding-left: 42px !important;
      padding-right: 6px !important;
      margin-bottom: 35px;
    }
    .timeline-node {
      left: 7px !important;
      width: 16px;
      height: 16px;
      top: 16px;
    }
    .timeline-card {
      padding: 18px 16px;
      border-radius: 14px;
    }
    .timeline-card h3 {
      font-size: 1.22rem;
    }
    .wax-letter-paper {
      padding: 28px 16px;
      border-radius: 16px;
    }
    .wax-seal {
      width: 72px;
      height: 72px;
    }
    .letter-body {
      font-size: 1.02rem;
      line-height: 1.8;
    }
    .quiz-card {
      padding: 22px 16px;
      border-radius: 16px;
    }
    .verse-card {
      padding: 28px 16px;
      border-radius: 18px;
    }
    .typing-box {
      font-size: 1.15rem;
      min-height: 75px;
    }
  }

  /* Hover transitions only active on pointer/mouse devices */
  @media (hover: hover) and (pointer: fine) {
    .gift-card-wrapper:hover .gift-svg {
      transform: scale(1.03) translateY(-4px);
      filter: drop-shadow(0 20px 55px rgba(190, 111, 171, 0.6));
    }
    .btn-submit:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(190, 111, 171, 0.6);
      background: linear-gradient(135deg, var(--cosmic-amethyst-light), var(--starlight-blush));
      color: var(--space-void);
    }
    .btn-yes:hover {
      transform: scale(1.06);
      box-shadow: 0 8px 35px rgba(246, 214, 229, 0.7);
      color: var(--space-void);
      background: linear-gradient(135deg, var(--starlight-blush), var(--celestial-orchid));
    }
    .timeline-card:hover {
      transform: translateY(-4px);
      border-color: var(--glass-border-strong);
      background: var(--glass-bg-hover);
      box-shadow: 0 12px 35px rgba(114, 52, 119, 0.45);
    }
    .photo-frame:hover {
      transform: translateY(-5px) scale(1.02);
      border-color: var(--glass-border-strong);
      box-shadow: 0 15px 40px rgba(190, 111, 171, 0.35);
    }
    .photo-frame:hover .frame-inner img {
      transform: scale(1.08);
    }
    .envelope-card:hover {
      transform: translateY(-5px);
      background: var(--glass-bg-hover);
      border-color: var(--glass-border-strong);
      box-shadow: 0 16px 45px rgba(114, 52, 119, 0.45);
    }
    .envelope-card:hover .env-icon {
      transform: scale(1.15) rotate(5deg);
    }
    .envelope-card:hover::before { opacity: 1; }
    .wax-seal:hover {
      transform: scale(1.08) rotate(5deg);
      box-shadow: 0 15px 40px rgba(226, 138, 181, 0.7);
    }
    .quiz-btn:hover:not(:disabled) {
      background: rgba(114, 52, 119, 0.35);
      border-color: var(--celestial-orchid);
      transform: translateX(4px);
    }
    .btn-verse:hover {
      background: var(--cosmic-amethyst);
      border-color: var(--celestial-orchid);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(190, 111, 171, 0.4);
    }
    .secret-trigger:hover {
      color: var(--starlight-blush);
      text-shadow: 0 0 10px var(--celestial-orchid);
    }
  }

  /* Active tactile feedback for mobile touch */
  .quiz-btn:active:not(:disabled),
  .btn-verse:active,
  .envelope-card:active,
  .wax-seal:active {
    transform: scale(0.97);
  }
"""

# Insert responsive additions right before </style>
content = content.replace("</style>", responsive_additions + "\n</style>")

# ==============================================================================
# 3. REQUIREMENT 2: QURAN VERSE HIDDEN BY DEFAULT
# ==============================================================================

# Update Quran Verse CSS: Add .verse-body-wrap collapsed by default
old_verse_css = """  /* ---------- CHAPTER 6: QURANIC VERSES GENERATOR ---------- */
  .verse-card {
    max-width: 720px;
    margin: 0 auto;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    border-radius: 22px;
    padding: 48px 40px;
    text-align: center;
    box-shadow: var(--glass-glow);
    position: relative;
  }
  .verse-arabic {
    font-family: var(--font-arabic);
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    color: var(--gold-starlight);
    line-height: 1.8;
    margin-bottom: 22px;
    direction: rtl;
    text-shadow: 0 0 20px var(--gold-glow);
  }
  .verse-translation {
    font-family: var(--font-heading);
    font-size: 1.15rem;
    font-style: italic;
    color: var(--starlight-blush);
    line-height: 1.8;
    margin-bottom: 16px;
  }
  .verse-reference {
    font-size: 0.92rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--celestial-orchid);
    font-weight: 500;
  }
  .btn-verse {
    margin-top: 28px;
    background: rgba(114, 52, 119, 0.35);
    border: 1px solid var(--glass-border);
    color: var(--starlight-white);
    padding: 12px 28px;
    border-radius: 30px;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }"""

new_verse_css = """  /* ---------- CHAPTER 6: QURANIC VERSES GENERATOR (COLLAPSED BY DEFAULT) ---------- */
  .verse-card {
    max-width: 720px;
    margin: 0 auto;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    border-radius: 22px;
    padding: 42px 36px;
    text-align: center;
    box-shadow: var(--glass-glow);
    position: relative;
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .verse-body-wrap {
    max-height: 0;
    opacity: 0;
    overflow: hidden;
    transform: translateY(10px);
    transition: max-height 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.5s ease, transform 0.5s ease, margin-bottom 0.4s ease;
    margin-bottom: 0;
  }
  .verse-body-wrap.revealed {
    max-height: 600px;
    opacity: 1;
    transform: translateY(0);
    margin-bottom: 26px;
  }
  .verse-arabic {
    font-family: var(--font-arabic);
    font-size: clamp(1.45rem, 5vw, 2.35rem);
    color: var(--gold-starlight);
    line-height: 1.8;
    margin-bottom: 18px;
    direction: rtl;
    text-shadow: 0 0 20px var(--gold-glow);
    word-break: break-word;
  }
  .verse-translation {
    font-family: var(--font-heading);
    font-size: clamp(0.98rem, 3.5vw, 1.15rem);
    font-style: italic;
    color: var(--starlight-blush);
    line-height: 1.75;
    margin-bottom: 14px;
  }
  .verse-reference {
    font-size: 0.92rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--celestial-orchid);
    font-weight: 500;
  }
  .btn-verse {
    min-height: 48px;
    background: rgba(114, 52, 119, 0.35);
    border: 1px solid var(--glass-border);
    color: var(--starlight-white);
    padding: 13px 30px;
    border-radius: 30px;
    font-size: 0.98rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }"""

content = content.replace(old_verse_css, new_verse_css)

# Update HTML for Chapter 6: wrap text in .verse-body-wrap and start collapsed
old_verse_html = """      <div class="verse-card">
        <div class="verse-arabic" id="verseArabic">
          وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً
        </div>
        <div class="verse-translation" id="verseTranslation">
          "And of His signs is that He created for you from yourselves mates that you may find tranquility in them; and He placed between you affection and mercy."
        </div>
        <div class="verse-reference" id="verseReference">
          Surah Ar-Rum • 30:21
        </div>
        <button type="button" class="btn-verse clickable" id="btnNextVerse" onclick="nextQuranVerse()">
          Show Me Another Ayah ✧
        </button>
      </div>"""

new_verse_html = """      <div class="verse-card">
        <!-- Verse body collapsed by default on page load -->
        <div class="verse-body-wrap" id="verseBodyWrap">
          <div class="verse-arabic" id="verseArabic"></div>
          <div class="verse-translation" id="verseTranslation"></div>
          <div class="verse-reference" id="verseReference"></div>
        </div>
        <button type="button" class="btn-verse clickable" id="btnNextVerse" onclick="revealOrNextQuranVerse()">
          Reveal an Ayah ✧
        </button>
      </div>"""

content = content.replace(old_verse_html, new_verse_html)

# Update JS for Chapter 6: revealOrNextQuranVerse()
old_verse_js = """  let currentVerseIndex = 0;
  function nextQuranVerse() {
    let nextIdx = Math.floor(Math.random() * quranVerses.length);
    while (nextIdx === currentVerseIndex && quranVerses.length > 1) {
      nextIdx = Math.floor(Math.random() * quranVerses.length);
    }
    currentVerseIndex = nextIdx;

    const v = quranVerses[currentVerseIndex];
    const arEl = document.getElementById("verseArabic");
    const trEl = document.getElementById("verseTranslation");
    const refEl = document.getElementById("verseReference");

    arEl.style.opacity = 0;
    trEl.style.opacity = 0;
    refEl.style.opacity = 0;

    setTimeout(() => {
      arEl.textContent = v.arabic;
      trEl.textContent = v.translation;
      refEl.textContent = v.reference;
      arEl.style.transition = trEl.style.transition = refEl.style.transition = "opacity 0.5s ease";
      arEl.style.opacity = trEl.style.opacity = refEl.style.opacity = 1;
    }, 300);
  }"""

new_verse_js = """  let currentVerseIndex = -1;
  let isVerseRevealed = false;

  function revealOrNextQuranVerse() {
    const wrap = document.getElementById("verseBodyWrap");
    const arEl = document.getElementById("verseArabic");
    const trEl = document.getElementById("verseTranslation");
    const refEl = document.getElementById("verseReference");
    const btn = document.getElementById("btnNextVerse");

    // Random selection avoiding back-to-back repetition
    let nextIdx = Math.floor(Math.random() * quranVerses.length);
    while (nextIdx === currentVerseIndex && quranVerses.length > 1) {
      nextIdx = Math.floor(Math.random() * quranVerses.length);
    }
    currentVerseIndex = nextIdx;
    const v = quranVerses[currentVerseIndex];

    if (!isVerseRevealed) {
      // First Click: Reveal the verse with smooth expansion
      isVerseRevealed = true;
      arEl.textContent = v.arabic;
      trEl.textContent = v.translation;
      refEl.textContent = v.reference;
      wrap.classList.add("revealed");
      btn.textContent = "Show Me Another Ayah ✧";
    } else {
      // Subsequent Clicks: Smooth cross-fade to next verse
      wrap.style.opacity = "0";
      setTimeout(() => {
        arEl.textContent = v.arabic;
        trEl.textContent = v.translation;
        refEl.textContent = v.reference;
        wrap.style.opacity = "1";
      }, 250);
    }
  }"""

content = content.replace(old_verse_js, new_verse_js)

# ==============================================================================
# 4. DODGING NO BUTTON MOBILE SAFEGUARD
# ==============================================================================
old_dodge_js = """  function dodgeNoButton() {
    dodgeCount++;
    const pad = 80;
    const btnW = btnNo.offsetWidth || 110;
    const btnH = btnNo.offsetHeight || 48;
    const maxW = window.innerWidth - btnW - pad;
    const maxH = window.innerHeight - btnH - pad;

    const yesRect = btnYes.getBoundingClientRect();
    let randX, randY, safe = false, attempts = 0;

    // Ensure No button never lands within 100px of Yes button
    while (!safe && attempts < 25) {
      randX = Math.max(pad, Math.floor(Math.random() * maxW));
      randY = Math.max(pad, Math.floor(Math.random() * maxH));
      attempts++;

      const dist = Math.hypot(randX - (yesRect.left + yesRect.width / 2), randY - (yesRect.top + yesRect.height / 2));
      if (dist > 180) safe = true;
    }

    btnNo.style.left = randX + "px";
    btnNo.style.top = randY + "px";

    proposeFeedback.textContent = playfulRemarks[Math.min(dodgeCount - 1, playfulRemarks.length - 1)];
  }"""

new_dodge_js = """  function dodgeNoButton() {
    dodgeCount++;
    const isSmallScreen = window.innerWidth < 600;
    const pad = isSmallScreen ? 14 : 50;
    const btnW = btnNo.offsetWidth || 90;
    const btnH = btnNo.offsetHeight || 44;
    const maxW = Math.max(14, window.innerWidth - btnW - pad);
    const maxH = Math.max(14, window.innerHeight - btnH - pad);

    const yesRect = btnYes.getBoundingClientRect();
    let randX, randY, safe = false, attempts = 0;
    const safeDistance = isSmallScreen ? 120 : 180;

    // Ensure No button never lands near or on top of Yes button
    while (!safe && attempts < 30) {
      randX = Math.max(pad, Math.floor(Math.random() * maxW));
      randY = Math.max(pad, Math.floor(Math.random() * maxH));
      attempts++;

      const dist = Math.hypot(randX - (yesRect.left + yesRect.width / 2), randY - (yesRect.top + yesRect.height / 2));
      if (dist > safeDistance) safe = true;
    }

    // Keep strictly within visible viewport bounds on all devices
    randX = Math.min(Math.max(pad, randX), window.innerWidth - btnW - 10);
    randY = Math.min(Math.max(pad, randY), window.innerHeight - btnH - 10);

    btnNo.style.left = randX + "px";
    btnNo.style.top = randY + "px";

    proposeFeedback.textContent = playfulRemarks[Math.min(dodgeCount - 1, playfulRemarks.length - 1)];
  }"""

content = content.replace(old_dodge_js, new_dodge_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Both updates applied successfully to index.html!")
