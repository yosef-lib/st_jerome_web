import codecs

with codecs.open('templates/cetak_khusus.html', 'r', 'utf-8') as f:
    html = f.read()

# Change title and text
html = html.replace('Cetak Stiker Khusus', 'Cetak Kartu & Kantong Buku')
html = html.replace('Pilih buku dan jenis stiker yang ingin dicetak', 'Pilih buku untuk mencetak kelengkapan sirkulasi fisik')
html = html.replace('Pilih komponen stiker yang ingin dicetak.', 'Pilih komponen sirkulasi yang ingin dicetak di kertas tebal/manila.')

# Change checkboxes
old_cb = '''                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkIdentitas" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Stiker Identitas</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkPunggung" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Label Punggung</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkBarcode" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Stiker Barcode</span>
                        </label>'''

new_cb = '''                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkKartu" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Kartu Buku (7.5x12 cm)</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="chkKantong" class="form-checkbox text-primary h-5 w-5" checked>
                            <span>Kantong Buku (Lipat)</span>
                        </label>'''
html = html.replace(old_cb, new_cb)

# Change session storage key
html = html.replace("sessionStorage.getItem('selectedBooks_khusus'", "sessionStorage.getItem('selectedBooks_kartu'")
html = html.replace("sessionStorage.setItem('selectedBooks_khusus'", "sessionStorage.setItem('selectedBooks_kartu'")

# Change JS payload options
old_js = '''    const options = {
        identitas: document.getElementById('chkIdentitas').checked,
        punggung: document.getElementById('chkPunggung').checked,
        barcode: document.getElementById('chkBarcode').checked
    };'''
new_js = '''    const options = {
        identitas: false,
        punggung: false,
        barcode: false,
        kartu: document.getElementById('chkKartu').checked,
        kantong: document.getElementById('chkKantong').checked
    };'''
html = html.replace(old_js, new_js)

# Change endpoint
html = html.replace("fetch('/api/cetak_khusus'", "fetch('/api/cetak_kartu'")
# Change page search URL
html = html.replace("window.location.href = '/cetak_khusus", "window.location.href = '/cetak_kartu")

with codecs.open('templates/cetak_kartu.html', 'w', 'utf-8') as f:
    f.write(html)
print("cetak_kartu created")
