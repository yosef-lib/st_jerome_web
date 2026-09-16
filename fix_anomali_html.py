import codecs

with codecs.open('templates/anomali.html', 'r', 'utf-8') as f:
    html = f.read()

old_table = '''        <table class="w-full table-auto">
            <thead>
                <tr class="bg-gray-2 text-left">
                    <th class="min-w-[220px] py-4 px-4 font-medium text-black">Judul Buku</th>
                    <th class="py-4 px-4 font-medium text-black">Eksemplar A & DDC</th>
                    <th class="py-4 px-4 font-medium text-black">Eksemplar B & DDC</th>
                </tr>
            </thead>
            <tbody>
                {% for row in inkonsistensi %}
                <tr class="border-b border-[#eee] hover:bg-gray-50 transition">
                    <td class="py-4 px-4">
                        <p class="text-sm font-medium text-black">{{ row['judul'] }}</p>
                    </td>
                    <td class="py-4 px-4">
                        <p class="text-sm font-bold text-warning">{{ row['no_induk_1'] }}</p>
                        <p class="text-sm font-bold text-warning">Call: {{ row['panggil_1'] }}</p>
                    </td>
                    <td class="py-4 px-4 bg-danger/10">
                        <p class="text-sm font-bold text-danger">{{ row['no_induk_2'] }}</p>
                        <p class="text-sm font-bold text-danger">Call: {{ row['panggil_2'] }}</p>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>'''

new_table = '''
        {% if inkonsistensi_dict %}
        <div class="flex flex-col gap-6">
            {% for judul, exemplars in inkonsistensi_dict.items() %}
            <div class="border border-stroke rounded-lg overflow-hidden shadow-sm">
                <div class="bg-gray-2 py-3 px-4 border-b border-stroke flex flex-col gap-1">
                    <h4 class="font-bold text-black text-sm">{{ judul }}</h4>
                    <span class="text-xs text-slate-500">Pengarang: {{ exemplars[0]['pengarang'] }} | Penerbit: {{ exemplars[0]['penerbit'] }} ({{ exemplars[0]['tahun_terbit'] }})</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full table-auto text-sm">
                        <thead>
                            <tr class="bg-white text-left text-slate-500 text-xs uppercase">
                                <th class="py-2 px-4 font-medium">No Induk</th>
                                <th class="py-2 px-4 font-medium">Nomor Panggil (Call Number)</th>
                                <th class="py-2 px-4 font-medium">DDC Dasar</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for ex in exemplars %}
                            <tr class="border-t border-[#eee] hover:bg-gray-50 transition">
                                <td class="py-2 px-4 font-bold text-black">{{ ex['no_induk'] }}</td>
                                <td class="py-2 px-4 font-bold text-danger">{{ ex['no_panggil'] }}</td>
                                <td class="py-2 px-4">{{ ex['klasifikasi'] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        <div class="mt-6 flex justify-between items-center">
            {% if page > 1 %}
            <a href="?lokasi={{ lokasi }}&page={{ page - 1 }}" class="rounded bg-primary py-2 px-4 text-white hover:bg-opacity-90 transition">
                <i class="fa-solid fa-chevron-left mr-1"></i> Sebelumnya
            </a>
            {% else %}
            <div></div>
            {% endif %}
            
            <span class="text-sm text-slate-500 font-medium">Halaman {{ page }} dari {{ total_pages }}</span>
            
            {% if page < total_pages %}
            <a href="?lokasi={{ lokasi }}&page={{ page + 1 }}" class="rounded bg-primary py-2 px-4 text-white hover:bg-opacity-90 transition">
                Selanjutnya <i class="fa-solid fa-chevron-right ml-1"></i>
            </a>
            {% else %}
            <div></div>
            {% endif %}
        </div>
        {% else %}
        <p class="text-success font-medium py-4">Tidak ada anomali DDC yang ditemukan!</p>
        {% endif %}
'''

html = html.replace(old_table, new_table)
html = html.replace("DDC Beda)", "DDC Beda) - Pagination")
with codecs.open('templates/anomali.html', 'w', 'utf-8') as f:
    f.write(html)

print("anomali frontend fixed")
