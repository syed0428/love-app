import re

with open('nebula_b64.txt', 'r') as f:
    nebula_b64 = f.read().strip()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the base64 background variable
html = re.sub(r'--nebula-bg-data:\s*url\([^)]+\);', f'--nebula-bg-data: url("{nebula_b64}");', html)

# 2. Replace the background CSS section with clean, high-performance GPU-friendly CSS
old_bg_section_regex = r'/\* Fixed Nebula Backdrops \*/.*?(?=/\* Floating Parallax Hearts)'
new_bg_section = """/* Fixed Nebula Backdrops (High Performance GPU Accelerated) */
  .real-nebula-bg {
    position: fixed;
    inset: 0;
    background-image: var(--nebula-bg-data), url('nebula_backdrop.jpg');
    background-position: center 25%;
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.70;
    mix-blend-mode: screen;
    pointer-events: none;
    z-index: 1;
    transform: translateZ(0);
  }
  .nebula-vignette {
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 50% 35%, transparent 25%, rgba(33, 5, 53, 0.55) 65%, #0d0216 100%);
    pointer-events: none;
    z-index: 1;
    transform: translateZ(0);
  }
"""
html = re.sub(old_bg_section_regex, new_bg_section, html, flags=re.DOTALL)

# 3. Remove .grain CSS if present
html = re.sub(r'/\* Subtle Texture Overlay \*/\s*\.grain\s*\{[^}]*\}', '', html)

# 4. Remove .grain and .nebula-glow elements from HTML body
html = re.sub(r'<div class="nebula-glow[^"]*"></div>\s*', '', html)
html = re.sub(r'<div class="grain"></div>\s*', '', html)

# 5. Optimize Cards CSS for smooth 60fps scrolling
# Reduce heavy 16px blur to crisp 6px blur with solid background fallback
html = html.replace("backdrop-filter: blur(16px);", "backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);")
html = html.replace("backdrop-filter: blur(14px);", "backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);")
html = html.replace("backdrop-filter: blur(12px);", "backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);")

