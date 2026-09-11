import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================================
# 1. REPLACE GALLERY CSS WITH ROMANTIC ASYMMETRIC POLAROID MEMORY WALL
# ==============================================================================
css_start = "/* ---------- CHAPTER 2: PHOTO GALLERY ---------- */"
css_end = "/* ---------- CHAPTER 3: INTERACTIVE ENVELOPES (COMPACT CLOSED DEFAULT) ---------- */"

idx1 = content.find(css_start)
idx2 = content.find(css_end)
assert idx1 != -1 and idx2 != -1, "Gallery CSS markers not found!"

new_gallery_css = """/* ---------- CHAPTER 2: ROMANTIC POLAROID MEMORY WALL ---------- */
    .gallery-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 34px 28px;
      align-items: start;
    }

    @media (max-width: 900px) {
      .gallery-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 28px 22px;
      }
      .photo-frame:nth-child(even) {
        margin-top: 28px; /* Organic staggered 2-column layout */
      }
    }

    @media (max-width: 560px) {
      .gallery-grid {
        grid-template-columns: 1fr;
        max-width: 360px;
        margin: 0 auto;
        gap: 30px;
      }
      .photo-frame:nth-child(even) {
        margin-top: 0 !important;
      }
    }

    /* Asymmetric Polaroid Frame with tactile depth and warm celestial tint */
    .photo-frame {
      background: linear-gradient(175deg, rgba(255, 245, 250, 0.1) 0%, rgba(38, 12, 48, 0.88) 12%, rgba(20, 5, 28, 0.95) 100%);
      border: 1px solid rgba(246, 214, 229, 0.22);
      border-radius: 16px;
      padding: 14px 14px 18px 14px; /* Classic polaroid bottom-heavy margin */
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.55), 0 0 20px rgba(114, 52, 119, 0.25);
      transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, border-color 0.3s ease;
      position: relative;
      overflow: visible;
      cursor: default;
    }

    /* Subtle frosted rose washi tape strip on top of polaroids */
    .photo-frame::after {
      content: '';
      position: absolute;
      top: -9px;
      left: 50%;
      transform: translateX(-50%);
      width: 52px;
      height: 15px;
      background: rgba(246, 214, 229, 0.18);
      border: 1px solid rgba(246, 214, 229, 0.3);
      backdrop-filter: blur(4px);
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
      border-radius: 2px;
      z-index: 12;
      pointer-events: none;
    }

    /* Organic scattered rotations & staggered heights for natural memory wall feel */
    .photo-frame:nth-child(1) {
      transform: rotate(-1.8deg);
    }
    .photo-frame:nth-child(2) {
      transform: rotate(1.6deg);
      margin-top: 36px; /* Staggered downward on desktop */
    }
    .photo-frame:nth-child(3) {
      transform: rotate(-2.2deg);
      margin-top: 8px;
    }
    .photo-frame:nth-child(4) {
      transform: rotate(1.5deg);
    }
    .photo-frame:nth-child(5) {
      transform: rotate(-1.4deg);
      margin-top: 32px; /* Staggered downward on desktop */
    }
    .photo-frame:nth-child(6) {
      transform: rotate(2deg);
      margin-top: 6px;
    }

    /* Interactive hover: gentle straighten and lift with starlight glow */
    @media (hover: hover) and (pointer: fine) {
      .photo-frame:hover {
        transform: rotate(0deg) translateY(-8px) scale(1.025);
        border-color: rgba(246, 214, 229, 0.5);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 30px rgba(190, 111, 171, 0.45);
        z-index: 25;
      }
      .photo-frame:hover .frame-inner img {
        transform: scale(1.05);
      }
    }

    /* Photo Cutout Window */
    .frame-inner {
      width: 100%;
      border-radius: 8px;
      overflow: hidden;
      position: relative;
      background: radial-gradient(circle at center, #2e0d3a 0%, #15041d 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 24px 16px;
      border: 1px solid rgba(190, 111, 171, 0.2);
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.6);
    }

    /* Varied aspect ratios across frames to break uniform box look */
    .photo-frame:nth-child(1) .frame-inner { aspect-ratio: 4/5.2; }
    .photo-frame:nth-child(2) .frame-inner { aspect-ratio: 4/4.8; }
    .photo-frame:nth-child(3) .frame-inner { aspect-ratio: 4/5.4; }
    .photo-frame:nth-child(4) .frame-inner { aspect-ratio: 4/4.9; }
    .photo-frame:nth-child(5) .frame-inner { aspect-ratio: 4/5.3; }
    .photo-frame:nth-child(6) .frame-inner { aspect-ratio: 4/4.7; }

    .frame-inner img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 2;
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Delicate Romantic Scrapbook Invitation ("add a memory...") */
    .btn-add-photo {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      margin-top: 14px;
      padding: 8px 16px;
      border-radius: 20px;
      background: rgba(114, 52, 119, 0.16);
      border: 1.5px dashed rgba(199, 116, 178, 0.5);
      color: var(--starlight-blush);
      font-family: var(--font-heading);
      font-style: italic;
      font-size: 0.95rem;
      letter-spacing: 0.02em;
      cursor: pointer;
      transition: all 0.3s ease;
      position: relative;
      z-index: 5;
    }

    .btn-add-photo:hover {
      background: rgba(114, 52, 119, 0.38);
      border-color: var(--celestial-orchid);
      border-style: solid;
      color: #ffffff;
      transform: translateY(-2px);
      box-shadow: 0 4px 18px rgba(190, 111, 171, 0.4);
    }

    .btn-add-photo:active {
      transform: scale(0.96);
    }

    /* Discrete Change control - only visible on hover (desktop) or gentle corner badge (mobile) */
    .btn-change-photo {
      position: absolute;
      top: 10px;
      right: 10px;
      z-index: 20;
      padding: 5px 12px;
      font-size: 0.74rem;
      font-weight: 500;
      font-family: var(--font-body);
      border-radius: 14px;
      background: rgba(18, 4, 26, 0.88);
      border: 1px solid rgba(246, 214, 229, 0.4);
      color: var(--starlight-blush);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      cursor: pointer;
      display: none;
      align-items: center;
      gap: 5px;
      box-shadow: 0 3px 12px rgba(0, 0, 0, 0.6);
      opacity: 0;
      pointer-events: none;
      transform: translateY(-4px);
      transition: all 0.25s ease;
    }

    /* On desktop, reveal change button only when photo is hovered */
    @media (hover: hover) and (pointer: fine) {
      .photo-frame.has-photo:hover .btn-change-photo {
        display: inline-flex;
        opacity: 0.95;
        pointer-events: auto;
        transform: translateY(0);
      }
      .btn-change-photo:hover {
        opacity: 1;
        background: rgba(45, 13, 56, 0.98);
        border-color: var(--celestial-orchid);
        color: #ffffff;
        transform: scale(1.05);
      }
    }

    /* On mobile touch devices, keep change button subtle in corner without blocking photo */
    @media (hover: none) or (pointer: coarse) {
      .photo-frame.has-photo .btn-change-photo {
        display: inline-flex;
        opacity: 0.8;
        pointer-events: auto;
        transform: none;
      }
      .btn-change-photo:active {
        opacity: 1;
        transform: scale(0.95);
      }
    }

    /* Processing & Loading Overlay */
    .frame-loader {
      position: absolute;
      inset: 0;
      z-index: 15;
      background: rgba(18, 5, 26, 0.9);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 10px;
      color: var(--starlight-blush);
      font-size: 0.88rem;
      font-family: var(--font-heading);
      font-style: italic;
    }

    .loader-spinner {
      width: 30px;
      height: 30px;
      border: 3px solid rgba(190, 111, 171, 0.25);
      border-top-color: var(--celestial-orchid);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    /* Inline Error Badge */
    .frame-error-badge {
      position: absolute;
      bottom: 12px;
      left: 10px;
      right: 10px;
      z-index: 20;
      padding: 7px 10px;
      border-radius: 10px;
      background: rgba(74, 15, 35, 0.92);
      border: 1px solid rgba(235, 87, 87, 0.6);
      color: #ffd6d6;
      font-size: 0.78rem;
      text-align: center;
      backdrop-filter: blur(6px);
      display: none;
    }

    /* Polaroid Scrapbook Placeholder Content */
    .placeholder-card {
      z-index: 1;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 8px 6px;
    }

    /* Warm glowing delicate heart outline (replaces corporate star) */
    .memory-heart-icon {
      color: var(--celestial-orchid);
      margin-bottom: 10px;
      filter: drop-shadow(0 0 8px rgba(190, 111, 171, 0.6));
      opacity: 0.9;
      transition: transform 0.3s ease;
    }

    .photo-frame:hover .memory-heart-icon {
      transform: scale(1.1);
      color: var(--starlight-blush);
    }

    /* Romantic Handwritten Polaroid Note Typography */
    .polaroid-title {
      font-family: var(--font-heading);
      font-size: 1.15rem;
      font-style: italic;
      color: var(--starlight-blush);
      margin-bottom: 4px;
      letter-spacing: 0.02em;
    }

    .polaroid-sub {
      font-size: 0.84rem;
      color: var(--text-dim);
      font-style: italic;
      line-height: 1.4;
    }

    /* Handwritten Polaroid Bottom Caption */
    .frame-caption {
      margin-top: 13px;
      text-align: center;
      font-size: 0.95rem;
      color: var(--starlight-blush);
      font-family: var(--font-heading);
      font-style: italic;
      letter-spacing: 0.03em;
      opacity: 0.92;
    }

    """

