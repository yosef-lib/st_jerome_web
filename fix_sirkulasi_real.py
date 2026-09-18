import codecs, re

with codecs.open('templates/cetak_sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

pattern = r"<div class=\"flex flex-wrap gap-6 mb-6\">\s*<label class=\"flex items-center gap-2 cursor-pointer\">.*?Stiker Barcode</span>\s*</label>\s*</div>"
new_cb = '''<div class="flex flex-wrap gap-6 mb-6">
                <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" id="chkKartu" checked class="w-5 h-5 accent-primary cursor-pointer">
                    <span class="text-black font-medium">Kartu Buku (7.5x12 cm)</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" id="chkKantong" checked class="w-5 h-5 accent-primary cursor-pointer">
                    <span class="text-black font-medium">Kantong Buku (Lipat)</span>
                </label>
            </div>'''
html, count = re.subn(pattern, new_cb, html, flags=re.DOTALL)
print(f"Checkboxes replaced {count} times")

js_pattern = r"const options = \{\s*identitas: document.getElementById\('opt_identitas'\).checked,\s*punggung: document.getElementById\('opt_punggung'\).checked,\s*barcode: document.getElementById\('opt_barcode'\).checked\s*\};"
new_js = '''const options = {
                identitas: false,
                punggung: false,
                barcode: false,
                kartu: document.getElementById('chkKartu').checked,
                kantong: document.getElementById('chkKantong').checked
            };'''
html, count = re.subn(js_pattern, new_js, html, flags=re.DOTALL)
print(f"JS options replaced {count} times")

with codecs.open('templates/cetak_sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
