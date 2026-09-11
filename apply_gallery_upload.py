import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==============================================================================
# 1. ADD CSS FOR ADD PHOTO / CHANGE PHOTO / LOADER / ERROR BADGE
# ==============================================================================
gallery_css_needle = "/* Fallback Card when image is not yet loaded */"
idx_css = content.find(gallery_css_needle)
assert idx_css != -1, "gallery_css_needle not found!"

new_gallery_css = """/* In-Browser Photo Upload & Change Controls */
    .btn-add-photo {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 14px;
      padding: 9px 18px;
      border-radius: 20px;
      background: linear-gradient(135deg, rgba(114, 52, 119, 0.75), rgba(190, 111, 171, 0.5));
      border: 1px solid var(--celestial-orchid);
      color: var(--starlight-blush);
      font-family: var(--font-body);
      font-size: 0.88rem;
      font-weight: 500;
      letter-spacing: 0.02em;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(114, 52, 119, 0.35);
      transition: all 0.25s ease;
      position: relative;
      z-index: 5;
    }

    .btn-add-photo:hover {
      background: linear-gradient(135deg, rgba(148, 68, 152, 0.92), rgba(199, 116, 178, 0.75));
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(190, 111, 171, 0.55);
      color: var(--starlight-white);
    }

    .btn-add-photo:active {
      transform: scale(0.96);
    }

    /* Change photo pill button - discrete in corner to prevent accidental taps */
    .btn-change-photo {
      position: absolute;
      bottom: 10px;
      right: 10px;
      z-index: 10;
      padding: 6px 14px;
      font-size: 0.78rem;
      font-weight: 500;
      font-family: var(--font-body);
      border-radius: 18px;
      background: rgba(22, 6, 32, 0.88);
      border: 1px solid rgba(190, 111, 171, 0.6);
      color: var(--starlight-blush);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      cursor: pointer;
      display: none; /* Displayed dynamically when photo exists */
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
      opacity: 0.92;
      transition: all 0.25s ease;
    }

    .btn-change-photo:hover {
      opacity: 1;
      background: rgba(45, 13, 56, 0.98);
      border-color: var(--celestial-orchid);
      color: var(--starlight-white);
      transform: scale(1.04);
      box-shadow: 0 6px 20px rgba(190, 111, 171, 0.5);
    }

    .btn-change-photo:active {
      transform: scale(0.96);
    }

    /* Processing & Loading Overlay */
    .frame-loader {
      position: absolute;
      inset: 0;
      z-index: 15;
      background: rgba(18, 5, 26, 0.88);
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: var(--starlight-blush);
      font-size: 0.88rem;
      font-family: var(--font-body);
    }

    .loader-spinner {
      width: 32px;
      height: 32px;
      border: 3px solid rgba(190, 111, 171, 0.25);
      border-top-color: var(--celestial-orchid);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* Inline Error Badge */
    .frame-error-badge {
      position: absolute;
      bottom: 12px;
      left: 12px;
      right: 12px;
      z-index: 20;
      padding: 8px 12px;
      border-radius: 12px;
      background: rgba(74, 15, 35, 0.92);
      border: 1px solid rgba(235, 87, 87, 0.6);
      color: #ffd6d6;
      font-size: 0.8rem;
      text-align: center;
      backdrop-filter: blur(6px);
      display: none;
    }

    /* Fallback Card when image is not yet loaded */"""

content = content[:idx_css] + new_gallery_css + content[idx_css + len(gallery_css_needle):]

# ==============================================================================
# 2. UPDATE GALLERY HTML (FRAMES 1 TO 6)
# ==============================================================================
old_gallery_start = '<!-- Frame 1: Your favourite photo of us -->'
old_gallery_end = '<!-- CHAPTER 3: INTERACTIVE ENVELOPES'

idx_g1 = content.find(old_gallery_start)
idx_g2 = content.find(old_gallery_end)
assert idx_g1 != -1 and idx_g2 != -1, "Gallery frames HTML markers not found!"

