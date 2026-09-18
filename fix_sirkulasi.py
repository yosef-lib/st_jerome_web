import codecs, re

with codecs.open('templates/cetak_sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()

# Fix checkboxes
pattern = r"<label class=\"flex items-center gap-2 cursor-pointer\">\s*<input type=\"checkbox\" id=\"chkIdentitas\".*?<span>Stiker Barcode</span>\s*</label>"
new_cb = '''<label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkKartu" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Kartu Buku (7.5x12 cm)</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer ml-4 border-l pl-4 border-stroke">
                            <input type="checkbox" id="chkKantong" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Kantong Buku (Lipat)</span>
                        </label>'''

html, count = re.subn(pattern, new_cb, html, flags=re.DOTALL)
print(f"Checkboxes replaced {count} times")

with codecs.open('templates/cetak_sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)

# Fix app.py variable
with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

app_code = app_code.replace("render_template('cetak_sirkulasi.html', buku_list=buku_list, page=page, total_pages=total_pages, search=search)", "render_template('cetak_sirkulasi.html', koleksi_list=[dict(row) for row in buku_list], page=page, total_pages=total_pages, search=search)")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("app.py updated")