# 6. Replace the Canvas Starfield and Hero Tilt JS with ultra-optimized 60fps versions
old_canvas_js_regex = r'// ---------- CANVAS STARFIELD & SHOOTING STARS ----------.*?// ---------- SCROLL PROGRESS & PARALLAX HEARTS ----------'
new_canvas_js = """// ---------- CANVAS STARFIELD & SHOOTING STARS (HIGH-FPS OPTIMIZED) ----------
  function initStarfield() {
    const canvas = document.getElementById("spaceCanvas");
    const ctx = canvas.getContext("2d");
    let stars = [];
    let shootingStars = [];
    let width, height;

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      createStars();
    }

    function createStars() {
      stars = [];
      // Fixed, optimal star count: 120 stars (no lag on any laptop or phone)
      const numStars = 120;
      for (let i = 0; i < numStars; i++) {
        stars.push({
          x: Math.random() * width,
          y: Math.random() * height,
          radius: Math.random() * 1.3 + 0.4,
          alpha: Math.random() * 0.7 + 0.3,
          speed: Math.random() * 0.015 + 0.005,
          color: Math.random() > 0.35 ? '#f4d5e0' : (Math.random() > 0.5 ? '#c774b2' : '#ffffff'),
          isBright: Math.random() > 0.75
        });
      }
    }

    function addShootingStar() {
      if (shootingStars.length < 1 && Math.random() < 0.008) {
        shootingStars.push({
          x: Math.random() * width * 0.7,
          y: Math.random() * height * 0.35,
          len: Math.random() * 80 + 50,
          speed: Math.random() * 6 + 7,
          angle: (Math.PI / 4) + (Math.random() * 0.2 - 0.1),
          alpha: 1
        });
      }
    }

    let lastTime = 0;
    function draw(timestamp) {
      // Throttle slightly if needed, smooth 60fps
      ctx.clearRect(0, 0, width, height);

      // Draw Twinkling Stars (Zero shadowBlur for 60fps hardware acceleration)
      for (let i = 0; i < stars.length; i++) {
        const star = stars[i];
        star.alpha += Math.sin(timestamp * star.speed) * 0.012;
        if (star.alpha > 1) star.alpha = 1;
        if (star.alpha < 0.2) star.alpha = 0.2;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = star.color;
        ctx.globalAlpha = star.alpha;
        ctx.fill();

        // Soft halo for bright stars (drawn with arc instead of expensive shadowBlur)
        if (star.isBright) {
          ctx.beginPath();
          ctx.arc(star.x, star.y, star.radius * 2.4, 0, Math.PI * 2);
          ctx.fillStyle = star.color;
          ctx.globalAlpha = star.alpha * 0.18;
          ctx.fill();
        }
      }

      // Draw Shooting Stars
      addShootingStar();
      for (let i = shootingStars.length - 1; i >= 0; i--) {
        let ss = shootingStars[i];
        ctx.beginPath();
        ctx.moveTo(ss.x, ss.y);
        let endX = ss.x - Math.cos(ss.angle) * ss.len;
        let endY = ss.y - Math.sin(ss.angle) * ss.len;
        let grad = ctx.createLinearGradient(ss.x, ss.y, endX, endY);
        grad.addColorStop(0, "rgba(255, 255, 255, " + ss.alpha + ")");
        grad.addColorStop(0.5, "rgba(199, 116, 178, " + (ss.alpha * 0.7) + ")");
        grad.addColorStop(1, "transparent");

        ctx.strokeStyle = grad;
        ctx.lineWidth = 1.8;
        ctx.lineTo(endX, endY);
        ctx.stroke();

        ss.x += Math.cos(ss.angle) * ss.speed;
        ss.y += Math.sin(ss.angle) * ss.speed;
        ss.alpha -= 0.022;

        if (ss.alpha <= 0 || ss.x > width || ss.y > height) {
          shootingStars.splice(i, 1);
        }
      }

      ctx.globalAlpha = 1;
      requestAnimationFrame(draw);
    }

    window.addEventListener("resize", resize);
    resize();
    requestAnimationFrame(draw);
  }

  // ---------- SCROLL PROGRESS & PARALLAX HEARTS ----------"""

html = re.sub(old_canvas_js_regex, new_canvas_js, html, flags=re.DOTALL)

# 7. Optimize Hero 3D Tilt with requestAnimationFrame throttling
old_tilt_js_regex = r'// ---------- DESKTOP 3D TILT ON HERO ----------.*?// ---------- STEP 1: GIFT BOX OPENING ----------'
new_tilt_js = """// ---------- DESKTOP 3D TILT ON HERO (THROTTLED WITH RAF) ----------
  function initHeroTilt() {
    const hero = document.getElementById("heroSection");
    const tiltWrapper = document.getElementById("heroTilt");
    if (!hero || !tiltWrapper) return;

    if (window.matchMedia("(pointer: fine)").matches) {
      let ticking = false;
      let mouseX = 0, mouseY = 0;

      hero.addEventListener("mousemove", (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (!ticking) {
          requestAnimationFrame(() => {
            const rect = hero.getBoundingClientRect();
            const x = mouseX - rect.left - rect.width / 2;
            const y = mouseY - rect.top - rect.height / 2;
            const tiltX = (y / (rect.height / 2)) * -6;
            const tiltY = (x / (rect.width / 2)) * 6;
            tiltWrapper.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateZ(0)`;
            ticking = false;
          });
          ticking = true;
        }
      });

      hero.addEventListener("mouseleave", () => {
        tiltWrapper.style.transform = "rotateX(0deg) rotateY(0deg) translateZ(0)";
      });
    }
  }

  // ---------- STEP 1: GIFT BOX OPENING ----------"""

html = re.sub(old_tilt_js_regex, new_tilt_js, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Performance optimization applied successfully to index.html!")
