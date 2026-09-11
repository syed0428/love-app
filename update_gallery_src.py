import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .frame-inner img CSS to include z-index: 2
old_img_css = """.frame-inner img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.6s ease;
    }"""

new_img_css = """.frame-inner img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 2; /* Sits cleanly over placeholder card when loaded */
      transition: transform 0.6s ease;
    }"""

assert old_img_css in content, "old_img_css not found!"
content = content.replace(old_img_css, new_img_css)

# 2. Update Chapter 2 Gallery HTML
old_gallery_start = '<!-- Frame 1 -->'
old_gallery_end = '<!-- CHAPTER 3: INTERACTIVE ENVELOPES -->'

idx1 = content.find(old_gallery_start)
idx2 = content.find(old_gallery_end)
assert idx1 != -1 and idx2 != -1, "Gallery markers not found!"

new_gallery_html = """<!-- Frame 1: Your favourite photo of us -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo1.jpg" alt="Your favourite photo of us" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>First Steps</h4>
                <p>Your smile that lights up the room</p>
              </div>
            </div>
            <div class="frame-caption">"Your favourite photo of us"</div>
          </div>

          <!-- Frame 2: A trip you both loved -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo2.jpg" alt="A trip you both loved" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>Blessed Journey</h4>
                <p>Umrah together in Mecca</p>
              </div>
            </div>
            <div class="frame-caption">"A trip you both loved"</div>
          </div>

          <!-- Frame 3: Her, mid-laugh -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo3.jpg" alt="Her, mid-laugh" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>Laughter</h4>
                <p>Every small teasing moment</p>
              </div>
            </div>
            <div class="frame-caption">"Her, mid-laugh"</div>
          </div>

          <!-- Frame 4: A quiet ordinary day -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo4.jpg" alt="A quiet ordinary day" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>Our Quiet Evenings</h4>
                <p>Peaceful conversations together</p>
              </div>
            </div>
            <div class="frame-caption">"A quiet ordinary day"</div>
          </div>

          <!-- Frame 5: The two of you, together -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo5.jpg" alt="The two of you, together" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>Madurai Days</h4>
                <p>Treasured hometown memories</p>
              </div>
            </div>
            <div class="frame-caption">"The two of you, together"</div>
          </div>

          <!-- Frame 6: One more, just because -->
          <div class="photo-frame">
            <div class="frame-inner">
              <img src="photo6.jpg" alt="One more, just because" onerror="this.style.display='none'" onload="this.style.display='block'">
              <div class="placeholder-card">
                <div class="star-icon">✦</div>
                <h4>Forever Ahead</h4>
                <p>Waiting to be together again</p>
              </div>
            </div>
            <div class="frame-caption">"One more, just because"</div>
          </div>
        </div>
      </div>
    </section>

    """

content = content[:idx1] + new_gallery_html + content[idx2:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Gallery image src attributes and captions updated in index.html!")
