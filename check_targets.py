with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

def check(name, target):
    idx = c.find(target)
    print(f"{name}: {'FOUND at ' + str(idx) if idx != -1 else 'NOT FOUND'}")

check("old_envelopes_css", ".envelopes-grid {\n      display: grid;\n      grid-template-columns: repeat(3, 1fr);")
check("gate", ".gate {\n      position: fixed;\n      inset: 0;")
check("old_no_btn_css", ".btn-no-dodger {")
check("old_propose_html", 'class="propose-buttons"')
check("old_dialog_switch", 'dateGateDialog.classList.remove("active");')
check("old_dodge_js", 'function initNoButtonPosition()')