content = content[:idx1] + new_gallery_css + content[idx2:]

# ==============================================================================
# 2. UPDATE CHAPTER 2 GALLERY HTML
# ==============================================================================
html_start = '<!-- Frame 1: Your favourite photo of us -->'
html_end = '<!-- CHAPTER 3: INTERACTIVE ENVELOPES'

idx_h1 = content.find(html_start)
idx_h2 = content.find(html_end)
assert idx_h1 != -1 and idx_h2 != -1, "Gallery HTML markers not found!"

new_gallery_html = """<!-- Frame 1: Your favourite photo of us -->
          <div class="photo-frame" id="photoFrame1">
            <div class="frame-inner" id="frameInner1">
              <input type="file" id="photoInput1" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(1, this)">
              <img id="galleryImg1" src="photo1.jpg" alt="Your favourite photo of us" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder1">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">First Steps</div>
                <div class="polaroid-sub">your smile that lights up my universe</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(1)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader1">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError1"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange1" style="display:none" onclick="triggerPhotoUpload(1)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ your favourite photo of us ~</div>
          </div>

          <!-- Frame 2: A trip you both loved -->
          <div class="photo-frame" id="photoFrame2">
            <div class="frame-inner" id="frameInner2">
              <input type="file" id="photoInput2" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(2, this)">
              <img id="galleryImg2" src="photo2.jpg" alt="A trip you both loved" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder2">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">Blessed Journey</div>
                <div class="polaroid-sub">Umrah together before the Kaaba</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(2)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader2">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError2"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange2" style="display:none" onclick="triggerPhotoUpload(2)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ a trip you both loved ~</div>
          </div>

          <!-- Frame 3: Her, mid-laugh -->
          <div class="photo-frame" id="photoFrame3">
            <div class="frame-inner" id="frameInner3">
              <input type="file" id="photoInput3" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(3, this)">
              <img id="galleryImg3" src="photo3.jpg" alt="Her, mid-laugh" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder3">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">Her, Mid-Laugh</div>
                <div class="polaroid-sub">Kutty Shafeen teasing moment</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(3)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader3">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError3"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange3" style="display:none" onclick="triggerPhotoUpload(3)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ her, mid-laugh ~</div>
          </div>

          <!-- Frame 4: A quiet ordinary day -->
          <div class="photo-frame" id="photoFrame4">
            <div class="frame-inner" id="frameInner4">
              <input type="file" id="photoInput4" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(4, this)">
              <img id="galleryImg4" src="photo4.jpg" alt="A quiet ordinary day" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder4">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">A Quiet Ordinary Day</div>
                <div class="polaroid-sub">where I find stillness and rest</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(4)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader4">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError4"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange4" style="display:none" onclick="triggerPhotoUpload(4)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ a quiet ordinary day ~</div>
          </div>

          <!-- Frame 5: The two of you, together -->
          <div class="photo-frame" id="photoFrame5">
            <div class="frame-inner" id="frameInner5">
              <input type="file" id="photoInput5" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(5, this)">
              <img id="galleryImg5" src="photo5.jpg" alt="The two of you, together" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder5">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">Side By Side</div>
                <div class="polaroid-sub">the two of us, together always</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(5)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader5">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError5"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange5" style="display:none" onclick="triggerPhotoUpload(5)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ the two of you, together ~</div>
          </div>

          <!-- Frame 6: One more, just because -->
          <div class="photo-frame" id="photoFrame6">
            <div class="frame-inner" id="frameInner6">
              <input type="file" id="photoInput6" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(6, this)">
              <img id="galleryImg6" src="photo6.jpg" alt="One more, just because" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder6">
                <svg class="memory-heart-icon" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <div class="polaroid-title">Forever Ahead</div>
                <div class="polaroid-sub">Bangalore to Madurai, one heart</div>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(6)">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>add a memory...</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader6">
                <div class="loader-spinner"></div>
                <span>Adding to our wall... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError6"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange6" style="display:none" onclick="triggerPhotoUpload(6)">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>change</span>
              </button>
            </div>
            <div class="frame-caption">~ one more, just because ~</div>
          </div>
        </div>
      </div>
    </section>

    """

