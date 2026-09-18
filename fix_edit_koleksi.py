import codecs

with codecs.open('templates/edit_koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

checkbox_html = '''        </div>
        
        <div class="mb-5 flex flex-col xl:flex-row gap-5">
            <div class="w-full">
                <label class="mb-2.5 block text-black font-medium text-sm">Status Peminjaman</label>
                <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" name="is_reference_only" value="1" {% if buku.is_reference_only %}checked{% endif %} class="w-5 h-5 rounded border-stroke text-primary focus:ring-primary">
                    <span class="text-black">Jadikan Buku Referensi / Hanya Baca di Tempat (Tidak Bisa Dipinjam)</span>
                </label>
            </div>
        </div>'''

code = code.replace('''                </select>
            </div>
        </div>''', '''                </select>
            </div>
        </div>''' + checkbox_html)

with codecs.open('templates/edit_koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Updated edit_koleksi.html")
