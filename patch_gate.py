with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make gate disappear completely when hidden
text = text.replace(
    """.gate.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
  }""",
    """.gate.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    display: none !important;
  }"""
)

text = text.replace(
    """      setTimeout(() => {
        const gate = document.getElementById("gateOverlay");
        const main = document.getElementById("mainExperience");
        gate.classList.add("hidden");
        main.classList.add("revealed");
        btnNo.style.display = "none";
        initTypingEffect();
      }, 1400);""",
    """      setTimeout(() => {
        const gate = document.getElementById("gateOverlay");
        const main = document.getElementById("mainExperience");
        gate.classList.add("hidden");
        gate.style.display = "none";
        main.classList.add("revealed");
        btnNo.style.display = "none";
        initTypingEffect();
      }, 1400);"""
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched gate.hidden smoothly!")
