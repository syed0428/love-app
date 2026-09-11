with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Gate Dialog prompt text
old_prompt = '<p>Enter the date that changed our lives forever to unlock this experience.</p>'
new_prompt = "<p>What's the date of our first day together? Enter it to unlock this experience.</p>"

if old_prompt in content:
    content = content.replace(old_prompt, new_prompt)
    print("Updated gate prompt text!")
else:
    print("Warning: old_prompt not found.")

# 2. Update config constants & Day Counter
old_config = """    const ANNIVERSARY_DATE = "13/07/2025";
    const ANNIVERSARY_RAW = "13072025";

    // Dynamic Day Counter (Counts days together from July 13, 2025)
    function initDaysCounter() {
      const startDate = new Date(2025, 6, 13); // Note: Month is 0-indexed (6 = July)"""

new_config = """    const ANNIVERSARY_DATE = "28/01/2023";
    const ANNIVERSARY_RAW = "28012023";

    // Dynamic Day Counter (Counts days together from January 28, 2023)
    function initDaysCounter() {
      const startDate = new Date(2023, 0, 28); // Note: Month is 0-indexed (0 = January)"""

if old_config in content:
    content = content.replace(old_config, new_config)
    print("Updated anniversary constants and day counter!")
else:
    print("Warning: old_config not found.")

# 3. Update auto-unlock and validation checks
old_auto = 'if (val === "13072025") {'
new_auto = 'if (val === "28012023" || val === ANNIVERSARY_RAW) {'

if old_auto in content:
    content = content.replace(old_auto, new_auto)
    print("Updated auto-unlock check!")
else:
    print("Warning: old_auto not found.")

old_validation = 'if (raw === "13072025" || raw === ANNIVERSARY_RAW || dateInput.value.trim() === ANNIVERSARY_DATE) {'
new_validation = 'if (raw === "28012023" || raw === ANNIVERSARY_RAW || dateInput.value.trim() === ANNIVERSARY_DATE) {'

if old_validation in content:
    content = content.replace(old_validation, new_validation)
    print("Updated submit validation check!")
else:
    print("Warning: old_validation not found.")

# 4. Update Progressive Hints
old_hints = """          if (failedDateAttempts === 1) {
            dateFeedback.textContent = "Hint: That unforgettable day in July... ♥";
          } else if (failedDateAttempts === 2) {
            dateFeedback.textContent = "Our official anniversary date! 13-07-2025 😄";
          } else {
            dateFeedback.textContent = "Try typing: 13 / 07 / 2025 ✨";
          }"""

new_hints = """          if (failedDateAttempts === 1) {
            dateFeedback.textContent = "Hint: Our very first day together in January 2023... ♥";
          } else if (failedDateAttempts === 2) {
            dateFeedback.textContent = "It was a Saturday, 28-01-2023 😄";
          } else {
            dateFeedback.textContent = "Try typing: 28 / 01 / 2023 ✨";
          }"""

if old_hints in content:
    content = content.replace(old_hints, new_hints)
    print("Updated progressive hints!")
else:
    print("Warning: old_hints not found.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated index.html successfully!")