new_gallery_html = """<!-- Frame 1: Your favourite photo of us -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner1">
              <input type="file" id="photoInput1" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(1, this)">
              <img id="galleryImg1" src="photo1.jpg" alt="Your favourite photo of us" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder1">
                <div class="star-icon">✦</div>
                <h4>First Steps</h4>
                <p>Your smile that lights up the room</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(1)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader1">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError1"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange1" onclick="triggerPhotoUpload(1)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"Your favourite photo of us"</div>
          </div>

          <!-- Frame 2: A trip you both loved -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner2">
              <input type="file" id="photoInput2" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(2, this)">
              <img id="galleryImg2" src="photo2.jpg" alt="A trip you both loved" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder2">
                <div class="star-icon">✦</div>
                <h4>Blessed Journey</h4>
                <p>Umrah together in Mecca</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(2)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader2">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError2"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange2" onclick="triggerPhotoUpload(2)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"A trip you both loved"</div>
          </div>

          <!-- Frame 3: Her, mid-laugh -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner3">
              <input type="file" id="photoInput3" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(3, this)">
              <img id="galleryImg3" src="photo3.jpg" alt="Her, mid-laugh" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder3">
                <div class="star-icon">✦</div>
                <h4>Laughter</h4>
                <p>Every small teasing moment</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(3)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader3">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError3"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange3" onclick="triggerPhotoUpload(3)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"Her, mid-laugh"</div>
          </div>

          <!-- Frame 4: A quiet ordinary day -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner4">
              <input type="file" id="photoInput4" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(4, this)">
              <img id="galleryImg4" src="photo4.jpg" alt="A quiet ordinary day" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder4">
                <div class="star-icon">✦</div>
                <h4>Our Quiet Evenings</h4>
                <p>Peaceful conversations together</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(4)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader4">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError4"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange4" onclick="triggerPhotoUpload(4)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"A quiet ordinary day"</div>
          </div>

          <!-- Frame 5: The two of you, together -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner5">
              <input type="file" id="photoInput5" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(5, this)">
              <img id="galleryImg5" src="photo5.jpg" alt="The two of you, together" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder5">
                <div class="star-icon">✦</div>
                <h4>Madurai Days</h4>
                <p>Treasured hometown memories</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(5)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader5">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError5"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange5" onclick="triggerPhotoUpload(5)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"The two of you, together"</div>
          </div>

          <!-- Frame 6: One more, just because -->
          <div class="photo-frame">
            <div class="frame-inner" id="frameInner6">
              <input type="file" id="photoInput6" class="photo-file-input" accept="image/*" style="display:none" onchange="handlePhotoUpload(6, this)">
              <img id="galleryImg6" src="photo6.jpg" alt="One more, just because" class="frame-photo" style="display:none" onerror="this.style.display='none'">
              
              <div class="placeholder-card" id="placeholder6">
                <div class="star-icon">✦</div>
                <h4>Forever Ahead</h4>
                <p>Waiting to be together again</p>
                <button type="button" class="btn-add-photo clickable" onclick="triggerPhotoUpload(6)">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                  </svg>
                  <span>Add Photo</span>
                </button>
              </div>

              <div class="frame-loader" id="frameLoader6">
                <div class="loader-spinner"></div>
                <span>Saving photo... ✨</span>
              </div>
              <div class="frame-error-badge" id="frameError6"></div>

              <button type="button" class="btn-change-photo clickable" id="btnChange6" onclick="triggerPhotoUpload(6)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
                <span>Change</span>
              </button>
            </div>
            <div class="frame-caption">"One more, just because"</div>
          </div>
        </div>
      </div>
    </section>

    """

content = content[:idx_g1] + new_gallery_html + content[idx_g2:]

# ==============================================================================
# 3. ADD JAVASCRIPT: INDEXEDDB / LOCALSTORAGE PERSISTENCE & UPLOAD LOGIC
# ==============================================================================
js_anchor = "function toggleEnvelope(card)"
idx_js = content.find(js_anchor)
assert idx_js != -1, "js_anchor not found!"