content = content[:idx_h1] + new_gallery_html + content[idx_h2:]

# ==============================================================================
# 3. UPDATE displayPhotoInFrame TO ADD has-photo CLASS TO FRAME
# ==============================================================================
old_display_func = """function displayPhotoInFrame(frameId, dataUrl) {
      const imgEl = document.getElementById("galleryImg" + frameId);
      const placeholderEl = document.getElementById("placeholder" + frameId);
      const changeBtn = document.getElementById("btnChange" + frameId);

      if (imgEl) {
        imgEl.src = dataUrl;
        imgEl.style.display = "block";
      }
      if (placeholderEl) {
        placeholderEl.style.display = "none";
      }
      if (changeBtn) {
        changeBtn.style.display = "inline-flex";
      }
    }"""

new_display_func = """function displayPhotoInFrame(frameId, dataUrl) {
      const imgEl = document.getElementById("galleryImg" + frameId);
      const placeholderEl = document.getElementById("placeholder" + frameId);
      const changeBtn = document.getElementById("btnChange" + frameId);
      const frameEl = document.getElementById("photoFrame" + frameId);

      if (imgEl) {
        imgEl.src = dataUrl;
        imgEl.style.display = "block";
      }
      if (placeholderEl) {
        placeholderEl.style.display = "none";
      }
      if (frameEl) {
        frameEl.classList.add("has-photo");
      }
    }"""

assert old_display_func in content, "old_display_func not found!"
content = content.replace(old_display_func, new_display_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Romantic polaroid photo wall redesign applied to index.html!")
