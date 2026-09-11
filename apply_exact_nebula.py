import base64
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('nebula_backdrop.jpg', 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

data_uri = f"data:image/jpeg;base64,{b64_data}"
print("Base64 Data URI length:", len(data_uri))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the color variables with the exact pixel-sampled palette
old_palette = """    --space-void: #090314;
    --space-deep: #110622;
    --space-midnight: #1b0a30;
    --nebula-shadow: #2d0d38;
    --nebula-wine: #4c1758;
    --cosmic-amethyst: #723477;
    --cosmic-amethyst-light: #8e4494;
    --celestial-orchid: #be6fab;
    --celestial-orchid-glow: rgba(190, 111, 171, 0.4);
    --starlight-blush: #f6d6e5;"""

new_palette = f"""    /* Exact Swatches Extracted from User's Reference Image */
    --space-void: #0d0216;
    --space-deep: #210535;              /* Swatch 1: Deepest Cosmic Plum Black */
    --space-midnight: #28083e;
    --nebula-shadow: #420d4a;           /* Swatch 2: Deep Midnight Nebula Purple */
    --nebula-wine: #561460;
    --cosmic-amethyst: #7b347e;         /* Swatch 3: Vibrant Celestial Violet */
    --cosmic-amethyst-light: #944498;
    --celestial-orchid: #c774b2;        /* Swatch 4: Luminous Nebula Orchid / Magenta */
    --celestial-orchid-glow: rgba(199, 116, 178, 0.45);
    --starlight-blush: #f4d5e0;         /* Swatch 5: Soft Glowing Starlight Blush */
    --nebula-bg-data: url("{data_uri}");"""

if old_palette in html:
    html = html.replace(old_palette, new_palette)
    print("✓ Replaced color palette with exact swatches")
else:
    print("Warning: old palette block not found exactly")

# Now add the real Orion nebula background layer in CSS
old_bg_css = """.nebula-glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    pointer-events: none;
    z-index: 1;
    opacity: 0.38;
    mix-blend-mode: screen;
    animation: nebulaPulse 14s ease-in-out infinite alternate;
  }"""

new_bg_css = """.real-nebula-bg {
    position: fixed;
    inset: 0;
    background-image: var(--nebula-bg-data), url('nebula_backdrop.jpg');
    background-position: center 25%;
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.62;
    mix-blend-mode: screen;
    pointer-events: none;
    z-index: 1;
    filter: contrast(1.15) saturate(1.2);
  }
  .nebula-vignette {
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 50% 35%, transparent 20%, rgba(33, 5, 53, 0.6) 65%, #0d0216 100%);
    pointer-events: none;
    z-index: 1;
  }
  .nebula-glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    pointer-events: none;
    z-index: 1;
    opacity: 0.38;
    mix-blend-mode: screen;
    animation: nebulaPulse 14s ease-in-out infinite alternate;
  }"""

if old_bg_css in html:
    html = html.replace(old_bg_css, new_bg_css)
    print("✓ Added .real-nebula-bg CSS layer")

# Add the real nebula HTML element after canvas
old_canvas = '<canvas id="spaceCanvas"></canvas>'
new_canvas = '<canvas id="spaceCanvas"></canvas>\n\n<!-- Authentic Orion Nebula Background Layer -->\n<div class="real-nebula-bg"></div>\n<div class="nebula-vignette"></div>'

if old_canvas in html and 'class="real-nebula-bg"' not in html:
    html = html.replace(old_canvas, new_canvas)
    print("✓ Injected real nebula HTML elements")

# Update gate background to feel more galactic
old_gate_bg = "background: radial-gradient(circle at center, #1b0728 0%, #090314 90%);"
new_gate_bg = "background: radial-gradient(circle at center, #350c44 0%, #210535 55%, #0d0216 100%);"
if old_gate_bg in html:
    html = html.replace(old_gate_bg, new_gate_bg)
    print("✓ Enhanced gate cosmic gradient")

# Update gift box colors to exact swatches
old_box_grad = """          <linearGradient id="cosmicBoxGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#4c1758"/>
            <stop offset="55%" stop-color="#320f3d"/>
            <stop offset="100%" stop-color="#190622"/>
          </linearGradient>"""

new_box_grad = """          <linearGradient id="cosmicBoxGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#561460"/>
            <stop offset="45%" stop-color="#420d4a"/>
            <stop offset="100%" stop-color="#210535"/>
          </linearGradient>"""

if old_box_grad in html:
    html = html.replace(old_box_grad, new_box_grad)
    print("✓ Updated gift box SVG gradient to exact swatches")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html with embedded Orion Nebula backdrop!")