new_gallery_js = """// ============================================================================
    // CHAPTER 2: IN-BROWSER PHOTO UPLOAD & INDEXEDDB / LOCALSTORAGE PERSISTENCE
    // ============================================================================
    const GALLERY_DB_NAME = "HayathiLoveGalleryDB";
    const GALLERY_DB_VERSION = 1;
    const GALLERY_STORE_NAME = "photos";

    function openGalleryDB() {
      return new Promise((resolve) => {
        if (!window.indexedDB) {
          resolve(null);
          return;
        }
        try {
          const req = window.indexedDB.open(GALLERY_DB_NAME, GALLERY_DB_VERSION);
          req.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains(GALLERY_STORE_NAME)) {
              db.createObjectStore(GALLERY_STORE_NAME);
            }
          };
          req.onsuccess = (e) => resolve(e.target.result);
          req.onerror = () => resolve(null);
        } catch (err) {
          resolve(null);
        }
      });
    }

    async function saveGalleryPhoto(frameId, dataUrl) {
      try {
        const db = await openGalleryDB();
        if (db) {
          return new Promise((resolve) => {
            const tx = db.transaction(GALLERY_STORE_NAME, "readwrite");
            tx.objectStore(GALLERY_STORE_NAME).put(dataUrl, frameId);
            tx.oncomplete = () => {
              db.close();
              resolve(true);
            };
            tx.onerror = () => {
              db.close();
              fallbackSaveLS(frameId, dataUrl);
              resolve(true);
            };
          });
        } else {
          fallbackSaveLS(frameId, dataUrl);
        }
      } catch (err) {
        fallbackSaveLS(frameId, dataUrl);
      }
    }

    function fallbackSaveLS(frameId, dataUrl) {
      try {
        localStorage.setItem("hayathi_gallery_" + frameId, dataUrl);
      } catch (err) {
        console.warn("Storage quota exceeded", err);
      }
    }

    async function getGalleryPhoto(frameId) {
      try {
        const db = await openGalleryDB();
        if (db) {
          return new Promise((resolve) => {
            const tx = db.transaction(GALLERY_STORE_NAME, "readonly");
            const req = tx.objectStore(GALLERY_STORE_NAME).get(frameId);
            req.onsuccess = (e) => {
              db.close();
              const val = e.target.result;
              if (val) resolve(val);
              else resolve(fallbackGetLS(frameId));
            };
            req.onerror = () => {
              db.close();
              resolve(fallbackGetLS(frameId));
            };
          });
        }
      } catch (err) {}
      return fallbackGetLS(frameId);
    }

    function fallbackGetLS(frameId) {
      try {
        return localStorage.getItem("hayathi_gallery_" + frameId);
      } catch (err) {
        return null;
      }
    }

    function triggerPhotoUpload(frameId) {
      const input = document.getElementById("photoInput" + frameId);
      if (input) {
        input.value = "";
        input.click();
      }
    }

    function handlePhotoUpload(frameId, input) {
      const file = input.files && input.files[0];
      if (!file) return;

      const loader = document.getElementById("frameLoader" + frameId);

      if (!file.type.startsWith("image/")) {
        showFrameError(frameId, "Please select an image file (JPG, PNG, WebP) ✨");
        return;
      }

      if (loader) loader.style.display = "flex";

      const reader = new FileReader();
      reader.onerror = () => {
        if (loader) loader.style.display = "none";
        showFrameError(frameId, "Unable to read image. Please try another! ✨");
      };

      reader.onload = (e) => {
        const rawDataUrl = e.target.result;
        const img = new Image();
        img.onerror = () => {
          if (loader) loader.style.display = "none";
          showFrameError(frameId, "Image format error. Please try another! ✨");
        };

        img.onload = async () => {
          try {
            // Downsample gracefully to max 1440px to ensure fast loads & smooth performance
            const MAX_DIM = 1440;
            let w = img.width;
            let h = img.height;
            if (w > MAX_DIM || h > MAX_DIM) {
              if (w > h) {
                h = Math.round((h * MAX_DIM) / w);
                w = MAX_DIM;
              } else {
                w = Math.round((w * MAX_DIM) / h);
                h = MAX_DIM;
              }
            }
            const canvas = document.createElement("canvas");
            canvas.width = w;
            canvas.height = h;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, w, h);
            const optimizedDataUrl = canvas.toDataURL("image/jpeg", 0.90);

            await saveGalleryPhoto(frameId, optimizedDataUrl);
            displayPhotoInFrame(frameId, optimizedDataUrl);
          } catch (err) {
            await saveGalleryPhoto(frameId, rawDataUrl);
            displayPhotoInFrame(frameId, rawDataUrl);
          } finally {
            if (loader) loader.style.display = "none";
          }
        };
        img.src = rawDataUrl;
      };

      reader.readAsDataURL(file);
    }

    function displayPhotoInFrame(frameId, dataUrl) {
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
    }

    function showFrameError(frameId, msg) {
      const errorEl = document.getElementById("frameError" + frameId);
      if (!errorEl) return;
      errorEl.textContent = msg;
      errorEl.style.display = "block";
      setTimeout(() => {
        errorEl.style.display = "none";
      }, 3500);
    }

    async function initGalleryPhotos() {
      for (let i = 1; i <= 6; i++) {
        const saved = await getGalleryPhoto(i);
        if (saved) {
          displayPhotoInFrame(i, saved);
        } else {
          // Check if local file exists on disk
          const testImg = new Image();
          testImg.onload = () => {
            displayPhotoInFrame(i, `photo${i}.jpg`);
          };
          testImg.onerror = () => {
            // Keep empty placeholder visible
          };
          testImg.src = `photo${i}.jpg`;
        }
      }
    }

    // Call on load
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initGalleryPhotos);
    } else {
      initGalleryPhotos();
    }

    """

content = content[:idx_js] + new_gallery_js + content[idx_js:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: In-browser Photo Upload & IndexedDB feature integrated cleanly into index.html!")
