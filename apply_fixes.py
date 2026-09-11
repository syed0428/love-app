import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================================
# 1. FIX LOVE-NOTE ENVELOPES: COMPACT CLOSED DEFAULT + DISPLAY: NONE WHEN CLOSED
# ==============================================================================
old_env_start = "/* ---------- CHAPTER 3: INTERACTIVE ENVELOPES ---------- */"
old_env_end = "/* ---------- CHAPTER 4: WAX-SEALED LOVE LETTER ---------- */"

idx1 = content.find(old_env_start)
idx2 = content.find(old_env_end)
assert idx1 != -1 and idx2 != -1, "Envelope CSS markers not found!"

new_envelopes_css = """/* ---------- CHAPTER 3: INTERACTIVE ENVELOPES (COMPACT CLOSED DEFAULT) ---------- */
    .envelopes-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
      align-items: start; /* Prevents closed cards from stretching when a sibling opens */
    }

    @media (max-width: 860px) {
      .envelopes-grid {
        grid-template-columns: 1fr;
        max-width: 440px;
        margin: 0 auto;
        gap: 16px;
      }
    }

    /* Compact closed envelope state by default */
    .envelope-card {
      background: rgba(35, 10, 45, 0.72);
      border: 1px solid var(--glass-border);
      border-radius: 16px;
      padding: 22px 20px;
      text-align: center;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
    }

    .envelope-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, transparent, var(--celestial-orchid), transparent);
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .envelope-card:hover {
      transform: translateY(-4px);
      background: rgba(50, 16, 62, 0.85);
      border-color: var(--glass-border-strong);
      box-shadow: 0 12px 35px rgba(114, 52, 119, 0.4);
    }

    .envelope-card:hover::before {
      opacity: 1;
    }

    .env-icon {
      font-size: 2.2rem;
      color: var(--celestial-orchid);
      margin-bottom: 8px;
      display: inline-block;
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      filter: drop-shadow(0 0 10px rgba(190, 111, 171, 0.5));
    }

    .envelope-card:hover .env-icon {
      transform: scale(1.12) rotate(4deg);
    }

    .envelope-card h3 {
      font-size: 1.18rem;
      margin-bottom: 6px;
      color: var(--starlight-blush);
      font-weight: 500;
    }

    .envelope-card .env-teaser {
      font-size: 0.85rem;
      color: var(--text-dim);
      letter-spacing: 0.02em;
    }

    /* Content is strictly hidden and collapsed by default */
    .env-content {
      display: none;
      opacity: 0;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.45s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
      color: var(--text-muted);
      font-size: 0.96rem;
      line-height: 1.7;
      text-align: left;
      margin-top: 0;
      padding-top: 0;
      border-top: 1px dashed transparent;
    }

    /* Expanded open state on click */
    .envelope-card.open {
      background: rgba(54, 18, 68, 0.88);
      border-color: var(--celestial-orchid);
      padding: 26px 24px 26px;
      box-shadow: 0 12px 40px rgba(114, 52, 119, 0.45), var(--glass-glow);
    }

    .envelope-card.open .env-teaser {
      display: none;
    }

    .envelope-card.open .env-content {
      display: block;
      max-height: 600px;
      opacity: 1;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px dashed rgba(190, 111, 171, 0.4);
    }

    """

content = content[:idx1] + new_envelopes_css + content[idx2:]

# ==============================================================================
# 2. FIX GATE CSS: OVERFLOW HIDDEN
# ==============================================================================
gate_needle = ".gate {\n      position: fixed;\n      inset: 0;"
idx_gate = content.find(gate_needle)
assert idx_gate != -1, "Gate CSS not found!"
idx_gate_end = content.find("}", idx_gate)

new_gate_css = """.gate {
      position: fixed;
      inset: 0;
      width: 100%;
      width: 100vw;
      height: 100vh;
      height: 100svh;
      height: 100dvh;
      z-index: 500;
      background: radial-gradient(circle at center, #350c44 0%, #210535 55%, #0d0216 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: calc(16px + env(safe-area-inset-top, 0px)) 16px calc(16px + env(safe-area-inset-bottom, 0px));
      overflow: hidden; /* Prevent scrollbars during button dodging */
      transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.8s ease;
    }"""

content = content[:idx_gate] + new_gate_css + content[idx_gate_end+1:]

# ==============================================================================
# 3. FIX .btn-no-dodger CSS: VIEWPORT POSITIONING
# ==============================================================================
no_btn_needle = "/* Floating Dodging No Button */"
idx_no = content.find(no_btn_needle)
assert idx_no != -1, "btn-no-dodger CSS not found!"
idx_no_end = content.find("/* --- Celebration Confetti", idx_no)

new_no_btn_css = """/* Floating Dodging No Button - Positioned in Viewport Space */
    .btn-no-dodger {
      position: fixed;
      min-height: 44px;
      background: rgba(45, 13, 56, 0.92);
      color: var(--text-muted);
      border: 1px solid var(--glass-border);
      padding: 12px 28px;
      font-size: 1rem;
      font-weight: 500;
      border-radius: 30px;
      cursor: pointer;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: left 0.26s cubic-bezier(0.18, 0.89, 0.32, 1.28), top 0.26s cubic-bezier(0.18, 0.89, 0.32, 1.28);
      z-index: 520; /* Floating directly in gate viewport */
      user-select: none;
      white-space: nowrap;
      display: none; /* Shown dynamically when propose gate dialog activates */
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    @media (max-width: 480px) {
      .btn-no-dodger {
        padding: 10px 20px;
        font-size: 0.95rem;
        min-height: 44px;
      }
    }

    """

