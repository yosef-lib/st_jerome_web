import codecs

with codecs.open('templates/cetak_khusus.html', 'r', 'utf-8') as f:
    html = f.read()

old_klas = '''                        <td class="border-b border-[#eee] py-4 px-4">
                            <p class="text-slate-500">{{ buku.klasifikasi }} {{ buku.cutter }} {{ buku.huruf_judul }}</p>
                        </td>'''

new_klas = '''                        <td class="border-b border-[#eee] py-4 px-4">
                            {% if buku.klasifikasi and buku.cutter %}
                            <p class="text-slate-500">{{ buku.klasifikasi }} {{ buku.cutter }} {{ buku.huruf_judul }}</p>
                            {% else %}
                            <span class="inline-flex rounded-full bg-danger bg-opacity-10 py-1 px-3 text-xs font-medium text-danger" title="Buku ini tidak memiliki nomor panggil yang lengkap">
                                <i class="fa-solid fa-triangle-exclamation mr-1"></i> Tidak Lengkap
                            </span>
                            {% endif %}
                        </td>'''

html = html.replace(old_klas, new_klas)

with codecs.open('templates/cetak_khusus.html', 'w', 'utf-8') as f:
    f.write(html)
print("ui fixed")
