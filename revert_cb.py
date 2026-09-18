import codecs

with codecs.open('templates/cetak_khusus.html', 'r', 'utf-8') as f:
    html = f.read()

bad_cb = '''                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkBarcode" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Stiker Barcode</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer ml-4 border-l pl-4 border-stroke">
                            <input type="checkbox" id="chkKartu" class="form-checkbox text-primary h-5 w-5">
                            <span>Kartu Buku</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkKantong" class="form-checkbox text-primary h-5 w-5">
                            <span>Kantong Buku</span>
                        </label>
                    </div>'''

good_cb = '''                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkBarcode" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Stiker Barcode</span>
                        </label>
                    </div>'''

html = html.replace(bad_cb, good_cb)

bad_js = '''    const options = {
        identitas: document.getElementById('chkIdentitas').checked,
        punggung: document.getElementById('chkPunggung').checked,
        barcode: document.getElementById('chkBarcode').checked,
        kartu: document.getElementById('chkKartu').checked,
        kantong: document.getElementById('chkKantong').checked
    };'''

good_js = '''    const options = {
        identitas: document.getElementById('chkIdentitas').checked,
        punggung: document.getElementById('chkPunggung').checked,
        barcode: document.getElementById('chkBarcode').checked
    };'''

html = html.replace(bad_js, good_js)

with codecs.open('templates/cetak_khusus.html', 'w', 'utf-8') as f:
    f.write(html)
print("cetak_khusus reverted")
