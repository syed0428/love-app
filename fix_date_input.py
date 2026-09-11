import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update maxlength on dateInput
content = content.replace(
    '<input type="text" id="dateInput" class="date-input" placeholder="DD / MM / YYYY" maxlength="10" autocomplete="off">',
    '<input type="text" id="dateInput" class="date-input" placeholder="DD / MM / YYYY" maxlength="14" autocomplete="off">'
)

# 2. Update the input event listener to support full 8 digits and auto-submit on completion
old_input_logic = """  if (dateInput) {
    // Auto-insert slash as user types numbers (dd/mm/yyyy)
    dateInput.addEventListener("input", (e) => {
      let val = e.target.value.replace(/\D/g, "");
      if (val.length > 8) val = val.substring(0, 8);

      let formatted = val;
      if (val.length > 2 && val.length <= 4) {
        formatted = val.substring(0, 2) + " / " + val.substring(2);
      } else if (val.length > 4) {
        formatted = val.substring(0, 2) + " / " + val.substring(2, 4) + " / " + val.substring(4);
      }
      e.target.value = formatted;
    });

    dateInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        dateSubmitBtn.click();
      }
    });
  }"""

new_input_logic = """  if (dateInput) {
    // Auto-insert slash as user types numbers (dd / mm / yyyy)
    dateInput.addEventListener("input", (e) => {
      let val = e.target.value.replace(/\D/g, "");
      if (val.length > 8) val = val.substring(0, 8);

      let formatted = val;
      if (val.length > 4) {
        formatted = val.substring(0, 2) + " / " + val.substring(2, 4) + " / " + val.substring(4);
      } else if (val.length > 2) {
        formatted = val.substring(0, 2) + " / " + val.substring(2);
      }
      e.target.value = formatted;

      // Auto-unlock immediately when full valid date (8 digits) is entered
      if (val === "13072025") {
        setTimeout(() => {
          dateSubmitBtn.click();
        }, 300);
      }
    });

    dateInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        dateSubmitBtn.click();
      }
    });
  }"""

if old_input_logic in content:
    content = content.replace(old_input_logic, new_input_logic)
    print("✓ Updated input event logic with auto-unlock")
else:
    print("Warning: old input logic not found exactly")

# 3. Ensure validation logic checks raw digits
old_val_check = """      const raw = dateInput.value.replace(/\D/g, "");
      if (raw === ANNIVERSARY_RAW || dateInput.value.trim() === ANNIVERSARY_DATE) {"""

new_val_check = """      const raw = dateInput.value.replace(/\D/g, "");
      if (raw === "13072025" || raw === ANNIVERSARY_RAW || dateInput.value.trim() === ANNIVERSARY_DATE) {"""

if old_val_check in content:
    content = content.replace(old_val_check, new_val_check)
    print("✓ Updated validation check")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html fixed successfully!")