content = content[:idx_no] + new_no_btn_css + content[idx_no_end:]

# ==============================================================================
# 4. MOVE #btnNo FROM INSIDE propose-buttons TO DIRECT CHILD OF #gateOverlay
# ==============================================================================
propose_needle = '<div class="propose-buttons">'
idx_prop = content.find(propose_needle)
assert idx_prop != -1, "propose-buttons HTML not found!"
idx_prop_end = content.find('<!-- ==========================================================================\n     MAIN APPLICATION', idx_prop)

old_prop_block = content[idx_prop:idx_prop_end]
# Remove btnNo from propose-buttons
new_prop_block = old_prop_block.replace(
    '<button type="button" class="btn-no-dodger clickable" id="btnNo">No</button>',
    ''
)
# Insert btnNo right before </div>\n\n  </div>
last_div = new_prop_block.rfind('</div>')
new_prop_block = new_prop_block[:last_div] + '    <!-- Floating Dodging No Button (direct child of gateOverlay for true viewport fixed positioning) -->\n    <button type="button" class="btn-no-dodger clickable" id="btnNo">No</button>\n  ' + new_prop_block[last_div:]

content = content[:idx_prop] + new_prop_block + content[idx_prop_end:]

# ==============================================================================
# 5. UPDATE DIALOG SWITCH TO SHOW btnNo
# ==============================================================================
old_switch = """dateGateDialog.style.display = "none";
              proposeGateDialog.classList.add("active");
              initNoButtonPosition();"""

new_switch = """dateGateDialog.style.display = "none";
              proposeGateDialog.classList.add("active");
              if (btnNo) {
                btnNo.style.display = "inline-flex";
                initNoButtonPosition();
              }"""

assert old_switch in content, "old_switch not found!"
content = content.replace(old_switch, new_switch)

# ==============================================================================
# 6. UPDATE JS DODGING LOGIC WITH STRICT BOUNDS & SCROLLBAR AVOIDANCE
# ==============================================================================
dodge_needle = "function initNoButtonPosition()"
idx_dodge = content.find(dodge_needle)
assert idx_dodge != -1, "initNoButtonPosition JS not found!"
idx_dodge_end = content.find("if (btnNo) {", idx_dodge)

new_dodge_js = """function initNoButtonPosition() {
      const spacer = document.querySelector(".no-spacer");
      if (!spacer || !btnNo) return;
      const rect = spacer.getBoundingClientRect();
      btnNo.style.display = "inline-flex";
      btnNo.style.left = rect.left + "px";
      btnNo.style.top = rect.top + "px";
    }

    window.addEventListener("resize", () => {
      if (proposeGateDialog && proposeGateDialog.classList.contains("active") && dodgeCount === 0) {
        initNoButtonPosition();
      }
    });

    function dodgeNoButton() {
      dodgeCount++;
      btnNo.style.display = "inline-flex";

      const isMobile = window.innerWidth < 480;
      const padX = isMobile ? 24 : 40;
      const padY = isMobile ? 24 : 40;
      const btnW = btnNo.offsetWidth || (isMobile ? 86 : 100);
      const btnH = btnNo.offsetHeight || 44;

      // Absolute strict viewport constraints
      const minX = padX;
      const maxX = Math.max(minX, window.innerWidth - btnW - padX);
      const minY = padY;
      const maxY = Math.max(minY, window.innerHeight - btnH - padY);

      const yesRect = btnYes.getBoundingClientRect();
      const yesCenterX = yesRect.left + yesRect.width / 2;
      const yesCenterY = yesRect.top + yesRect.height / 2;
      const safeDist = isMobile ? 110 : 160;

      let randX = minX, randY = minY;
      let safe = false, attempts = 0;

      // Calculate safe coordinates avoiding the YES button
      while (!safe && attempts < 40) {
        randX = minX + Math.floor(Math.random() * (maxX - minX + 1));
        randY = minY + Math.floor(Math.random() * (maxY - minY + 1));
        attempts++;

        const noCenterX = randX + btnW / 2;
        const noCenterY = randY + btnH / 2;
        const dist = Math.hypot(noCenterX - yesCenterX, noCenterY - yesCenterY);

        if (dist >= safeDist) {
          safe = true;
        }
      }

      // Hard clamp: 100% guaranteed to remain inside visible screen with margin
      randX = Math.max(minX, Math.min(randX, maxX));
      randY = Math.max(minY, Math.min(randY, maxY));

      btnNo.style.left = randX + "px";
      btnNo.style.top = randY + "px";

      proposeFeedback.textContent = playfulRemarks[Math.min(dodgeCount - 1, playfulRemarks.length - 1)];
    }

    """

content = content[:idx_dodge] + new_dodge_js + content[idx_dodge_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: index.html has been updated with both fixes!")
