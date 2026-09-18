import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

# Add action buttons for Bibliografi
actions_html = '''
                                    <div class="flex justify-between items-center mb-3">
                                        <h4 class="font-semibold text-sm text-slate-700">Daftar Barcode (Salinan)</h4>
                                        <div class="flex gap-2">
                                            <a :href="'/input_buku?edit=' + b.id" class="px-3 py-1 bg-warning text-white text-xs rounded font-medium hover:bg-opacity-90 transition"><i class="fa-solid fa-pen-to-square"></i> Edit Bibliografi</a>
                                            <button @click="deleteBiblio(b.id)" class="px-3 py-1 bg-danger text-white text-xs rounded font-medium hover:bg-opacity-90 transition"><i class="fa-solid fa-trash"></i> Hapus Buku</button>
                                        </div>
                                    </div>
'''
code = code.replace('<h4 class="font-semibold text-sm mb-3 text-slate-700">Daftar Barcode (Salinan)</h4>', actions_html)

# Add Delete action column header for Eksemplar
code = code.replace('<th class="p-2">Status Peminjaman</th>', '<th class="p-2">Status Peminjaman</th>\n<th class="p-2 text-center w-10">Aksi</th>')

# Add Delete button for Eksemplar
eksemplar_action = '''
                                                    <td class="p-2 text-center">
                                                        <button @click="deleteEksemplar(e.id)" class="text-danger hover:text-opacity-70" title="Hapus Salinan"><i class="fa-solid fa-trash-can"></i></button>
                                                    </td>
                                                </tr>
'''
code = code.replace('''                                                </tr>\n                                            </template>''', eksemplar_action + '                                            </template>')

code = code.replace('<td colspan="4" class="p-3', '<td colspan="5" class="p-3')

# Update JS
js_methods = '''
        async deleteBiblio(id) {
            if (!confirm("Peringatan: Anda akan menghapus judul buku ini BESERTA seluruh salinannya! Lanjutkan?")) return;
            try {
                const res = await fetch('/api/bibliografi/' + id, { method: 'DELETE' });
                if (res.ok) {
                    this.loadData(this.currentPage);
                }
            } catch (e) {
                console.error(e); alert("Error");
            }
        },
        async deleteEksemplar(id) {
            if (!confirm("Hapus barcode ini?")) return;
            try {
                const res = await fetch('/api/eksemplar/' + id, { method: 'DELETE' });
                if (res.ok) {
                    // refresh eksemplar list
                    this.toggleEksemplar(this.expandedId); 
                    this.toggleEksemplar(this.expandedId); // double toggle to refresh
                    this.loadData(this.currentPage);
                }
            } catch (e) {
                console.error(e); alert("Error");
            }
        },
'''
code = code.replace('async loadData(page = 1) {', js_methods + '\n        async loadData(page = 1) {')

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Patched koleksi.html for delete")
