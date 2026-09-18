import codecs

with codecs.open('templates/input_buku.html', 'r', 'utf-8') as f:
    code = f.read()

old_code = """<input type="number" x-model="form.jumlah" min="1" max="50" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black font-bold text-lg" required>
                        </div>
                        <div class="w-2/3">"""

new_code = """<input type="number" x-model="form.jumlah" min="1" max="50" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black font-bold text-lg" required>
                        </div>
                        <div class="w-1/3">
                            <label class="block text-sm font-medium mb-1">Asal Koleksi</label>
                            <select x-model="form.status_buku" class="w-full border border-stroke rounded px-3 py-2 outline-none focus:border-primary text-black font-semibold text-md" required>
                                <option value="BELI">Beli</option>
                                <option value="HIBAH">Hadiah / Hibah</option>
                            </select>
                        </div>
                        <div class="w-1/3">"""

code = code.replace(old_code, new_code)

old_js = "jumlah: 1,"
new_js = "jumlah: 1,\n                status_buku: 'BELI',"
code = code.replace(old_js, new_js)

old_fd = "formData.append('jumlah_eksemplar', this.form.jumlah);"
new_fd = "formData.append('jumlah_eksemplar', this.form.jumlah);\n            formData.append('status_buku', this.form.status_buku);"
code = code.replace(old_fd, new_fd)

with codecs.open('templates/input_buku.html', 'w', 'utf-8') as f:
    f.write(code)
print("status_buku added")
