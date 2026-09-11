with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

def show(target, len_after=300):
    idx = c.find(target)
    print(f"=== {target} ===")
    print(repr(c[idx:idx+len_after]))

show(".gate {\n      position: fixed;")
show(".btn-no-dodger {")
show('class="propose-buttons"')
show('dateGateDialog.classList.remove("active");')
show('function initNoButtonPosition()', 1200)
