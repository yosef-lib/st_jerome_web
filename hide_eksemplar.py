import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

old_alpine = "data() {"
new_alpine = "data() {\n            const urlParams = new URLSearchParams(window.location.search);\n            const editId = urlParams.get('edit');\n"
code = code.replace(old_alpine, new_alpine)

old_return = "return {"
new_return = "return {\n            editMode: !!editId,\n"
code = code.replace(old_return, new_return)

old_eksemplar_ui = """<h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">2. Pembuatan Eksemplar (Barcode)</h3>"""
new_eksemplar_ui = """<h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">2. Pembuatan Eksemplar (Barcode)</h3>"""
# Wait, I can wrap the whole div in x-show="!editMode"
old_div = """<div class="mb-4">
                <h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">2. Pembuatan Eksemplar (Barcode)</h3>"""
new_div = """<div class="mb-4" x-show="!editMode">
                <h3 class="text-md font-semibold border-b border-stroke pb-2 mb-4 text-slate-700">2. Pembuatan Eksemplar (Barcode)</h3>"""
code = code.replace(old_div, new_div)

old_jumlah = "jumlah: 1,\n                status_buku: 'BELI',"
new_jumlah = "jumlah: editId ? 0 : 1,\n                status_buku: 'BELI',"
code = code.replace(old_jumlah, new_jumlah)

old_jumlah2 = "jumlah: 1"
new_jumlah2 = "jumlah: this.editMode ? 0 : 1"
# wait, there are two jumlah: 1 in the file. I already replaced one. Let's just do a regex.

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("Eksemplar hidden in edit mode")
